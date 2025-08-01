from fastmcp.tools import Tool
import json
import re

class PromptBuilder:
  def build_main_prompt(self, query: str, tools: list[Tool]):
    return f'''
    Você é um assistente que analisa mensagens de usuários e determina qual ação executar.
    As possíveis tarefas são: Calcular áreas de figuras geométricas específicas.
    Ferramentas Disponíveis:
    {tools}

    Mensagem do usuário: ${query}
    
    Responda APENAS com um JSON no seguinte formato:
    {{
      "action": {[t.name for t in tools]},
      "parameters": {{
        // parâmetros necessários baseados na ação
      }}
    }}
    
    Se o usuário nao informar todos os dados requeridos para executar a ação, use:
    {{
      "action": "discover",
      "parameters: {{
        "message": // parâmetros necessários para executar ação
      }}
    }}
    
    Se não conseguir determinar a ação, use:
    {{
      "action": "unknown",
      "parameters": {{}}
    }}
    '''
  
  def parse_llm_response(self, response: str) -> dict:
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

