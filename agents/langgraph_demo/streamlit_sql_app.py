import streamlit as st
import pandas as pd
from langchain_community.agent_toolkits import SQLDatabaseToolkit
from langchain_community.utilities import SQLDatabase
from langchain_community.agent_toolkits import create_sql_agent
from llm_model import call_model
import psycopg2
from dotenv import load_dotenv
import os
import time

# Load environment variables
load_dotenv()

# Page configuration
st.set_page_config(
    page_title="SQL Agent Query Interface",
    page_icon="🗃️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .query-box {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 10px;
        margin: 1rem 0;
    }
    .result-box {
        background-color: #e8f4fd;
        padding: 1rem;
        border-radius: 10px;
        margin: 1rem 0;
    }
    .error-box {
        background-color: #ffebee;
        padding: 1rem;
        border-radius: 10px;
        margin: 1rem 0;
        border-left: 5px solid #f44336;
    }
    .success-box {
        background-color: #e8f5e8;
        padding: 1rem;
        border-radius: 10px;
        margin: 1rem 0;
        border-left: 5px solid #4caf50;
    }
</style>
""", unsafe_allow_html=True)

def initialize_sql_agent():
    """Initialize the SQL agent with database connection."""
    try:
        # Database connection string
        db_uri = "postgresql+psycopg2://testdb_user:testdb123@localhost:5432/testdb?options=-csearch_path=member_identity,incentives,public"
        
        # Create database connection
        db = SQLDatabase.from_uri(db_uri)
        
        # Create toolkit
        toolkit = SQLDatabaseToolkit(db=db, llm=call_model())
        
        # Create SQL agent
        sql_agent = create_sql_agent(
            llm=call_model(),
            toolkit=toolkit,
            verbose=True
        )
        
        return sql_agent, db
    except Exception as e:
        st.error(f"Failed to initialize SQL agent: {str(e)}")
        return None, None

def get_database_info(db):
    """Get basic information about the database."""
    try:
        # Get table names
        table_names = db.get_usable_table_names()
        
        # Get database dialect
        dialect = db.dialect
        
        return {
            "tables": table_names,
            "dialect": str(dialect),
            "total_tables": len(table_names)
        }
    except Exception as e:
        return {"error": str(e)}

def execute_query(agent, query):
    """Execute a query using the SQL agent."""
    try:
        with st.spinner("Executing query..."):
            result = agent.invoke({"input": query})
            return result
    except Exception as e:
        return {"error": str(e)}

def main():
    # Main header
    st.markdown('<h1 class="main-header">🗃️ SQL Agent Query Interface</h1>', unsafe_allow_html=True)
    
    # Sidebar for database information and settings
    with st.sidebar:
        st.header("🔧 Database Information")
        
        # Initialize session state
        if 'sql_agent' not in st.session_state:
            st.session_state.sql_agent = None
            st.session_state.db = None
            st.session_state.db_info = None
        
        # Initialize database button
        if st.button("🔄 Initialize Database Connection", type="primary"):
            with st.spinner("Connecting to database..."):
                agent, db = initialize_sql_agent()
                if agent and db:
                    st.session_state.sql_agent = agent
                    st.session_state.db = db
                    st.session_state.db_info = get_database_info(db)
                    st.success("✅ Database connected successfully!")
                else:
                    st.error("❌ Failed to connect to database")
        
        # Display database info if available
        if st.session_state.db_info and 'error' not in st.session_state.db_info:
            st.subheader("📊 Database Details")
            st.write(f"**Dialect:** {st.session_state.db_info['dialect']}")
            st.write(f"**Total Tables:** {st.session_state.db_info['total_tables']}")
            
            if st.session_state.db_info['tables']:
                st.subheader("📋 Available Tables")
                for table in st.session_state.db_info['tables']:
                    st.write(f"• {table}")
        
        # Connection status
        if st.session_state.sql_agent:
            st.success("🟢 Agent Ready")
        else:
            st.warning("🟡 Agent Not Initialized")
    
    # Main content area
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.header("💬 Query Interface")
        
        # Check if agent is initialized
        if not st.session_state.sql_agent:
            st.warning("⚠️ Please initialize the database connection first using the sidebar.")
            st.info("👈 Use the 'Initialize Database Connection' button in the sidebar to get started.")
            return
        
        # Query input
        st.subheader("📝 Enter your SQL query or question")
        
        # Predefined example queries
        example_queries = [
            "How many rows are in the incentive transaction table?",
            "Show me the schema of all tables",
            "What are the column names in the member table?",
            "Count the total number of records across all tables",
            "Show me the first 5 rows from any table with data"
        ]
        
        # Example queries dropdown
        selected_example = st.selectbox(
            "📚 Choose an example query (optional):",
            [""] + example_queries,
            index=0
        )
        
        # Query text area
        query_input = st.text_area(
            "Your query:",
            value=selected_example if selected_example else "",
            height=100,
            placeholder="Enter your SQL question or query here..."
        )
        
        # Execute button
        col_btn1, col_btn2, col_btn3 = st.columns([1, 1, 2])
        
        with col_btn1:
            execute_btn = st.button("🚀 Execute Query", type="primary")
        
        with col_btn2:
            clear_btn = st.button("🧹 Clear")
        
        if clear_btn:
            st.rerun()
        
        # Execute query
        if execute_btn and query_input.strip():
            st.markdown('<div class="query-box">', unsafe_allow_html=True)
            st.write("**Executing Query:**")
            st.code(query_input, language="sql")
            st.markdown('</div>', unsafe_allow_html=True)
            
            # Execute the query
            result = execute_query(st.session_state.sql_agent, query_input)
            
            if result and 'error' not in result:
                st.markdown('<div class="success-box">', unsafe_allow_html=True)
                st.success("✅ Query executed successfully!")
                st.markdown('</div>', unsafe_allow_html=True)
                
                # Display results
                st.subheader("📊 Query Results")
                
                # Try to parse and display the output
                if 'output' in result:
                    st.markdown('<div class="result-box">', unsafe_allow_html=True)
                    st.write("**Agent Response:**")
                    st.write(result['output'])
                    st.markdown('</div>', unsafe_allow_html=True)
                
                # Show intermediate steps if available
                if 'intermediate_steps' in result and result['intermediate_steps']:
                    with st.expander("🔍 View Execution Steps"):
                        for i, step in enumerate(result['intermediate_steps']):
                            st.write(f"**Step {i+1}:**")
                            st.write(step)
                            st.divider()
                
                # Display full result in expander
                with st.expander("📋 Full Result Details"):
                    st.json(result)
                    
            else:
                error_msg = result.get('error', 'Unknown error occurred') if result else 'No result returned'
                st.markdown('<div class="error-box">', unsafe_allow_html=True)
                st.error(f"❌ Error executing query: {error_msg}")
                st.markdown('</div>', unsafe_allow_html=True)
        
        elif execute_btn and not query_input.strip():
            st.warning("⚠️ Please enter a query before executing.")
    
    with col2:
        st.header("📚 Quick Help")
        
        st.subheader("💡 Tips")
        st.write("""
        • Ask natural language questions about your data
        • Use specific table names if you know them
        • Ask for schema information to understand your data structure
        • Be specific about what you want to see
        """)
        
        st.subheader("🔍 Example Questions")
        st.write("""
        • "How many users are in the database?"
        • "What columns does the orders table have?"
        • "Show me recent transactions"
        • "What's the average order value?"
        • "List all table names"
        """)
        
        st.subheader("⚙️ Features")
        st.write("""
        • 🤖 AI-powered SQL generation
        • 📊 Natural language queries
        • 🔍 Database schema exploration
        • 📈 Result visualization
        • 🚀 Real-time execution
        """)
        
        # Query history (if we want to implement it later)
        if 'query_history' not in st.session_state:
            st.session_state.query_history = []
        
        if st.session_state.query_history:
            st.subheader("📝 Recent Queries")
            for i, query in enumerate(reversed(st.session_state.query_history[-5:])):
                with st.expander(f"Query {len(st.session_state.query_history) - i}"):
                    st.code(query, language="sql")

if __name__ == "__main__":
    main()

