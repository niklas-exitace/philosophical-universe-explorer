#!/usr/bin/env python3
"""
Easy launcher for the Philosophical Universe Explorer
"""

import os
import sys
import subprocess
from pathlib import Path
import webbrowser
import time

def check_requirements():
    """Check if all requirements are installed"""
    print("🔍 Checking requirements...")
    
    required_packages = [
        'streamlit',
        'plotly',
        'pandas',
        'networkx',
        'openai',
        'anthropic'
    ]
    
    missing = []
    for package in required_packages:
        try:
            __import__(package)
        except ImportError:
            missing.append(package)
    
    if missing:
        print(f"❌ Missing packages: {', '.join(missing)}")
        print("Installing missing packages...")
        subprocess.check_call([sys.executable, "-m", "pip", "install"] + missing)
        print("✅ Packages installed!")
    else:
        print("✅ All requirements satisfied!")

def check_api_keys():
    """Check for API keys"""
    print("\n🔑 Checking API keys...")
    
    has_openai = bool(os.getenv('OPENAI_API_KEY'))
    has_anthropic = bool(os.getenv('ANTHROPIC_API_KEY'))
    
    if not has_openai and not has_anthropic:
        print("⚠️  No API keys found. You can add them in the app sidebar.")
        print("   For best experience, set one of:")
        print("   - OPENAI_API_KEY")
        print("   - ANTHROPIC_API_KEY")
    else:
        if has_openai:
            print("✅ OpenAI API key found")
        if has_anthropic:
            print("✅ Anthropic API key found")

def run_app():
    """Run the Streamlit app"""
    print("\n🚀 Launching Philosophical Universe Explorer...")
    print("=" * 50)
    
    app_path = Path(__file__).parent / "app_complete.py"
    
    # Set environment variable to suppress Streamlit's automatic browser opening
    env = os.environ.copy()
    env['STREAMLIT_SERVER_HEADLESS'] = 'true'
    
    # Start Streamlit
    process = subprocess.Popen(
        [sys.executable, "-m", "streamlit", "run", str(app_path), 
         "--server.port", "8501",
         "--server.address", "localhost"],
        env=env
    )
    
    # Wait a moment for the server to start
    time.sleep(3)
    
    # Open browser
    print("\n✨ Opening browser...")
    webbrowser.open('http://localhost:8501')
    
    print("\n" + "=" * 50)
    print("🌌 Philosophical Universe Explorer is running!")
    print("📍 URL: http://localhost:8501")
    print("🛑 Press Ctrl+C to stop the server")
    print("=" * 50)
    
    try:
        process.wait()
    except KeyboardInterrupt:
        print("\n👋 Shutting down...")
        process.terminate()
        process.wait()
        print("✅ Server stopped. Goodbye!")

def main():
    """Main entry point"""
    print("""
    ╔═══════════════════════════════════════════════════════════════╗
    ║              🌌 PHILOSOPHICAL UNIVERSE EXPLORER 🌌             ║
    ║                      Project Simone                           ║
    ╚═══════════════════════════════════════════════════════════════╝
    """)
    
    # Check requirements
    check_requirements()
    
    # Check API keys
    check_api_keys()
    
    # Run the app
    run_app()

if __name__ == "__main__":
    # Make sure we're in the right directory
    os.chdir(Path(__file__).parent)
    
    # Run
    main()