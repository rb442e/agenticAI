from langgraph.graph import MessagesState, StateGraph, START, END
from langchain_core.runnables.graph import MermaidDrawMethod
from pydantic import BaseModel
from dotenv import load_dotenv

load_dotenv()

class inputState(BaseModel):
    name: str
    age: int


def welcome_node(state: inputState) -> inputState:
    return inputState(name=state.name, age=state.age)

def goodbye_node(state: inputState) -> inputState:
    return inputState(name=state.name, age=state.age)


def main():
    print("Langraph Basic Demo Started")
    
    # Initialize the graph
    graph = StateGraph(inputState)

    # Add node
    graph.add_node("node_1", welcome_node)
    graph.add_node("node_2", goodbye_node)

    # Add edge
    graph.add_edge(START, "node_1")
    graph.add_edge("node_1", "node_2")
    graph.add_edge("node_2", END)

    # Set the entry point
    graph.set_entry_point("node_1")

    # Compile the graph
    app = graph.compile()

    # app.get_graph().draw_mermaid_png(draw_method=MermaidDrawMethod.PYPPETEER, output_file_path="langgraph_diagram.png")
    print("Graph diagram saved as 'langgraph_diagram.png'")

    # Run the graph
    result = app.invoke({"name": "John", "age": 30})
    # print(result)
    result = app.invoke({"name": "Prince", "age": 80})
    print(result)

if __name__ == "__main__":
    main()
    print("Langraph Basic Demo Completed")