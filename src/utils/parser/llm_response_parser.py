import json
import re

def parse_llm_response(response: str) -> dict:
  try:
    # Remove blocos de código .md, ex: ```json ... ```
    match = re.search(r"```(?:json)?\s*([\s\S]+?)\s*```", response)
    if match:
        response = match.group(1).strip()

    data = json.loads(response)
    tool_name = data["action"]
    args = data["parameters"]

    return {
        "tool": tool_name,
        "args": args
    }
  except Exception as e:
    return {"error": f"Erro ao interpretar resposta da LLM: {response}"}
