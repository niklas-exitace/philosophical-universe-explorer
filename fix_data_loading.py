"""
Fix for data loading in deployment
"""
import os
import shutil
from pathlib import Path

# Copy uploaded data to the expected location
source = Path("data/processed")
target = Path("data/processed")

if source.exists() and len(list(source.glob("*.json"))) > 0:
    print(f"✅ Data already in correct location: {len(list(source.glob('*.json')))} files")
else:
    # Check if data was uploaded to wrong location
    possible_locations = [
        Path("C:/Users/Niklas/PycharmProjects/Mondlandung/podcast_analysis/data/final_processed"),
        Path("podcast_analysis/data/final_processed"),
        Path("final_processed"),
        Path(".")
    ]
    
    for loc in possible_locations:
        if loc.exists():
            json_files = list(loc.glob("*.json"))
            if json_files:
                print(f"Found {len(json_files)} files in {loc}")
                target.mkdir(parents=True, exist_ok=True)
                for f in json_files:
                    shutil.copy2(f, target / f.name)
                print(f"✅ Copied data to {target}")
                break

print("\nChecking all data locations:")
for root, dirs, files in os.walk("."):
    json_files = [f for f in files if f.endswith(".json")]
    if json_files:
        print(f"Found {len(json_files)} JSON files in: {root}")