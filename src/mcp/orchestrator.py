from src.mcp.client import mcp_client_list_all, run_action
from src.utils.prompt.prompt_builder import build_main_prompt
from src.llm.gemini import GeminiClient
from src.utils.parser.llm_response_parser import parse_llm_response

gemini = GeminiClient()
async def run_user_query(query: str):
  resources = await mcp_client_list_all()
  
  prompt = build_main_prompt(query, resources["tools"])
  llm_response = await gemini.generate(prompt)
  response_object = parse_llm_response(llm_response)

  tool, params = response_object["tool"], response_object["args"]
  return await run_action(tool, params) if response_object["tool"] != "unknown" else response_object
