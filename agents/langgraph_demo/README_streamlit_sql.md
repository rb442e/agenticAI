# Streamlit SQL Agent Interface

This is a web-based interface for querying your PostgreSQL database using natural language, powered by LangChain and Azure OpenAI.

## Features

- 🤖 **AI-Powered SQL Generation**: Ask questions in natural language and get SQL queries automatically generated
- 📊 **Database Schema Explorer**: View available tables and their structures
- 🔍 **Real-time Query Execution**: Execute queries and see results instantly
- 📈 **User-Friendly Interface**: Clean, modern web interface built with Streamlit
- 🚀 **Error Handling**: Comprehensive error handling and user feedback

## Prerequisites

1. **Database Setup**: Ensure you have a PostgreSQL database running with the connection details:
   - Host: localhost
   - Port: 5432
   - Database: testdb
   - Username: testdb_user
   - Password: testdb123
   - Schemas: member_identity, incentives, public

2. **Environment Variables**: Create a `.env` file in the project root with your Azure OpenAI credentials:
   ```env
   OPEN_API_KEY=your_azure_openai_key
   DEPLOYMENT_NAME=your_deployment_name
   BASE_URL=your_azure_openai_endpoint
   API_VERSION=your_api_version
   ```

3. **Dependencies**: Install the required dependencies:
   ```bash
   # If using uv (recommended)
   uv pip install -e .
   
   # Or using pip
   pip install -e .
   ```

## How to Run

1. **Start the Streamlit App**:
   ```bash
   streamlit run streamlit_sql_app.py
   ```

2. **Open Your Browser**: The app will automatically open in your default browser at `http://localhost:8501`

3. **Initialize Database Connection**: Click the "Initialize Database Connection" button in the sidebar

4. **Start Querying**: Enter your questions or SQL queries in the main interface

## Usage Examples

### Natural Language Queries
- "How many rows are in the incentive transaction table?"
- "Show me the schema of all tables"
- "What are the column names in the member table?"
- "Count the total number of records across all tables"

### Direct SQL Queries
- `SELECT COUNT(*) FROM incentive_transactions;`
- `SHOW TABLES;`
- `DESCRIBE member_table;`

## Interface Overview

### Sidebar
- **Database Connection**: Initialize and manage your database connection
- **Database Information**: View connected database details and available tables
- **Connection Status**: Real-time connection status indicator

### Main Interface
- **Query Input**: Large text area for entering your questions or SQL queries
- **Example Queries**: Dropdown with pre-built example queries
- **Execution Controls**: Execute and clear buttons
- **Results Display**: Formatted results with syntax highlighting

### Features Panel
- **Quick Help**: Tips and usage guidance
- **Example Questions**: Sample natural language queries
- **Feature Overview**: List of available features

## Troubleshooting

### Common Issues

1. **Database Connection Failed**:
   - Verify PostgreSQL is running
   - Check connection credentials in the code
   - Ensure the database and schemas exist

2. **Azure OpenAI Errors**:
   - Verify your `.env` file has correct credentials
   - Check your Azure OpenAI deployment is active
   - Ensure you have sufficient quota

3. **Module Import Errors**:
   - Make sure all dependencies are installed
   - Verify you're in the correct virtual environment

### Error Messages
The interface provides detailed error messages to help diagnose issues:
- Connection errors are shown in the sidebar
- Query execution errors are displayed in the main interface
- Helpful tips are provided for common problems

## Architecture

The application consists of several key components:

1. **SQL Agent**: LangChain-based agent that converts natural language to SQL
2. **Database Connection**: PostgreSQL connection with multiple schema support
3. **Streamlit Interface**: Web-based user interface
4. **LLM Integration**: Azure OpenAI for natural language processing

## Security Notes

- The application connects to a local database - ensure proper network security
- API keys are loaded from environment variables - never commit them to version control
- The SQL agent has full database access - use appropriate database user permissions

## Contributing

To extend this interface:
1. Modify `streamlit_sql_app.py` for UI changes
2. Update `sql_agent.py` for agent behavior changes
3. Edit `llm_model.py` for different LLM configurations

## Support

If you encounter issues:
1. Check the troubleshooting section above
2. Verify all prerequisites are met
3. Review the error messages in the interface
4. Check the Streamlit console output for detailed error logs

