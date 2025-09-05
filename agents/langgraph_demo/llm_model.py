import os
from langchain_openai import AzureChatOpenAI
from dotenv import load_dotenv

load_dotenv()
 
 # Get the values from the .env file
open_api_key= os.getenv("OPEN_API_KEY")
deployment_name=os.getenv("DEPLOYMENT_NAME")
open_api_base=os.getenv("BASE_URL")
open_api_version=os.getenv("API_VERSION")
  
 
# Create the model instance
def call_model():
    return AzureChatOpenAI(deployment_name = deployment_name,
                        openai_api_key = open_api_key,
                        openai_api_version = open_api_version,
                        azure_endpoint = open_api_base,
                        temperature = 0)

if __name__ == "__main__":
    print("Model initialized successfully")