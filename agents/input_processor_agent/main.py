# main.py
from google.adk.agents import BaseAgent 
from tools.parse_input import parse_input
class InputProcessorAgent(BaseAgent):
    def __init__(self):
        super().__init__(name="input_processor_agent")
    async def run(self, input_type: str, data: str) -> dict:
        print(f"[InputProcessorAgent] Processing {input_type} input...")
        parsed = parse_input(input_type, data)
        return parsed
  
if __name__ == '__main__':
    import asyncio
    agent = InputProcessorAgent()
    result = asyncio.run(agent.run("text", "Customer John from Acme Corp is interested."))
    print("[Agent Output]", result)