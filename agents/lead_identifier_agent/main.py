# main.py
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../tools')))

from google.adk.agents import BaseAgent 
from tools.detect_lead import detect_lead

class LeadIdentifierAgent(BaseAgent):
    def __init__(self):
        super().__init__(name="lead_identifier_agent")
    
    async def run(self, content: str) -> dict:
        print(f"[LeadIdentifierAgent] Analyzing text content...")
        lead_info = detect_lead(content)
        return lead_info

if __name__ == '__main__':
    import asyncio
    agent = LeadIdentifierAgent()
    sample_text = "Hi, this is Sarah from XYZ Corp. We're interested in your product and would love a demo."
    result = asyncio.run(agent.run(sample_text))
    print("[Agent Output]", result)
