import os
import sys
import traceback
import asyncio
from pathlib import Path
from dotenv import load_dotenv
from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from google.genai import types
from google.adk.agents.llm_agent import LlmAgent
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.adk.artifacts.in_memory_artifact_service import InMemoryArtifactService
from google.adk.tools.mcp_tool.mcp_toolset import MCPToolset, StdioServerParameters
import uvicorn

current_dir = Path(__file__).parent.resolve()
env_path = current_dir.parent/".env"
print(f"Loading .env file from {env_path}")
load_dotenv(env_path)
print("DotEnv File Loaded")
server_script = current_dir.parent/"mcp_server/adk_mcp_server.py"
server_script_str = str(server_script.resolve()) 
print(f"Script Path: {server_script_str}")
  

app = FastAPI()
app.mount("/static", StaticFiles(directory="ui/static"), name="static")
templates = Jinja2Templates(directory="ui/templates")


async def get_tools_async():
  """Gets tools from the File System MCP Server."""
  print("Attempting to connect to MCP Filesystem server...")
  tools, exit_stack = await MCPToolset.from_server(
      # Use StdioServerParameters for local process communication
      connection_params=StdioServerParameters(
          command="C:\\Users\\pvispute\\AppData\\Local\\Programs\\Python\\Python311\\python.exe", # Command to run the server
          args=[
                "C:\\Users\\pvispute\\Documents\\GADK\\LeadSurgeAI\\mcp_server\\adk_mcp_server.py"],
      )
  )
  print("MCP Toolset created successfully.")
  # MCP requires maintaining a connection to the local MCP Server.
  # exit_stack manages the cleanup of this connection.
  return tools, exit_stack


# --- Step 2: Agent Definition ---
async def get_agent_async():
  """Creates an ADK Agent equipped with tools from the MCP Server."""
  tools, exit_stack = await get_tools_async()
  print(f"Fetched {len(tools)} tools from MCP server.")
  root_agent = LlmAgent(
      model='gemini-2.0-flash', # Adjust model name if needed based on availability
      name='filesystem_assistant',
      instruction='Parse user input, detect lead if it is a qualified lead, and create a Salesforce lead if yes.',
      tools=tools, # Provide the MCP tools to the ADK agent
  )
  return root_agent, exit_stack


# --- Step 3: Main Execution Logic ---
async def async_main(user_input: str) -> str:
  session_service = InMemorySessionService()
  # Artifact service might not be needed for this example
  artifacts_service = InMemoryArtifactService()

  session = session_service.create_session(
      state={}, app_name='leadsurge', user_id='user_fs'
  )

  print(f"User Query: '{user_input}'")
  content = types.Content(role='user', parts=[types.Part(text=user_input)])
  root_agent, exit_stack = await get_agent_async()
  runner = Runner(
      app_name='leadsurge',
      agent=root_agent,
      artifact_service=artifacts_service, # Optional
      session_service=session_service,
  )

  print("Running agent...")
  events_async = runner.run_async(
      session_id=session.id, user_id=session.user_id, new_message=content
  )
  
  final_output = ""
  async for event in events_async:
        print(f"Event received: {event}")
        if event.content:
            final_output = event.content.parts[0].text
  # Crucial Cleanup: Ensure the MCP server process connection is closed.
  print("Closing MCP server connection...")
  await exit_stack.aclose()
  print("Cleanup complete.")
  return final_output

@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("index.html", {
        "request": request,
        "user_input": "",
        "result": None,
        "error": None
    })


@app.post("/process", response_class=HTMLResponse)
async def process(request: Request, user_input: str = Form(...)):
    result = None
    error = None

    try:
        result = await async_main(user_input)
    except Exception:
        error = traceback.format_exc()
        print("[❌ ERROR]\n", error)

    return templates.TemplateResponse("index.html", {
        "request": request,
        "user_input": user_input,
        "result": result,
        "error": error
    })
if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=3000)