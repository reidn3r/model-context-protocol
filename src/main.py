from fastapi import FastAPI
from src.mcp.orchestrator import run_user_query
from src.models.query import UserQuery

app = FastAPI()
@app.get("/ping")
def ping():
    return "pong"

@app.post("/query")
async def user_query(data: UserQuery):
    return await run_user_query(data.query)
