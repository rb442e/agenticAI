#!/usr/bin/env python3
"""
LangGraph Studio Setup for Multi-Agent Collaboration

This file sets up LangGraph Studio to visualize and debug your multi-agent workflow.
"""

import os
from typing import Literal
from dotenv import load_dotenv

from langchain_core.messages import BaseMessage, HumanMessage
from langchain_anthropic import ChatAnthropic
from langgraph.prebuilt import create_react_agent
from langgraph.graph import MessagesState, END, StateGraph, START
from langgraph.types import Command
from langchain_core.tools import tool
from langchain_tavily import TavilySearch
from langchain_experimental.utilities import PythonREPL

# Load environment variables
load_dotenv()

# Create a simple Tavily search tool without date conflicts
tavily_search = TavilySearch(max_results=5)

@tool
def web_search_tool(query: str):
    """Use this to search the web for current information. Keep queries simple and avoid date parameters."""
    try:
        # Use simple search without conflicting date parameters
        results = tavily_search.invoke({"query": query})
        return results
    except Exception as e:
        return f"Search failed: {str(e)}"

# Warning: This executes code locally, which can be unsafe when not sandboxed
repl = PythonREPL()

@tool
def python_repl_tool(code: str):
    """Use this to execute python code. If you want to see the output of a value,
    you should print it out with `print(...)`. This is visible to the user."""
    try:
        result = repl.run(code)
    except BaseException as e:
        return f"Failed to execute. Error: {repr(e)}"
    result_str = f"Successfully executed:\n```python\n{code}\n```\nStdout: {result}"
    return (
        result_str + "\n\nIf you have completed all tasks, respond with FINAL ANSWER."
    )

def make_system_prompt(suffix: str) -> str:
    return (
        "You are a helpful AI assistant, collaborating with other assistants."
        " Use the provided tools to progress towards answering the question."
        " If you are unable to fully answer, that's OK, another assistant with different tools "
        " will help where you left off. Execute what you can to make progress."
        " If you or any of the other assistants have the final answer or deliverable,"
        " prefix your response with FINAL ANSWER so the team knows to stop."
        f"\n{suffix}"
    )

# Initialize LLM
llm = ChatAnthropic(model="claude-3-haiku-20240307")

def get_next_node(last_message: BaseMessage, goto: str):
    if "FINAL ANSWER" in last_message.content:
        # Any agent decided the work is done
        return END
    return goto

# Research agent and node
research_agent = create_react_agent(
    llm,
    tools=[web_search_tool],
    prompt=make_system_prompt(
        "You can only do research. You are working with a chart generator colleague. "
        "Use simple search queries without date parameters to avoid conflicts. "
        "After gathering data, pass it to your colleague - do NOT create charts yourself. "
        "Never use 'FINAL ANSWER' - let the chart generator finish the task."
    ),
)

def research_node(
    state: MessagesState,
) -> Command[Literal["chart_generator", END]]:
    result = research_agent.invoke(state)
    goto = get_next_node(result["messages"][-1], "chart_generator")
    # wrap in a human message, as not all providers allow
    # AI message at the last position of the input messages list
    result["messages"][-1] = HumanMessage(
        content=result["messages"][-1].content, name="researcher"
    )
    return Command(
        update={
            # share internal message history of research agent with other agents
            "messages": result["messages"],
        },
        goto=goto,
    )

# Chart generator agent and node
chart_agent = create_react_agent(
    llm,
    [python_repl_tool],
    prompt=make_system_prompt(
        "You can only generate charts using Python/matplotlib. You are working with a researcher colleague. "
        "When you receive data, create a proper visual chart. Once the chart is complete and saved, "
        "use 'FINAL ANSWER' to indicate the task is finished."
    ),
)

def chart_node(state: MessagesState) -> Command[Literal["researcher", END]]:
    result = chart_agent.invoke(state)
    goto = get_next_node(result["messages"][-1], "researcher")
    # wrap in a human message, as not all providers allow
    # AI message at the last position of the input messages list
    result["messages"][-1] = HumanMessage(
        content=result["messages"][-1].content, name="chart_generator"
    )
    return Command(
        update={
            # share internal message history of chart agent with other agents
            "messages": result["messages"],
        },
        goto=goto,
    )

# Create the graph
workflow = StateGraph(MessagesState)
workflow.add_node("researcher", research_node)
workflow.add_node("chart_generator", chart_node)

workflow.add_edge(START, "researcher")
graph = workflow.compile()

if __name__ == "__main__":
    print("🚀 LangGraph Studio is ready!")
    print("\nTo use LangGraph Studio:")
    print("1. Run this command in your terminal:")
    print("   langgraph studio")
    print("\n2. Open your browser to the URL shown in the terminal")
    print("3. You can now visualize and debug your multi-agent workflow!")
    
    # Example of how to use the graph
    print("\n📊 Example workflow:")
    print("The graph will process: 'Get UK GDP data and create a chart'")
    
    # You can also test the graph here
    events = graph.stream(
        {
            "messages": [
                (
                    "user",
                    "First, get the UK's GDP over the past 5 years, then make a line chart of it. "
                    "Once you make the chart, finish.",
                )
            ],
        },
        {"recursion_limit": 150},
    )
    
    print("\n✅ Graph execution completed! Check the output above.")
