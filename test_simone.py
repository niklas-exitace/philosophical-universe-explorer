#!/usr/bin/env python3
"""Basic test script for Project Simone"""

import sys
import io
from pathlib import Path

# Set UTF-8 encoding for Windows
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

# Add project to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

try:
    print("Testing Project Simone installation...")
    
    # Test imports
    print("[OK] Testing imports...")
    from src.core import SimoneEngine, Config
    from src.analysis import PhilosophicalAnalyzer, ConceptMapper, InsightGenerator
    from src.utils import LLMClient, Cache
    
    # Test configuration loading
    print("[OK] Testing configuration...")
    config = Config()
    print(f"  - API key configured: {'Yes' if config.api.openai_key else 'No'}")
    print(f"  - Cache directory: {config.paths.cache_dir}")
    print(f"  - Existing analysis path: {config.paths.existing_analysis}")
    print(f"  - Path exists: {config.paths.existing_analysis.exists()}")
    
    # Test engine initialization
    print("[OK] Testing engine initialization...")
    engine = SimoneEngine()
    
    # Test data loading
    print("[OK] Testing data loading...")
    stats = engine.get_statistics()
    print(f"  - Episodes loaded: {stats['total_episodes']}")
    print(f"  - Valid episodes: {stats['valid_episodes']}")
    print(f"  - Total concepts: {stats['total_concepts']}")
    
    # Test basic functionality
    print("[OK] Testing basic functionality...")
    all_concepts = engine.data_manager.get_all_concepts()
    if all_concepts:
        first_concept = list(all_concepts.keys())[0]
        print(f"  - Sample concept: '{first_concept}' appears {all_concepts[first_concept]} times")
    
    print("\n[SUCCESS] All tests passed! Project Simone is ready to use.")
    print("\nRun 'python quickstart.py' for an interactive demo.")
    
except Exception as e:
    print(f"\n[ERROR] Test failed: {e}")
    import traceback
    traceback.print_exc()