from langchain_community.agent_toolkits import SQLDatabaseToolkit
from langchain_community.utilities import SQLDatabase
from langchain_community.agent_toolkits import create_sql_agent
from llm_model import call_model
import psycopg2
import streamlit as st

from dotenv import load_dotenv
load_dotenv()

# Use search_path for multiple schemas
db = SQLDatabase.from_uri(
    "postgresql+psycopg2://testdb_user:testdb123@localhost:5432/testdb?options=-csearch_path=member_identity,incentives,public"
)

toolkit = SQLDatabaseToolkit(db=db, llm=call_model())

# Create SQL agent
sql_agent = create_sql_agent(
    llm=call_model(),
    toolkit=toolkit,
    verbose=True
)

# Test the agent
if __name__ == "__main__":
    try:
        st.title("SQL Agent")
        query = st.text_input("Enter your query") 

        if st.button("Execute"):
            with st.spinner("Executing query..."):
                result = sql_agent.invoke(query)
                st.markdown(result["output"])
    except Exception as e:
        print(f"Error: {e}")
        print("Note: Make sure the 'member' table exists in your testdb database.")
