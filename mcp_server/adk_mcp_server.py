# adk_mcp_server.py
import asyncio
import json
from dotenv import load_dotenv
import traceback
from pathlib import Path
# MCP Server Imports
from mcp import types as mcp_types # Use alias to avoid conflict with genai.types
from mcp.server.lowlevel import Server, NotificationOptions
from mcp.server.models import InitializationOptions
import mcp.server.stdio


# ADK Tool Imports
from google.adk.tools.function_tool import FunctionTool
from google.adk.tools.load_web_page import load_web_page # Example ADK tool
# ADK <-> MCP Conversion Utility
from google.adk.tools.mcp_tool.conversion_utils import adk_to_mcp_tool_type

# Import your custom tools
from tools.parse_input import parse_input
from tools.detect_lead import detect_lead
from tools.create_salesforce_lead import create_salesforce_lead

# Wrap functions as ADK tools
parse_input_tool = FunctionTool(parse_input)
detect_lead_tool = FunctionTool(detect_lead)
create_lead_tool = FunctionTool(create_salesforce_lead)

# --- Load Environment Variables (If ADK tools need them) ---
current_dir = Path(__file__).parent.resolve()
env_path = current_dir.parent/".env"
print(f"Loading .env file from {env_path}")
load_dotenv(env_path)
print("DotEnv File Loaded")
## <<Custom>>
# Define your generator function (see example below)
def create_opprtunity(account_name: str, amount: float) -> str:
    print(f"🔥 Received input: {account_name}")
    """
    Creates an opportunity for the given account name and amount.
    
    Args:
        account_name (str): Name of the account.
        amount (float): Deal value in USD.

    Returns:
        str: Confirmation message.
    """
    return f"Opportunity created for {account_name} with amount ${amount}"

# Wrap the function
create_opprtunity_tool = FunctionTool(func=create_opprtunity)
## <<Custom>>

# --- Prepare the ADK Tool ---
# Instantiate the ADK tool you want to expose
print("Initializing ADK load_web_page tool...")
adk_web_tool = FunctionTool(load_web_page)
print(f"ADK tool '{adk_web_tool.name}' initialized.")
# --- End ADK Tool Prep ---

# --- MCP Server Setup ---
print("Creating MCP Server instance...")
# Create a named MCP Server instance
app = Server("adk-web-tool-mcp-server")

# Implement the MCP server's @app.list_tools handler


@app.list_tools()
async def list_tools() -> list[mcp_types.Tool]:
  """MCP handler to list available tools."""
  print("MCP Server: Received list_tools request.")
  # Convert the ADK tool's definition to MCP format
  mcp_tool_schema = [adk_to_mcp_tool_type(adk_web_tool),
                      adk_to_mcp_tool_type(parse_input_tool),
        adk_to_mcp_tool_type(detect_lead_tool),
        adk_to_mcp_tool_type(create_lead_tool)]
  for t in mcp_tool_schema:
    print(f"MCP Server: Advertising tool: {t.name}")
  return mcp_tool_schema



@app.call_tool()
async def call_tool(name: str, arguments: dict) -> list[mcp_types.TextContent | mcp_types.ImageContent | mcp_types.EmbeddedResource]:
 #   Handle tool execution calls
    # 3. Map tool names to their FunctionTool instances
    tools = {
        adk_web_tool.name: adk_web_tool,
        parse_input_tool.name: parse_input_tool,
        detect_lead_tool.name: detect_lead_tool,
        create_lead_tool.name: create_lead_tool
    }
    # 4. Invoke the requested tool if available
    if name in tools:
        try:
            result = await tools[name].run_async(args=arguments, tool_context=None)
            # Return result as text content (JSON-formatted)
            return [mcp_types.TextContent(type="text", text=json.dumps(result))]
        except Exception as e:
            error = {"error": f"Failed to execute tool '{name}': {str(e)}"}
            return [mcp_types.TextContent(type="text", text=json.dumps(error))]
    else:
        # Tool name not recognized
        error = {"error": f"Tool '{name}' not implemented."}
        return [mcp_types.TextContent(type="text", text=json.dumps(error))]

# --- MCP Server Runner ---
async def run_server():
  """Runs the MCP server over standard input/output."""
  # Use the stdio_server context manager from the MCP library
  async with mcp.server.stdio.stdio_server() as (read_stream, write_stream):
    print("MCP Server starting handshake...")
    await app.run(
        read_stream,
        write_stream,
        InitializationOptions(
            server_name=app.name, # Use the server name defined above
            server_version="0.1.0",
            capabilities=app.get_capabilities(
                # Define server capabilities - consult MCP docs for options
                notification_options=NotificationOptions(),
                experimental_capabilities={},
            ),
        ),
    )
    print("MCP Server run loop finished.")

if __name__ == "__main__":
  print("Launching MCP Server exposing ADK tools...")
  try:
    asyncio.run(run_server())
  except KeyboardInterrupt:
    print("\nMCP Server stopped by user.")
  except Exception as e:
    print(f"MCP Server encountered an error: {e}")
  finally:
    print("MCP Server process exiting.")
# --- End MCP Server ---