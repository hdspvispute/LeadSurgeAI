# 🚀 LeadSurge AI — Multi-Agent Lead Generation Demo

LeadSurge AI is a multi-agent system built using **Google Agent Development Kit (ADK)** and **MCP** to automate **lead detection** and **CRM integration** from natural language inputs like emails, transcripts, or audio.

---

## 🧠 What It Does

✅ Accepts user input (email, text, or voice transcript)  
✅ Detects if the message is a qualified lead  
✅ Automatically creates a lead in Salesforce (or mock CRM)  
✅ Fully agent-driven using MCP + FunctionTool architecture  
✅ Modern FastAPI UI to test it live

---

## 🧱 Architecture

![Lead Generation Architecture](./path/to/diagram.png) <!-- Replace with actual image path -->

### Components
| Component                  | Description                                    |
|---------------------------|------------------------------------------------|
| `parse_input`             | Preprocesses raw input into plain text         |
| `detect_lead`             | Uses LLMs or logic to determine lead quality   |
| `create_salesforce_lead`  | Creates a lead via API (mock or real)          |
| `adk_mcp_server.py`       | Wraps tools as FunctionTool and serves via MCP |
| `agent_runner.py`         | ADK agent that orchestrates tools via MCPToolset |
| `FastAPI UI`              | Clean web UI to test end-to-end flow           |

---

## 🧪 How to Run

### 1. 🔧 Start MCP Server

```bash
python mcp_server/adk_mcp_server.py

uvicorn ui.main:app --reload

Friday, April 11, 2025
2:21 PM

curl https://login.salesforce.com/services/oauth2/token ^
  -d "grant_type=password" ^
  -d "client_id=3MVG9rZjd7MXFdLihHhvr5DWWGAq3BcI7KIz0jDL51WAXsH0x9grpo2TSn0A5sXyKl_SsrLu7sweJT1s43o6T" ^
  -d "client_secret=21B846B99558FB886D0590924D656B5CBE37F8FF5AF794BD869AAB2DA27EF012" ^
  -d "username=prafulla.vispute573@agentforce.com" ^
  -d "password=Prachit@123pScnAYjGaV5WHY6EIWlOZUuBE"


python .\ui\main.py

https://orgfarm-1fb703dbbe-dev-ed.develop.my.salesforce.com/?ec=302&startURL=%2F00Q%2Fo
prafulla.vispute573@agentforce.com/Prachit@123

Add a new lead named Michael Thompson from ClearPath Consulting. His email is michael.thompson@clearpathco.com.

 Example 2:
Create a Salesforce lead for Sophia Miller, who works at BrightWave Media. Her email address is sophia.miller@brightwavemedia.com.

Please create a lead:
Name: Jason Lee
Company: Vertex Dynamics
Email: jason.lee@vertexdynamics.com