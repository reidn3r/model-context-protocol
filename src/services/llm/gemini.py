from google import genai
from config.envs import envsConfig

class GeminiClient:
  def __init__(self):
    self.model = genai.Client(api_key=envsConfig["GEMINI_KEY"])

  async def generate(self, prompt:str) -> str:
    response = await self.model.aio.models.generate_content(
        model=envsConfig["GEMINI_MODEL"],
        contents=prompt,
        config=genai.types.GenerateContentConfig(
          temperature=0,
        ),
    )
    return response.text
