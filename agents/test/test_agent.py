from langchain_core.messages import HumanMessage, SystemMessage
from llm_model import call_model

messages = [SystemMessage(content="You are a helpful assistant."), HumanMessage(content="What is the capital of France?")]
response = call_model().invoke(messages)
print(response.content)