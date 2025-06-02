#!/usr/bin/env python3
"""Test script to verify app components"""

import sys
import io
from pathlib import Path

# Set UTF-8 encoding for Windows
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

# Add project to path
sys.path.insert(0, str(Path(__file__).parent))

print("Testing Philosophical Universe Explorer components...")

try:
    # Test core imports
    print("\n[1/5] Testing core engine...")
    from src.core import SimoneEngine
    engine = SimoneEngine()
    stats = engine.get_statistics()
    print(f"✅ Core engine loaded - {stats['valid_episodes']} episodes ready")
    
    # Test visualizations
    print("\n[2/5] Testing visualization components...")
    from src.interface.visualizations import ConceptNetworkVisualizer, TimelineVisualizer
    concept_viz = ConceptNetworkVisualizer(engine.concept_mapper)
    timeline_viz = TimelineVisualizer(engine.data_manager)
    print("✅ Visualization components ready")
    
    # Test chat interface
    print("\n[3/5] Testing chat interface...")
    from src.interface.chat_interface import PhilosophicalChatInterface
    chat = PhilosophicalChatInterface(engine.data_manager, engine.config)
    print(f"✅ Chat interface ready (Anthropic: {'Yes' if chat.client else 'No'})")
    
    # Test Streamlit components
    print("\n[4/5] Testing Streamlit availability...")
    import streamlit
    import plotly.graph_objects
    print("✅ Streamlit and Plotly ready")
    
    # Test data
    print("\n[5/5] Testing data availability...")
    concepts = engine.data_manager.get_all_concepts()
    top_concepts = list(concepts.items())[:5]
    print(f"✅ Data loaded - Top concepts: {[c[0] for c in top_concepts]}")
    
    print("\n🎉 All tests passed! The app is ready to run.")
    print("\nTo start the app, run:")
    print("  python run_app.py")
    print("\nOr:")
    print("  streamlit run app_complete.py")
    
except Exception as e:
    print(f"\n❌ Error: {e}")
    import traceback
    traceback.print_exc()
    print("\nPlease check your installation and try again.")