from test_graph import graph, State
from langchain_core.messages import HumanMessage

def test_code_generation():
    """Test how the agent uses the python_repl_tool with code parameter"""
    
    # Example 1: Simple math calculation
    print("=== Test 1: Simple Math ===")
    result = graph.invoke({
        "messages": [HumanMessage(content="Calculate the sum of numbers from 1 to 10")]
    })
    print("Final message:", result["messages"][-1].content)
    print()
    
    # Example 2: Data processing
    print("=== Test 2: Data Processing ===")
    result = graph.invoke({
        "messages": [HumanMessage(content="Create a list of squares of numbers from 1 to 5 and print them")]
    })
    print("Final message:", result["messages"][-1].content)
    print()
    
    # Example 3: Function creation
    print("=== Test 3: Function Creation ===")
    result = graph.invoke({
        "messages": [HumanMessage(content="Write a function to check if a number is prime and test it with number 17")]
    })
    print("Final message:", result["messages"][-1].content)

if __name__ == "__main__":
    test_code_generation()
