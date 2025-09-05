
import os
from dotenv import load_dotenv
from langchain_core.messages import HumanMessage
from langgraph.graph import MessagesState, StateGraph, START, END
from nodes import run_agent_reasoning, tool_node

# Load environment variables
load_dotenv()


AGENT_REASON="agent_reason"
ACT="act"
LAST= -1

def should_continue(state: MessagesState) -> str:
    """Should continue"""
    last_message = state["messages"][LAST]
    if hasattr(last_message, 'tool_calls') and last_message.tool_calls:
        return ACT
    else:
        return END

flow = StateGraph(MessagesState)

flow.add_node(AGENT_REASON, run_agent_reasoning)
flow.set_entry_point(AGENT_REASON)
flow.add_node(ACT, tool_node)

flow.add_conditional_edges(AGENT_REASON, should_continue, {
    ACT: ACT,
    END: END    
    })

# Add edge from ACT back to AGENT_REASON to continue the loop
flow.add_edge(ACT, AGENT_REASON)

app = flow.compile()
# app.get_graph().draw_mermaid_png(output_file_path="flow.png", draw_method=MermaidDrawMethod.PYPPETEER)

def main():
    print("Starting LangGraph Agent Demo...")
    
    # Example conversation
    user_input = "Get the data from the database and use that number as input to the triple_number tool to get the result."
    
    # Create initial state
    initial_state = {
        "messages": [HumanMessage(content=user_input)]
    }
    
    # Run the graph
    print(f"User: {user_input}")
    print("Agent is thinking and acting...")
    
    result = app.invoke(initial_state)
    
    # Print the final response
    if result["messages"]:
        final_message = result["messages"][-1]
        print(f"Assistant: {final_message.content}")
    
    print("Demo completed!")



if __name__ == "__main__":
    main()
