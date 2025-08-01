from src.services.http.dto.query_dto import UserQuery
from fastapi import FastAPI
from src.containers import AppContainer

container = AppContainer()
container.wire(modules=[__name__])
import src.services.mcp.server

app = FastAPI()

@app.get("/ping")
def ping():
    return "pong"

@app.post("/query")
async def user_query(data: UserQuery):
    orchestrator = container.orchestrator()
    return await orchestrator.run(data.query)

