"""
Example showing how the code parameter is passed to the python_repl_tool
"""
from test_graph import python_repl_tool

def demonstrate_tool_usage():
    """Show direct tool usage examples"""
    
    print("=== Direct Tool Usage Examples ===\n")
    
    # Example 1: Simple calculation
    print("1. Simple Calculation:")
    code1 = """
# Calculate factorial of 5
def factorial(n):
    if n <= 1:
        return 1
    return n * factorial(n-1)

result = factorial(5)
print(f"Factorial of 5 is: {result}")
"""
    result1 = python_repl_tool(code1)
    print(result1)
    print("-" * 50)
    
    # Example 2: Data manipulation
    print("\n2. Data Manipulation:")
    code2 = """
# Work with lists and dictionaries
data = [1, 2, 3, 4, 5]
squared = [x**2 for x in data]
print(f"Original: {data}")
print(f"Squared: {squared}")

# Create a dictionary
info = {"name": "Python", "version": 3.9, "type": "language"}
for key, value in info.items():
    print(f"{key}: {value}")
"""
    result2 = python_repl_tool(code2)
    print(result2)
    print("-" * 50)
    
    # Example 3: Error handling demonstration
    print("\n3. Error Handling:")
    code3 = """
# This will cause an error
try:
    result = 10 / 0
except ZeroDivisionError as e:
    print(f"Caught error: {e}")
    result = "undefined"
    
print(f"Result: {result}")
"""
    result3 = python_repl_tool(code3)
    print(result3)

def show_agent_workflow():
    """Show how the agent would use the tool"""
    print("\n=== How the Agent Uses the Tool ===")
    print("""
    When you ask the agent to solve a problem, here's what happens:
    
    1. Agent receives your request (e.g., "Calculate fibonacci numbers")
    
    2. Agent decides to use python_repl_tool and generates code:
       python_repl_tool(code="
       def fibonacci(n):
           if n <= 1:
               return n
           return fibonacci(n-1) + fibonacci(n-2)
       
       # Test the function
       for i in range(10):
           print(f'F({i}) = {fibonacci(i)}')
       ")
    
    3. Tool executes the code and returns results
    
    4. Agent sees the output and can decide to:
       - Run more code if needed
       - Provide final answer
       - Debug if there were errors
    """)

if __name__ == "__main__":
    demonstrate_tool_usage()
    show_agent_workflow()
