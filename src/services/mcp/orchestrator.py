from src.services.mcp.client import mcp_client_list_all, run_action
from src.utils.prompt.prompt_builder import PromptBuilder
from src.services.llm.gemini import GeminiClient
from src.services.conversation_memory.memory import ConversationMemory

class MCPOrchestrator:
  def __init__(self, model: GeminiClient, prompt: PromptBuilder, memory: ConversationMemory):
    self.llm = model
    self.prompt = prompt
    self.memory = memory

  async def run(self, query: str):
    resources = await mcp_client_list_all()    

    memo = await self.memory.load()
    prompt = self.prompt.build_main_prompt(query, resources["tools"], memo)
    llm_response = await self.llm.generate(prompt)
    
    response_object = self.prompt.parse_llm_response(llm_response)

    tool, params = response_object["tool"], response_object["args"]
    action = await run_action(tool, params) if response_object["tool"] != "unknown" else response_object

    self.memory.save(query, str(action.data))
    return action