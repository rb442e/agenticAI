from langchain_core.messages import SystemMessage
from langgraph.graph import MessagesState
from langgraph.prebuilt import ToolNode
from react import tools, llm

SYSTEM_MESSAGE = """
You are a helpful assistant that can answer questions and help with tasks.
"""

def run_agent_reasoning(state: MessagesState) -> MessagesState:
    """ Run the reasoning agent """
    
    messages = [SystemMessage(content=SYSTEM_MESSAGE)] + state["messages"]
    
    response = llm.invoke(messages)
    return {"messages": [response]}

def run_tool_agent(state: MessagesState) -> MessagesState:
    """ Run the tool agent """
    # This function is not needed since we use ToolNode directly
    pass

tool_node = ToolNode(tools)
   


