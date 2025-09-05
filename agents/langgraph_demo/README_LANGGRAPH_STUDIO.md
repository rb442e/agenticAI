# LangGraph Studio Setup Guide

This guide will help you set up and use LangGraph Studio to visualize and debug your multi-agent collaboration workflow.

## 🚀 What is LangGraph Studio?

LangGraph Studio is a web-based interface that allows you to:
- **Visualize** your LangGraph workflows in real-time
- **Debug** each step of your multi-agent conversations
- **Monitor** tool usage and agent interactions
- **Trace** the flow of information between agents
- **Test** different inputs and see how your graph responds

## 📋 Prerequisites

You already have everything you need! Your project includes:
- ✅ `langgraph-sdk` (already installed)
- ✅ `langchain-anthropic` for the LLM
- ✅ `langchain-tavily` for web search
- ✅ `langchain-experimental` for Python code execution

## 🎯 Quick Start

### Option 1: Use the Startup Script (Recommended)
```bash
cd agents/langgraph_demo
./start_studio.sh
```

### Option 2: Manual Start
```bash
cd agents/langgraph_demo
langgraph studio
```

## 🌐 What You'll See

1. **Terminal Output**: LangGraph Studio will start and show you a local URL
2. **Browser Window**: Should open automatically to the studio interface
3. **Workflow Visualization**: Your multi-agent graph will be displayed

## 🔍 Understanding Your Workflow

Your multi-agent system has two main agents:

### 1. **Researcher Agent** 🔍
- **Role**: Gathers information from the web
- **Tools**: Web search tool (Tavily)
- **Behavior**: Searches for data, never creates charts

### 2. **Chart Generator Agent** 📊
- **Role**: Creates visualizations from data
- **Tools**: Python code execution tool
- **Behavior**: Generates charts, marks tasks as complete

## 🎮 How to Use LangGraph Studio

### **Step 1: Start the Studio**
```bash
./start_studio.sh
```

### **Step 2: Navigate the Interface**
- **Graph View**: See your workflow structure
- **Execution Panel**: Run your graph with different inputs
- **Trace View**: Step through each execution
- **Tool Usage**: Monitor which tools are called

### **Step 3: Test Your Workflow**
1. Enter a test prompt like: *"Get UK GDP data and create a chart"*
2. Watch the agents work together
3. See the flow: Researcher → Chart Generator → Complete

### **Step 4: Debug and Optimize**
- **Step-by-step execution**: See exactly what each agent does
- **Tool calls**: Monitor which tools are used and when
- **Error tracking**: Identify where things go wrong
- **Performance metrics**: See execution times and token usage

## 🛠️ Advanced Features

### **Custom Inputs**
Try different prompts to test your agents:
- "Research the latest AI trends and create a summary chart"
- "Find stock market data for Apple and visualize it"
- "Get weather data for London and show temperature trends"

### **Workflow Modifications**
- Add new agents to your graph
- Modify tool configurations
- Change agent prompts and behaviors
- Add new edges and routing logic

## 🔧 Troubleshooting

### **Studio Won't Start**
```bash
# Check if langgraph CLI is available
langgraph --version

# If not found, install it
pip install langgraph-sdk
```

### **Browser Doesn't Open**
- Check the terminal for the local URL (usually `http://localhost:8123`)
- Manually open the URL in your browser

### **Graph Not Loading**
- Ensure your `langgraph_studio.py` file is in the same directory
- Check that all imports are working correctly
- Verify your API keys are set in `.env`

## 📚 Example Workflow

Here's what happens when you run: *"Get UK GDP data and create a chart"*

1. **Start** → **Researcher Agent**
   - Agent searches for "UK GDP past 5 years"
   - Gathers data from web sources
   - Passes data to Chart Generator

2. **Researcher** → **Chart Generator Agent**
   - Receives GDP data
   - Creates Python code for matplotlib
   - Generates and saves the chart
   - Marks task as complete

3. **Chart Generator** → **End**
   - Workflow completes successfully

## 🎉 Benefits of LangGraph Studio

- **Real-time Visualization**: See your agents work live
- **Debugging**: Step through each execution step
- **Performance Monitoring**: Track execution times and costs
- **Tool Usage**: Monitor which tools are most effective
- **Error Detection**: Quickly identify and fix issues
- **Workflow Optimization**: Test different configurations

## 🚀 Next Steps

1. **Start the studio** and explore the interface
2. **Test different prompts** to see how your agents respond
3. **Monitor tool usage** to optimize performance
4. **Add new agents** or modify existing ones
5. **Experiment with different workflows** and routing logic

## 📞 Need Help?

- Check the [LangGraph documentation](https://langchain-ai.github.io/langgraph/)
- Explore the [LangGraph Studio guide](https://langchain-ai.github.io/langgraph/langgraph-studio/)
- Review your agent configurations and prompts

---

**Happy debugging! 🎯✨**
