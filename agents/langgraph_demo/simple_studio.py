#!/usr/bin/env python3
"""
Simple LangGraph Studio Interface

This provides a basic web interface to visualize and test your multi-agent workflow
since the langgraph CLI studio might not be available.
"""

import json
import asyncio
from typing import Dict, Any
from datetime import datetime
import gradio as gr
from langgraph_studio import graph, web_search_tool, python_repl_tool

class SimpleLangGraphStudio:
    def __init__(self):
        self.graph = graph
        self.execution_history = []
        
    def execute_workflow(self, user_input: str) -> str:
        """Execute the workflow with user input"""
        try:
            print(f"🚀 Executing workflow with input: {user_input}")
            
            # Execute the graph
            events = self.graph.stream(
                {
                    "messages": [
                        ("user", user_input)
                    ],
                },
                {"recursion_limit": 150},
            )
            
            # Collect execution steps
            execution_steps = []
            for event in events:
                step_info = {
                    "timestamp": datetime.now().isoformat(),
                    "event": str(event),
                    "node": list(event.keys())[0] if event else "unknown"
                }
                execution_steps.append(step_info)
                self.execution_history.append(step_info)
            
            # Format the output
            output = f"✅ Workflow executed successfully!\n\n"
            output += f"📝 User Input: {user_input}\n\n"
            output += f"🔄 Execution Steps ({len(execution_steps)} steps):\n"
            
            for i, step in enumerate(execution_steps, 1):
                output += f"\n{i}. {step['node']} at {step['timestamp']}\n"
                output += f"   Details: {step['event'][:200]}...\n"
            
            return output
            
        except Exception as e:
            error_msg = f"❌ Error executing workflow: {str(e)}"
            print(error_msg)
            return error_msg
    
    def get_workflow_info(self) -> str:
        """Get information about the workflow structure"""
        try:
            # Get the graph structure
            graph_info = self.graph.get_graph()
            
            info = "📊 Multi-Agent Workflow Information\n"
            info += "=" * 50 + "\n\n"
            
            info += "🏗️ Workflow Structure:\n"
            info += f"   - Start Node: START\n"
            info += f"   - End Node: END\n"
            info += f"   - Total Nodes: {len(graph_info.nodes)}\n\n"
            
            info += "🤖 Agents:\n"
            info += "   1. Researcher Agent\n"
            info += "      - Role: Gathers information from the web\n"
            info += "      - Tools: Web search (Tavily)\n"
            info += "      - Behavior: Searches for data, never creates charts\n\n"
            
            info += "   2. Chart Generator Agent\n"
            info += "      - Role: Creates visualizations from data\n"
            info += "      - Tools: Python code execution\n"
            info += "      - Behavior: Generates charts, marks tasks complete\n\n"
            
            info += "🔄 Workflow Flow:\n"
            info += "   START → Researcher → Chart Generator → END\n\n"
            
            info += "🛠️ Available Tools:\n"
            info += "   - web_search_tool: Search the web for information\n"
            info += "   - python_repl_tool: Execute Python code and create charts\n\n"
            
            info += "💡 Example Prompts:\n"
            info += "   - 'Get UK GDP data and create a chart'\n"
            info += "   - 'Research AI trends and visualize them'\n"
            info += "   - 'Find stock data for Apple and create a graph'\n"
            
            return info
            
        except Exception as e:
            return f"❌ Error getting workflow info: {str(e)}"
    
    def get_execution_history(self) -> str:
        """Get the execution history"""
        if not self.execution_history:
            return "📝 No executions yet. Run a workflow first!"
        
        output = f"📝 Execution History ({len(self.execution_history)} executions)\n"
        output += "=" * 50 + "\n\n"
        
        for i, execution in enumerate(self.execution_history, 1):
            output += f"Execution {i}:\n"
            output += f"  Time: {execution['timestamp']}\n"
            output += f"  Node: {execution['node']}\n"
            output += f"  Details: {execution['event'][:100]}...\n\n"
        
        return output
    
    def test_tools(self) -> str:
        """Test the individual tools"""
        output = "🧪 Testing Individual Tools\n"
        output += "=" * 30 + "\n\n"
        
        # Test web search tool
        try:
            search_result = web_search_tool.invoke("test query")
            output += "✅ Web Search Tool: Working\n"
        except Exception as e:
            output += f"❌ Web Search Tool: Failed - {str(e)}\n"
        
        # Test Python REPL tool
        try:
            python_result = python_repl_tool.invoke("print('Hello, World!')")
            output += "✅ Python REPL Tool: Working\n"
        except Exception as e:
            output += f"❌ Python REPL Tool: Failed - {str(e)}\n"
        
        return output

def create_interface():
    """Create the Gradio interface"""
    studio = SimpleLangGraphStudio()
    
    with gr.Blocks(title="LangGraph Studio - Multi-Agent Workflow", theme=gr.themes.Soft()) as interface:
        gr.Markdown("# 🚀 LangGraph Studio - Multi-Agent Workflow")
        gr.Markdown("Visualize and test your multi-agent collaboration workflow")
        
        with gr.Tab("🎯 Execute Workflow"):
            gr.Markdown("### Run your multi-agent workflow")
            user_input = gr.Textbox(
                label="User Input",
                placeholder="Enter your request (e.g., 'Get UK GDP data and create a chart')",
                lines=3
            )
            execute_btn = gr.Button("🚀 Execute Workflow", variant="primary")
            output = gr.Textbox(label="Execution Results", lines=15, max_lines=20)
            
            execute_btn.click(
                fn=studio.execute_workflow,
                inputs=[user_input],
                outputs=[output]
            )
        
        with gr.Tab("📊 Workflow Info"):
            gr.Markdown("### Workflow structure and information")
            info_btn = gr.Button("📋 Get Workflow Info", variant="secondary")
            info_output = gr.Markdown()
            
            info_btn.click(
                fn=studio.get_workflow_info,
                outputs=[info_output]
            )
        
        with gr.Tab("📝 Execution History"):
            gr.Markdown("### View execution history")
            history_btn = gr.Button("📚 View History", variant="secondary")
            history_output = gr.Textbox(label="Execution History", lines=15, max_lines=20)
            
            history_btn.click(
                fn=studio.get_execution_history,
                outputs=[history_output]
            )
        
        with gr.Tab("🧪 Tool Testing"):
            gr.Markdown("### Test individual tools")
            test_btn = gr.Button("🔧 Test Tools", variant="secondary")
            test_output = gr.Textbox(label="Tool Test Results", lines=10, max_lines=15)
            
            test_btn.click(
                fn=studio.test_tools,
                outputs=[test_output]
            )
        
        with gr.Tab("💡 Examples"):
            gr.Markdown("### Example prompts to try")
            examples = [
                "Get UK GDP data for the past 5 years and create a line chart",
                "Research the latest AI trends and create a summary visualization",
                "Find stock market data for Apple and create a price chart",
                "Get weather data for London and show temperature trends",
                "Research renewable energy adoption and create a bar chart"
            ]
            
            for example in examples:
                gr.Markdown(f"• **{example}**")
        
        gr.Markdown("---")
        gr.Markdown("**💡 Tip**: Start with the 'Execute Workflow' tab to test your multi-agent system!")
    
    return interface

if __name__ == "__main__":
    print("🚀 Starting Simple LangGraph Studio...")
    print("📱 This will open a web interface in your browser")
    print("🌐 You can visualize and test your multi-agent workflow")
    
    # Create and launch the interface
    interface = create_interface()
    interface.launch(
        server_name="0.0.0.0",
        server_port=7860,
        share=False,
        show_error=True
    )
