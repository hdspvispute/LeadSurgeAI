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


python .\ui\main.py

Example 1
Add a new lead named Michael Thompson from ClearPath Consulting. His email is michael.thompson@clearpathco.com.

 Example 2:
Create a Salesforce lead for Sophia Miller, who works at BrightWave Media. Her email address is sophia.miller@brightwavemedia.com.

Please create a lead:
Name: Jason Lee
Company: Vertex Dynamics
Email: jason.lee@vertexdynamics.com
