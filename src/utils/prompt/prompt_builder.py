from fastmcp.tools import Tool

def build_main_prompt(query: str, tools: list[Tool]):
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

  Se não conseguir determinar a ação, use:
  {{
    "action": "unknown",
    "parameters": {{}}
  }}
  '''
