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
import streamlit as st
import os
import glob
from PIL import Image

from dotenv import load_dotenv

load_dotenv()

class State(TypedDict):
    messages: Annotated[list, add_messages]
    generated_files: list  # Track generated image files

repl = PythonREPL()

# Global list to track generated image files
generated_image_files = []

@tool
def python_repl_tool(code: str):
    """Use this to execute python code. If you want to see the output of a value,
    you should print it out with `print(...)`. This is visible to the user."""
    global generated_image_files
    
    # Get current working directory for absolute paths
    current_dir = os.getcwd()
    
    # Get list of image files before execution (with full paths)
    image_patterns = ["*.png", "*.jpg", "*.jpeg", "*.svg"]
    before_files = set()
    for pattern in image_patterns:
        before_files.update(glob.glob(os.path.join(current_dir, pattern)))
    
    try:
        # Ensure matplotlib uses non-GUI backend in executed code
        if 'matplotlib' in code and 'matplotlib.use(' not in code:
            code = "import matplotlib\nmatplotlib.use('Agg')\n" + code
        
        # Also ensure plots are saved to current directory
        if 'plt.savefig(' in code or 'savefig(' in code:
            # Always ensure we're in the right directory and add absolute path handling
            code = f"""
import os
import matplotlib
matplotlib.use('Agg')
os.chdir('{current_dir}')
print(f"Working directory set to: {{os.getcwd()}}")
{code}
"""
            
        result = repl.run(code)
        
        # Small delay to ensure file system operations complete
        import time
        time.sleep(0.5)
        
    except BaseException as e:
        return f"Failed to execute. Error: {repr(e)}"
    
    # Get list of image files after execution to detect new files
    after_files = set()
    for pattern in image_patterns:
        after_files.update(glob.glob(os.path.join(current_dir, pattern)))
    
    new_files = after_files - before_files
    
    # Add new image files to our tracking list (store just filenames for display)
    for file_path in new_files:
        filename = os.path.basename(file_path)
        if filename not in generated_image_files:
            generated_image_files.append(filename)
    
    # Also check for any .png files that might have been created with plt.savefig
    # This is a fallback in case the file detection missed something
    if 'plt.savefig(' in code or 'savefig(' in code:
        all_png_files = glob.glob(os.path.join(current_dir, "*.png"))
        for png_file in all_png_files:
            filename = os.path.basename(png_file)
            if filename not in generated_image_files:
                # Check if file was created recently (within last 10 seconds)
                file_time = os.path.getmtime(png_file)
                import time
                if time.time() - file_time < 10:
                    generated_image_files.append(filename)
                    new_files.add(png_file)
    
    result_str = f"Successfully executed:\n```python\n{code}\n```\nStdout: {result}"
    
    if new_files:
        filenames = [os.path.basename(f) for f in new_files]
        result_str += f"\n\nGenerated image files: {filenames}"
    
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
    call_model(),
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

# # Safely generate Mermaid diagram
# try:
#     graph.get_graph().draw_mermaid_png(output_file_path="langgraph_diagram7.png")
#     print("Mermaid diagram generated successfully: langgraph_diagram7.png")
# except Exception as e:
#     print(f"Warning: Could not generate Mermaid diagram: {e}")
#     print("Continuing without diagram generation...")


# Streamlit interface
st.title("Python Developer Agent")
st.write("Ask me to create Python code, analyze data, or generate visualizations!")

# Initialize session state for generated files
if 'previous_files' not in st.session_state:
    st.session_state.previous_files = []


# Input and execution
question = st.text_input("Enter your query", key="user_input")

if question and st.button("Execute", key="execute_btn"):
    # Clear previous generated files list for this execution
    generated_image_files.clear()
    
    try:
        with st.spinner("Processing your request..."):
            result = graph.invoke({"messages": [HumanMessage(content=question)]})
        
        # Display the agent's response
        st.subheader("Agent Response:")
        st.markdown(result["messages"][-1].content)
        
        # Display only the newly generated charts/images from this execution
        if generated_image_files:
            st.subheader("Generated Visualizations:")
            current_dir = os.getcwd()
            
            for img_file in generated_image_files:
                # Create full path to the image file
                full_path = os.path.join(current_dir, img_file) if not os.path.isabs(img_file) else img_file
                
                if os.path.exists(full_path):
                    try:
                        # Display the image
                        image = Image.open(full_path)
                        st.image(image, caption=f"Generated: {img_file}", width="stretch")
                        
                        # Provide download button
                        with open(full_path, "rb") as file:
                            st.download_button(
                                label=f"Download {img_file}",
                                data=file.read(),
                                file_name=img_file,
                                mime="image/png"
                            )
                    except Exception as img_error:
                        st.error(f"Could not display image {img_file}: {img_error}")
                else:
                    st.warning(f"Generated file not found: {img_file}")
        
        # Update session state
        st.session_state.previous_files = generated_image_files.copy()
        
    except Exception as e:
        st.error(f"Error during execution: {e}")
        st.write("This might be due to API issues, network problems, or other runtime errors.")

# Display previously generated files if any exist
if st.session_state.previous_files:
    with st.expander("Previously Generated Files"):
        current_dir = os.getcwd()
        for img_file in st.session_state.previous_files:
            # Create full path to the image file
            full_path = os.path.join(current_dir, img_file) if not os.path.isabs(img_file) else img_file
            
            if os.path.exists(full_path):
                try:
                    image = Image.open(full_path)
                    st.image(image, caption=f"Previous: {img_file}", width="stretch")
                except Exception as img_error:
                    st.write(f"Could not display {img_file}: {img_error}")
            else:
                st.write(f"Previous file not found: {full_path}")