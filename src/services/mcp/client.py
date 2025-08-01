from fastmcp import Client
from src.registry.registry import mcp

async def mcp_client_list_all() -> dict:
  async with Client(mcp) as client:
    tools = await client.list_tools()
    resources = await client.list_resources()
    return {
      "tools": tools,
      "resources": resources
    }
  
async def run_action(tool_name: str, params: dict):
  async with Client(mcp) as client:
    return await client.call_tool(tool_name, params)
    
