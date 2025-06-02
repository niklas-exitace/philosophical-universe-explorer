"""Debug data loading issues"""

import sys
from pathlib import Path

# Add project to path
sys.path.insert(0, str(Path(__file__).parent))

from src.core import SimoneEngine

# Initialize engine
print("Initializing SimoneEngine...")
try:
    engine = SimoneEngine()
    print(f"✓ Engine initialized successfully")
    print(f"✓ Config path: {engine.config.config_path}")
    print(f"✓ Data path: {engine.config.paths.existing_analysis}")
    print(f"✓ Path exists: {engine.config.paths.existing_analysis.exists()}")
    
    # Check for data files
    if engine.config.paths.existing_analysis.exists():
        json_files = list(engine.config.paths.existing_analysis.glob("*.json"))
        print(f"✓ Found {len(json_files)} JSON files")
        if json_files:
            print(f"  First file: {json_files[0].name}")
    else:
        print(f"✗ Data directory does not exist: {engine.config.paths.existing_analysis}")
    
    # Check loaded episodes
    print(f"\n✓ Loaded episodes: {len(engine.data_manager.episodes)}")
    
    # Get statistics
    stats = engine.get_statistics()
    print(f"\nStatistics:")
    for key, value in stats.items():
        print(f"  {key}: {value}")
        
except Exception as e:
    print(f"✗ Error: {e}")
    import traceback
    traceback.print_exc()