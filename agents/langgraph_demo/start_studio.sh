#!/bin/bash

echo "🚀 Starting LangGraph Studio..."
echo ""

# Check if we're in the right directory
if [ ! -f "langgraph_studio.py" ]; then
    echo "❌ Error: Please run this script from the langgraph_demo directory"
    echo "   cd agents/langgraph_demo"
    echo "   ./start_studio.sh"
    exit 1
fi

# Activate virtual environment
if [ -f "../.venv/bin/activate" ]; then
    echo "✅ Activating virtual environment..."
    source ../.venv/bin/activate
else
    echo "❌ Error: Virtual environment not found at ../.venv/"
    echo "   Please ensure you're in the right directory and have a .venv folder"
    exit 1
fi

# Check if gradio is available
if ! python -c "import gradio" &> /dev/null; then
    echo "❌ Error: Gradio not found. Installing..."
    pip install gradio
fi

echo "✅ Starting Custom LangGraph Studio..."
echo "📱 A browser window should open automatically"
echo "🌐 If not, check the terminal for the local URL (usually http://localhost:7860)"
echo ""
echo "💡 Tips:"
echo "   - Use Ctrl+C to stop the studio"
echo "   - The studio will show your multi-agent workflow"
echo "   - You can debug and visualize each step"
echo "   - Test different prompts and see how agents work together"
echo ""

# Start the custom studio interface
python simple_studio.py
