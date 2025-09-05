from typing import Annotated, TypedDict
from langchain_core import messages
from langgraph.graph import MessagesState, StateGraph, START, END
from langgraph.graph.message import add_messages
from langchain_core.tools import tool
from llm_model import call_model
from langgraph.prebuilt import create_react_agent
from langchain_experimental.utilities import PythonREPL
from langchain_core.messages import HumanMessage
import matplotlib
matplotlib.use('Agg')  # Use non-GUI backend to prevent NSException
import matplotlib.pyplot as plt

from dotenv import load_dotenv

load_dotenv()

class State(TypedDict):
    messages: Annotated[list, add_messages]

repl = PythonREPL()

@tool
def python_repl_tool(code: str):
    """Use this to execute python code. If you want to see the output of a value,
    you should print it out with `print(...)`. This is visible to the user."""
    try:
        # Ensure matplotlib uses non-GUI backend in executed code
        if 'matplotlib' in code and 'matplotlib.use(' not in code:
            code = "import matplotlib\nmatplotlib.use('Agg')\n" + code
        result = repl.run(code)
    except BaseException as e:
        return f"Failed to execute. Error: {repr(e)}"
    result_str = f"Successfully executed:\n```python\n{code}\n```\nStdout: {result}"
    return (
        result_str + "\n\nIf you have completed all tasks, respond with FINAL ANSWER. Focus on what was accomplished, not the code details."
    )


def make_system_prompt(suffix: str) -> str:
    return (
        "You are a helpful AI assistant that can answer questions and help with tasks."
        f"\n{suffix}"
    )



tools = [python_repl_tool]

code_generator_agent = create_react_agent(
    call_model,
    tools,
    prompt=make_system_prompt(
        """You are an expert Python code generator and problem solver. Your role is to:

1. **Understand Requirements**: Carefully analyze user requests and break down complex problems into manageable steps.

2. **Generate Clean Code**: Write well-structured, readable, and efficient Python code that follows best practices:
   - Use meaningful variable and function names
   - Add appropriate comments for complex logic
   - Follow PEP 8 style guidelines
   - Include proper error handling when necessary

3. **Execute and Validate**: Use the python_repl_tool to run your code and verify it works correctly:
   - Test your code with sample inputs
   - Debug any errors that occur
   - Iterate and improve the solution

4. **Explain Your Approach**: Provide clear explanations of:
   - The logic behind your solution
   - Any algorithms or techniques used
   - Key assumptions made

5. **Handle Edge Cases**: Consider and address potential edge cases or error conditions.

When writing code:
- Start with a clear plan or pseudocode if the problem is complex
- Use appropriate data structures and algorithms
- Optimize for readability first, then performance if needed
- Include docstrings for functions when appropriate
- Test your code thoroughly before presenting the final solution

6. **Create Visualizations**: Create graphs and charts using Python/matplotlib when appropriate. 
   - Always use matplotlib.use('Agg') for non-GUI backend to prevent display issues
   - Save plots to files using plt.savefig() instead of plt.show()
   - Use descriptive filenames for saved plots

Always use the python_repl_tool to execute and verify your code works as expected. 

**Important**: When creating plots or charts:
- Execute the code to generate the actual plot files
- Focus on the results and outcomes, not the code itself
- In your FINAL ANSWER, describe what was accomplished and where files were saved
- Do NOT include the full code in your final response unless specifically requested

When you have completed all tasks and verified the solution works correctly, respond with FINAL ANSWER."""
    ),
)


def agent_node(state: State):
    result = code_generator_agent.invoke(state)
    return {"messages": result["messages"]}

graph = StateGraph(State)

graph.add_node("agent_node", agent_node)

graph.add_edge(START, "agent_node")
graph.add_edge("agent_node", END)
 


graph = graph.compile()

# Safely generate Mermaid diagram
try:
    graph.get_graph().draw_mermaid_png(output_file_path="langgraph_diagram7.png")
    print("Mermaid diagram generated successfully: langgraph_diagram7.png")
except Exception as e:
    print(f"Warning: Could not generate Mermaid diagram: {e}")
    print("Continuing without diagram generation...")


# invoke the graph
try:
    result = graph.invoke({"messages": [HumanMessage(content="Create a line chart showing the top 5 asian countries by population. Get the data from the internet. Save it as a PNG file under folder png_files.")]})
    print("Graph execution completed successfully!")
    print("Final result: ", result["messages"][-1].content)
except Exception as e:
    print(f"Error during graph execution: {e}")
    print("This might be due to API issues, network problems, or other runtime errors.")