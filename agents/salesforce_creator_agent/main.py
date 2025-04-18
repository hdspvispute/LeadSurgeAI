# main.py
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../tools')))

from google.adk.agents import BaseAgent 
from tools.create_salesforce_lead import create_salesforce_lead

class SalesforceCreatorAgent(BaseAgent):
    def __init__(self):
        super().__init__(name="salesforce_creator_agent")

    async def run(self, name: str, company: str, email: str) -> dict:
        print(f"[SalesforceCreatorAgent] Creating lead for {name}...")
        response = create_salesforce_lead(name, company, email)
        return {"status": "success", "details": response}

if __name__ == '__main__':
    import asyncio
    agent = SalesforceCreatorAgent()
    result = asyncio.run(agent.run("Sarah", "XYZ Corp", "sarah@xyzcorp.com"))
    print("[Agent Output]", result)
