from dependency_injector import containers, providers
from src.services.http.http_client import HttpClient
from src.services.llm.gemini import GeminiClient
from src.services.mcp.orchestrator import MCPOrchestrator
from src.utils.prompt.prompt_builder import PromptBuilder

class AppContainer(containers.DeclarativeContainer):
  wiring_config = containers.WiringConfiguration(packages=["src", '.'])

  http_client = providers.Singleton(HttpClient)
  prompt_builder = providers.Singleton(PromptBuilder)
  gemini_client = providers.Singleton(GeminiClient)

  orchestrator = providers.Singleton(
    MCPOrchestrator,
    model=gemini_client,
    prompt=prompt_builder,
  )