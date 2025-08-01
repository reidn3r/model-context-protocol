from src.services.mcp.client import mcp_client_list_all, run_action
from src.utils.prompt.prompt_builder import PromptBuilder
from src.services.llm.gemini import GeminiClient

class MCPOrchestrator:
  def __init__(self, model: GeminiClient, prompt: PromptBuilder):
    self.llm = model
    self.prompt = prompt

  async def run(self, query: str):
    resources = await mcp_client_list_all()    
    prompt = self.prompt.build_main_prompt(query, resources["tools"])
    llm_response = await self.llm.generate(prompt)
    response_object = self.prompt.parse_llm_response(llm_response)


    tool, params = response_object["tool"], response_object["args"]
    return await run_action(tool, params) if response_object["tool"] != "unknown" else response_object
