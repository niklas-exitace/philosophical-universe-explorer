#!/usr/bin/env python3
"""
Setup and Run Script for Philosophical Universe Explorer
This script ensures all dependencies are installed and launches the app.
"""

import subprocess
import sys
import os
from pathlib import Path

def main():
    """Setup and run the Philosophical Universe Explorer."""
    
    print("🌌 Philosophical Universe Explorer - Setup & Run")
    print("=" * 50)
    
    # Change to project directory
    project_dir = Path(__file__).parent
    os.chdir(project_dir)
    
    print("\n📦 Installing required dependencies...")
    print("This may take a few minutes on first run.\n")
    
    # Install requirements
    try:
        subprocess.check_call([
            sys.executable, "-m", "pip", "install", "-r", "requirements.txt", "--quiet"
        ])
        print("✅ Dependencies installed successfully!")
    except subprocess.CalledProcessError:
        print("❌ Failed to install dependencies.")
        print("Please run manually: pip install -r requirements.txt")
        return
    
    print("\n🔍 Verifying data...")
    data_path = project_dir / "data" / "processed"
    if data_path.exists():
        episode_count = len(list(data_path.glob("*.json")))
        print(f"✅ Found {episode_count} analyzed episodes")
    else:
        print("⚠️  No processed data found. The app will guide you through data setup.")
    
    print("\n🚀 Launching Philosophical Universe Explorer...")
    print("\n" + "="*50)
    print("📌 The app will open in your default browser.")
    print("📌 If it doesn't, navigate to: http://localhost:8501")
    print("📌 Press Ctrl+C to stop the server.")
    print("="*50 + "\n")
    
    # Launch the app
    try:
        subprocess.run([sys.executable, "-m", "streamlit", "run", "app_complete.py"])
    except KeyboardInterrupt:
        print("\n\n👋 Thank you for exploring the philosophical universe!")
        print("🌟 Come back anytime to continue your journey.")
    except Exception as e:
        print(f"\n❌ Error launching app: {e}")
        print("Please try running manually: streamlit run app_complete.py")

if __name__ == "__main__":
    main()