from langgraph.prebuilt import create_react_agent

from langchain_tavily import TavilySearch
from langchain_core.tools import tool
from llm_model import call_model

import asyncio

from datetime import datetime

# Tool for searching the web
tavily_search_tool = TavilySearch(max_results=5)

@tool
async def web_search_tool(query: str):
    """Use this to search the web for current information. Keep queries simple and avoid date parameters."""
    try:
        results = tavily_search_tool.invoke({"query": query})
        return await results
    except Exception as e:
        return await f"Search failed: {str(e)}"

# Tools
tools = [web_search_tool]

# Get the current date
today = datetime.now().strftime("%Y-%m-%d")

system_prompt = f"""
You are a helpful assistant that can search the web for current information.
You are given a task to search the web for current information.
You are also given a date to search the web for current information.
You are also given a query to search the web for current information.
"""



graph = create_react_agent(model=call_model, tools=tools)

# graph.draw_mermaid_png(output_file_path="langgraph_diagram3.png")

graph.invoke({"query": "What are the latest AI courses available in MIT University?"})