from langgraph.graph import MessagesState, StateGraph, START, END
from langchain_core.runnables.graph import MermaidDrawMethod
from typing import TypedDict
from dotenv import load_dotenv

load_dotenv()

class InputState(TypedDict):
    string_value: str
    int_value: int

def modify_state(input: InputState) -> InputState:
    input['string_value'] += "a"
    input['int_value'] += 1
    return input

def router(state: InputState) -> str:
    if state['int_value'] < 5:
        return "node_1"
    else:
        return END

def main():
    print("Langraph Basic Demo Started")
    
    # Initialize the graph
    graph = StateGraph(InputState)

    # Add nodes
    graph.add_node("node_1", modify_state)
    graph.add_node("node_2", modify_state)

    # Add edges
    graph.add_edge(START, "node_1")
    graph.add_edge("node_1", "node_2")
    graph.add_edge("node_2", END)

    # Set the entry point
    graph.set_entry_point("node_1")

    # Add conditional edges
    graph.add_conditional_edges("node_2", router, {
        "node_1": "node_1",
        "__end__": END
    })

    # Compile the graph
    app = graph.compile()

    # Generate and save diagram
    app.get_graph().draw_mermaid_png(
        draw_method=MermaidDrawMethod.PYPPETEER, 
        output_file_path="langgraph_diagram1.png"
    )
    print("Graph diagram saved as 'langgraph_diagram1.png'")

    # Run the graph
    result = app.invoke({"string_value": "a", "int_value": 1})
    print(result)

if __name__ == "__main__":
    main()
    print("Langraph Basic Demo Completed")