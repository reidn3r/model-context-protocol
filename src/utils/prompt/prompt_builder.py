from fastmcp.tools import Tool
import json
import re

class PromptBuilder:
  def build_main_prompt(self, query: str, tools: list[Tool], memory: dict):
    return f'''
      Você é um assistente inteligente que analisa mensagens de usuários e determina qual ação executar.

      HISTÓRICO DA CONVERSA:
      {memory}

      FERRAMENTAS DISPONÍVEIS:
      {tools}

      MENSAGEM ATUAL DO USUÁRIO: {query}

      INSTRUÇÕES:
      1. Considere o histórico da conversa para entender o contexto
      2. Se o usuário se referir a algo mencionado anteriormente, use essa informação
      3. Analise a mensagem atual e determine a melhor ação a executar

      Responda APENAS com um JSON no seguinte formato:
      {{
        "action": "{tools}",
        "parameters": {{
          // parâmetros necessários baseados na ação escolhida
        }},
        "reasoning": "Breve explicação da escolha baseada no contexto"
      }}

      Se o usuário não informar todos os dados requeridos, use:
      {{
        "action": "discover",
        "parameters": {{
          "message": "Parâmetros necessários para executar a ação: [liste os parâmetros faltantes]"
        }},
        "reasoning": "Dados insuficientes fornecidos"
      }}

      Se não conseguir determinar a ação, use:
      {{
        "action": "unknown",
        "parameters": {{}},
        "reasoning": "Não foi possível determinar a ação adequada"
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

