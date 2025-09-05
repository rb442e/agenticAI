from langchain_core.tools import tool
from llm_model import call_model


@tool
def triple_number(number: int) -> int:
    """Triple a number"""
    return number * 3

@tool
def db_connect() -> int:
    """Connect to a database"""
    return 15

tools = [triple_number, db_connect]

llm = call_model().bind_tools(tools)
    
