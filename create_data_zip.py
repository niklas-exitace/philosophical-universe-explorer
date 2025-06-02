"""Create episode_data.zip for deployment"""

import zipfile
from pathlib import Path
import sys

def create_episode_zip():
    """Create a zip file with all episode data"""
    
    # Source path - adjust this to your local path
    source_path = Path("../podcast_analysis/data/final_processed")
    
    # Check if source exists
    if not source_path.exists():
        print(f"Error: Source path not found: {source_path}")
        print("Please adjust the source_path variable to point to your episode data")
        sys.exit(1)
    
    # Get all JSON files
    json_files = list(source_path.glob("*.json"))
    
    # Filter out index and checkpoint files
    json_files = [f for f in json_files if f.name not in ['episode_index.json', 'processing_checkpoint.json']]
    json_files = [f for f in json_files if 'batch_results' not in f.name]
    
    print(f"Found {len(json_files)} episode files")
    
    if not json_files:
        print("Error: No episode JSON files found!")
        sys.exit(1)
    
    # Create zip file
    zip_path = Path("episode_data.zip")
    
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for json_file in json_files:
            # Add file with just its name (no directory structure)
            zipf.write(json_file, json_file.name)
            print(f"Added: {json_file.name}")
    
    print(f"\n✅ Created {zip_path}")
    print(f"📦 Size: {zip_path.stat().st_size / 1024 / 1024:.2f} MB")
    print("\n📤 Upload this file to your deployed Streamlit app!")

if __name__ == "__main__":
    create_episode_zip()