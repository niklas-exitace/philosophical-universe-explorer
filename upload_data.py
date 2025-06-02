"""
Data Upload Helper for Streamlit Deployment
Run this locally to create a compressed data file for upload
"""

import os
import json
import zipfile
from pathlib import Path

def create_data_zip():
    """Create a zip file of all processed data"""
    
    # Path to the actual data
    source_path = Path(r"C:\Users\Niklas\PycharmProjects\Mondlandung\podcast_analysis\data\final_processed")
    
    if not source_path.exists():
        print(f"Error: Source path not found: {source_path}")
        return
    
    # Create zip file
    zip_path = Path("episode_data.zip")
    
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        # Add all JSON files
        json_files = list(source_path.glob("*.json"))
        print(f"Found {len(json_files)} JSON files")
        
        for json_file in json_files:
            # Add file to zip with just the filename (no path)
            zipf.write(json_file, json_file.name)
            print(f"Added: {json_file.name}")
    
    print(f"\n✅ Created {zip_path}")
    print(f"📦 File size: {zip_path.stat().st_size / 1024 / 1024:.2f} MB")
    print("\n📤 Upload this file to your Streamlit app!")

if __name__ == "__main__":
    create_data_zip()