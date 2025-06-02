#!/usr/bin/env python3
"""Quick start script for Project Simone"""

import sys
import os
import io
from pathlib import Path

# Set UTF-8 encoding for Windows
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

# Add project to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from src.core import SimoneEngine
import logging

logging.basicConfig(level=logging.INFO, format='%(message)s')
logger = logging.getLogger(__name__)


def main():
    """Quick demonstration of Project Simone capabilities"""
    
    print("""
    ╔═══════════════════════════════════════════════════════════╗
    ║                   PROJECT SIMONE                          ║
    ║     Intelligent Philosophical Content Analysis            ║
    ╚═══════════════════════════════════════════════════════════╝
    """)
    
    print("Initializing Project Simone...")
    engine = SimoneEngine()
    
    # Show statistics
    stats = engine.get_statistics()
    print(f"\n📊 Loaded {stats['valid_episodes']} episodes with valid analysis")
    print(f"   Total concepts discovered: {stats['total_concepts']}")
    print(f"   Philosophers referenced: {stats['total_philosophers']}")
    
    # Show top concepts
    print("\n🔝 Top Philosophical Concepts:")
    concepts = engine.data_manager.get_all_concepts()
    for concept, count in list(concepts.items())[:5]:
        print(f"   • {concept}: {count} occurrences")
    
    # Show top philosophers
    print("\n👤 Most Referenced Philosophers:")
    philosophers = engine.data_manager.get_all_philosophers()
    for philosopher, count in list(philosophers.items())[:5]:
        print(f"   • {philosopher}: {count} mentions")
    
    # Interactive mode
    print("\n💬 Interactive Mode (type 'help' for commands, 'quit' to exit)")
    
    while True:
        try:
            command = input("\n> ").strip()
            
            if command == 'quit':
                break
            elif command == 'help':
                print("""
Available commands:
  ask <question>     - Ask a philosophical question
  concept <name>     - Explore a specific concept
  episode <id>       - Show episode details
  insights           - Generate cross-episode insights
  stats              - Show statistics
  quit               - Exit
                """)
            elif command.startswith('ask '):
                question = command[4:]
                print("\n🤔 Thinking...")
                answer = engine.ask_question(question)
                print(f"\n{answer}")
            elif command.startswith('concept '):
                concept_name = command[8:]
                concept_map = engine.generate_concept_map(concept_name)
                if 'error' in concept_map:
                    print(f"\n❌ {concept_map['error']}")
                else:
                    print(f"\n📚 Concept: {concept_map['concept']}")
                    print(f"   Occurrences: {concept_map['occurrences']}")
                    print(f"   Episodes: {len(concept_map['episodes'])}")
                    print(f"   Related concepts: {len(concept_map['related_concepts'])}")
                    if concept_map['related_concepts']:
                        print("\n   Top related:")
                        for rel in concept_map['related_concepts'][:3]:
                            print(f"   • {rel['concept']} (strength: {rel['strength']})")
            elif command.startswith('episode '):
                ep_id = command[8:]
                episode = engine.data_manager.get_episode(ep_id)
                if episode:
                    print(f"\n📼 Episode: {episode.title}")
                    print(f"   Topic: {episode.content_analysis.get('primary_topic', 'Unknown')}")
                    print(f"   Concepts: {episode.episode_metrics.get('concepts_count', 0)}")
                    print(f"   Complexity: {episode.episode_metrics.get('complexity_level', 'Unknown')}")
                else:
                    print(f"\n❌ Episode '{ep_id}' not found")
            elif command == 'insights':
                print("\n💡 Generating insights...")
                insights = engine.generate_insights()
                if insights.get('meta_insights'):
                    print("\nKey Insights:")
                    for insight in insights['meta_insights'][:3]:
                        print(f"   • {insight}")
            elif command == 'stats':
                stats = engine.get_statistics()
                print(f"\n📊 Statistics:")
                for key, value in stats.items():
                    print(f"   {key}: {value}")
            else:
                print("Unknown command. Type 'help' for available commands.")
                
        except KeyboardInterrupt:
            print("\n\nExiting...")
            break
        except Exception as e:
            print(f"\n❌ Error: {e}")
            logger.exception("Error in interactive mode")
    
    print("\nThank you for using Project Simone! 🌙")


if __name__ == "__main__":
    main()