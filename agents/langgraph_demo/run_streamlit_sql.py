#!/usr/bin/env python3
"""
Launcher script for the Streamlit SQL Agent Interface
"""

import subprocess
import sys
import os
from pathlib import Path

def main():
    """Launch the Streamlit SQL interface."""
    
    # Get the directory where this script is located
    script_dir = Path(__file__).parent.absolute()
    
    # Path to the Streamlit app
    streamlit_app = script_dir / "streamlit_sql_app.py"
    
    # Check if the Streamlit app exists
    if not streamlit_app.exists():
        print(f"❌ Error: Streamlit app not found at {streamlit_app}")
        sys.exit(1)
    
    # Check if .env file exists
    env_file = script_dir.parent / ".env"
    if not env_file.exists():
        print("⚠️  Warning: .env file not found in the parent directory")
        print("   Make sure to create a .env file with your Azure OpenAI credentials:")
        print("   - OPEN_API_KEY=your_azure_openai_key")
        print("   - DEPLOYMENT_NAME=your_deployment_name")
        print("   - BASE_URL=your_azure_openai_endpoint")
        print("   - API_VERSION=your_api_version")
        print()
    
    print("🚀 Starting Streamlit SQL Agent Interface...")
    print(f"📁 App location: {streamlit_app}")
    print("🌐 The app will open in your default browser")
    print("⏹️  Press Ctrl+C to stop the server")
    print("-" * 50)
    
    try:
        # Run the Streamlit app
        subprocess.run([
            sys.executable, "-m", "streamlit", "run", str(streamlit_app),
            "--server.headless", "false",
            "--server.runOnSave", "true",
            "--browser.gatherUsageStats", "false"
        ], cwd=script_dir)
        
    except KeyboardInterrupt:
        print("\n👋 Shutting down Streamlit server...")
    except FileNotFoundError:
        print("❌ Error: Streamlit is not installed.")
        print("   Please install it with: pip install streamlit")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Error starting Streamlit: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()

