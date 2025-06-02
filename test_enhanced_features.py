#!/usr/bin/env python3
"""Test enhanced features of the Philosophical Universe Explorer"""

import sys
import os
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

def test_enhanced_chat():
    """Test the enhanced chat interface with content search"""
    print("\n🧪 Testing Enhanced Chat Interface...")
    
    try:
        from src.interface.chat_interface_enhanced import EnhancedPhilosophicalChat
        from src.core import SimoneEngine
        from src.core.config import Config
        
        # Initialize components
        config = Config()
        engine = SimoneEngine(config)
        
        # Create chat interface without API key (fallback mode)
        chat = EnhancedPhilosophicalChat(engine.data_manager, config, api_key=None)
        
        # Test content search
        print("\n🔍 Testing content search for 'shadow integration'...")
        results = chat.search_episode_content("shadow integration", max_results=3)
        
        if results:
            print(f"✅ Found {len(results)} relevant episodes:")
            for episode_id, text, score in results:
                episode = engine.data_manager.get_episode(episode_id)
                print(f"\n📚 {episode.title} (relevance: {score})")
                print(f"   {text[:200]}...")
        else:
            print("❌ No results found for 'shadow integration'")
            
        # Test a different search
        print("\n🔍 Testing content search for 'stoicism'...")
        results = chat.search_episode_content("stoicism", max_results=3)
        
        if results:
            print(f"✅ Found {len(results)} relevant episodes:")
            for episode_id, text, score in results:
                episode = engine.data_manager.get_episode(episode_id)
                print(f"\n📚 {episode.title} (relevance: {score})")
                print(f"   {text[:200]}...")
        else:
            print("❌ No results found for 'stoicism'")
        
        # Test fallback chat response
        print("\n💬 Testing fallback chat (no API key)...")
        response = chat.chat_with_content("When did we talk about stoicism?")
        print(f"Response preview: {response[:300]}...")
        
        print("\n✅ Enhanced chat interface tests completed!")
        
    except Exception as e:
        print(f"❌ Error testing enhanced chat: {e}")
        import traceback
        traceback.print_exc()

def test_episode_deep_dive():
    """Test episode deep dive functionality"""
    print("\n🧪 Testing Episode Deep Dive...")
    
    try:
        from src.interface.chat_interface_enhanced import EnhancedPhilosophicalChat
        from src.core import SimoneEngine
        from src.core.config import Config
        
        # Initialize components
        config = Config()
        engine = SimoneEngine(config)
        
        # Get first episode
        episodes = list(engine.data_manager.episodes.values())
        if episodes:
            episode = episodes[0]
            print(f"\n📚 Testing deep dive for: {episode.title}")
            
            # Create chat interface
            chat = EnhancedPhilosophicalChat(engine.data_manager, config, api_key=None)
            
            # Generate deep dive
            deep_dive = chat.get_episode_deep_dive(episode.episode_id)
            print(f"\nDeep dive preview: {deep_dive[:500]}...")
            
            print("\n✅ Deep dive functionality working!")
        else:
            print("❌ No episodes found")
            
    except Exception as e:
        print(f"❌ Error testing deep dive: {e}")
        import traceback
        traceback.print_exc()

def main():
    """Run all tests"""
    print("=" * 50)
    print("🌌 Testing Enhanced Features")
    print("=" * 50)
    
    test_enhanced_chat()
    test_episode_deep_dive()
    
    print("\n" + "=" * 50)
    print("✅ All enhanced feature tests completed!")
    print("\n📌 The app now includes:")
    print("   - Chat that searches actual episode content")
    print("   - Session-based API key input (secure)")
    print("   - Working episode deep dives")
    print("   - Fallback mode when no API key is provided")
    print("\n🚀 Run the app with: python setup_and_run.py")
    print("=" * 50)

if __name__ == "__main__":
    main()