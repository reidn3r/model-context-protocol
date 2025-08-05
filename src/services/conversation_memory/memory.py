from langchain.memory import ConversationBufferMemory

class ConversationMemory:
  def __init__(self):
    self.memory = ConversationBufferMemory(memory_key="backoffice_history", return_messages=False)

  def save(self, input: str, output: any) -> None:
    self.memory.save_context({"input": input}, {"output": output})
  
  async def load(self) -> dict:
    data = await self.memory.aload_memory_variables({})
    return data.get('backoffice_history', {})
