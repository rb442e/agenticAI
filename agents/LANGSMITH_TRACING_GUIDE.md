# LangSmith Tracing Setup Guide

This guide shows how to set up and use LangSmith tracing for your AI agents across different frameworks.

## Prerequisites

You mentioned you've already set these environment variables:
- `LANGSMITH_API_KEY` - Your LangSmith API key
- `LANGSMITH_TRACING=true` - Enables tracing

## Core Setup

### 1. Required Environment Variables

Add these to your `.env` file or environment:

```bash
# Required
LANGSMITH_API_KEY=your_api_key_here
LANGSMITH_TRACING=true

# Optional but recommended
LANGSMITH_PROJECT=your_project_name  # Organizes traces by project
LANGSMITH_ENDPOINT=https://api.smith.langchain.com  # Default endpoint
```

### 2. Python Configuration

For any Python script using LangChain/LangGraph, add this at the beginning:

```python
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure LangSmith tracing (if not set in .env)
os.environ["LANGSMITH_TRACING"] = "true"
os.environ["LANGSMITH_ENDPOINT"] = "https://api.smith.langchain.com"

# Set project name for organizing traces
if not os.environ.get("LANGSMITH_PROJECT"):
    os.environ["LANGSMITH_PROJECT"] = "your-project-name"
```

## Framework-Specific Examples

### 1. LangGraph (Your Current Setup)

Your `langgraph_demo/main.py` is now properly configured. The tracing will automatically capture:
- Agent reasoning steps
- Tool calls (triple_number, db_connect)
- Message flows between nodes
- State transitions

Example output will show traces for:
1. Initial user message
2. Agent reasoning
3. Tool selection and execution
4. Final response

### 2. OpenAI SDK Direct Usage

```python
import os
from langsmith import traceable
from openai import OpenAI

# Your existing Azure OpenAI setup
client = OpenAI(
    api_key=os.getenv("OPEN_API_KEY"),
    base_url=os.getenv("BASE_URL")
)

@traceable  # This decorator enables tracing
def chat_completion(messages, model="gpt-4"):
    return client.chat.completions.create(
        model=model,
        messages=messages
    )
```

### 3. CrewAI (For your crew projects)

```python
import os
from crewai import Agent, Task, Crew

# Set environment variables as shown above

# Your existing crew setup will automatically trace
agent = Agent(
    role='Researcher',
    goal='Research topics thoroughly',
    backstory='You are a research expert...',
    # LangSmith will automatically trace all agent interactions
)
```

### 4. AutoGen

```python
import os
import autogen

# Set environment variables as shown above

# Your existing autogen setup will trace automatically
config_list = autogen.config_list_from_env(
    filter_dict={"model": ["gpt-4"]}
)

# All agent conversations will be traced
```

## Running Your LangGraph Demo with Tracing

1. Make sure your `.env` file has the required variables
2. Run your demo:

```bash
cd /Users/a112932/Documents/projects/agents/langgraph_demo
python main.py
```

3. Check LangSmith dashboard at https://smith.langchain.com for traces

## What You'll See in LangSmith

### Trace Information
- **Run Name**: Automatically generated or custom named
- **Input/Output**: User queries and agent responses  
- **Duration**: How long each step took
- **Tokens Used**: Token consumption for each LLM call
- **Errors**: Any exceptions or failures

### Detailed Views
- **Timeline**: Visual representation of execution flow
- **Tree View**: Hierarchical view of nested calls
- **Logs**: Detailed logging information
- **Metadata**: Model parameters, temperatures, etc.

## Advanced Features

### 1. Custom Trace Names

```python
from langsmith import traceable

@traceable(name="custom_research_task")
def research_function(query):
    # Your code here
    pass
```

### 2. Adding Metadata

```python
from langsmith import Client

client = Client()

# Add tags and metadata to traces
with client.trace(name="research_session", tags=["research", "demo"]):
    result = your_agent_function()
```

### 3. Custom Feedback and Scores

```python
# Add feedback to traces
client.create_feedback(
    run_id=trace_id,
    key="helpfulness",
    score=0.8,
    comment="Very helpful response"
)
```

## Troubleshooting

### Common Issues

1. **No traces appearing**:
   - Check API key is correct
   - Verify `LANGSMITH_TRACING=true` is set
   - Ensure you're using supported LangChain versions

2. **Missing project organization**:
   - Set `LANGSMITH_PROJECT` environment variable
   - Different projects help organize traces

3. **Incomplete traces**:
   - Make sure all LLM calls go through LangChain/supported libraries
   - Direct API calls need `@traceable` decorator

4. **Rate limiting**:
   - LangSmith has rate limits on free tier
   - Check your plan limits

### Testing Your Setup

Run this simple test script:

```python
import os
from dotenv import load_dotenv
from langchain_openai import AzureChatOpenAI

load_dotenv()

# Configure tracing
os.environ["LANGSMITH_TRACING"] = "true"
os.environ["LANGSMITH_PROJECT"] = "test-tracing"

# Your existing model setup
llm = AzureChatOpenAI(
    deployment_name=os.getenv("DEPLOYMENT_NAME"),
    openai_api_key=os.getenv("OPEN_API_KEY"),
    openai_api_version=os.getenv("API_VERSION"),
    azure_endpoint=os.getenv("BASE_URL"),
    temperature=0
)

# This should create a trace
response = llm.invoke("Hello, this is a test message for tracing!")
print(response.content)
```

## Next Steps

1. **Run your LangGraph demo** - It's already configured
2. **Check LangSmith dashboard** - Look for traces under "langgraph-demo" project
3. **Explore other projects** - Apply similar configuration to your other agent projects
4. **Set up monitoring** - Use LangSmith for production monitoring and debugging

## Dashboard Access

Visit https://smith.langchain.com to view your traces, analytics, and manage projects.
