#!/usr/bin/env python3
"""
Simple test to verify LangGraph Studio setup
"""

def test_imports():
    """Test that all required modules can be imported"""
    try:
        from langchain_anthropic import ChatAnthropic
        print("✅ langchain_anthropic imported successfully")
    except ImportError as e:
        print(f"❌ Failed to import langchain_anthropic: {e}")
        return False
    
    try:
        from langgraph.graph import StateGraph, MessagesState, START, END
        print("✅ langgraph.graph imported successfully")
    except ImportError as e:
        print(f"❌ Failed to import langgraph.graph: {e}")
        return False
    
    try:
        from langgraph.prebuilt import create_react_agent
        print("✅ langgraph.prebuilt imported successfully")
    except ImportError as e:
        print(f"❌ Failed to import langgraph.prebuilt: {e}")
        return False
    
    try:
        from langchain_core.tools import tool
        print("✅ langchain_core.tools imported successfully")
    except ImportError as e:
        print(f"❌ Failed to import langchain_core.tools: {e}")
        return False
    
    try:
        from langchain_tavily import TavilySearch
        print("✅ langchain_tavily imported successfully")
    except ImportError as e:
        print(f"❌ Failed to import langchain_tavily: {e}")
        return False
    
    try:
        from langchain_experimental.utilities import PythonREPL
        print("✅ langchain_experimental.utilities imported successfully")
    except ImportError as e:
        print(f"❌ Failed to import langchain_experimental.utilities: {e}")
        return False
    
    return True

def test_langgraph_cli():
    """Test if langgraph CLI is available"""
    import subprocess
    try:
        result = subprocess.run(['langgraph', '--version'], 
                              capture_output=True, text=True, timeout=10)
        if result.returncode == 0:
            print(f"✅ LangGraph CLI available: {result.stdout.strip()}")
            return True
        else:
            print(f"❌ LangGraph CLI error: {result.stderr}")
            return False
    except FileNotFoundError:
        print("❌ LangGraph CLI not found. Please install: pip install langgraph-sdk")
        return False
    except subprocess.TimeoutExpired:
        print("❌ LangGraph CLI test timed out")
        return False

def main():
    print("🧪 Testing LangGraph Studio Setup...")
    print("=" * 50)
    
    # Test imports
    imports_ok = test_imports()
    print()
    
    # Test CLI
    cli_ok = test_langgraph_cli()
    print()
    
    if imports_ok and cli_ok:
        print("🎉 All tests passed! LangGraph Studio is ready to use.")
        print("\n🚀 To start LangGraph Studio, run:")
        print("   ./start_studio.sh")
        print("   # or manually:")
        print("   langgraph studio")
    else:
        print("❌ Some tests failed. Please check the errors above.")
        if not imports_ok:
            print("   - Make sure you're in the virtual environment")
            print("   - Run: source ../.venv/bin/activate")
        if not cli_ok:
            print("   - Install LangGraph CLI: pip install langgraph-sdk")

if __name__ == "__main__":
    main()
