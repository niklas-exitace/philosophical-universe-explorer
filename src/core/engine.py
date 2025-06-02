"""Core engine for Project Simone - orchestrates all analysis operations"""

import logging
from typing import Dict, List, Optional, Any
from pathlib import Path
import json
from datetime import datetime

from .config import Config
from .data_manager import DataManager, Episode
from ..analysis import PhilosophicalAnalyzer, ConceptMapper, InsightGenerator
from ..utils import LLMClient, Cache

logger = logging.getLogger(__name__)


class SimoneEngine:
    """Main engine that orchestrates all Project Simone operations"""
    
    def __init__(self, config_path: Optional[str] = None):
        """Initialize the Simone engine"""
        logger.info("Initializing Project Simone Engine...")
        
        # Load configuration
        self.config = Config(config_path)
        
        # Initialize data manager
        self.data_manager = DataManager(self.config)
        
        # Initialize LLM client
        self.llm_client = LLMClient(self.config)
        
        # Initialize cache
        self.cache = Cache(self.config.paths.cache_dir)
        
        # Initialize analyzers
        self.philosophical_analyzer = PhilosophicalAnalyzer(self.llm_client, self.cache)
        self.concept_mapper = ConceptMapper(self.data_manager)
        self.insight_generator = InsightGenerator(self.llm_client, self.data_manager)
        
        logger.info("Project Simone Engine initialized successfully")
    
    def analyze_new_content(self, content: str, metadata: Optional[Dict] = None) -> Episode:
        """Analyze new philosophical content"""
        logger.info("Analyzing new content...")
        
        # Create metadata if not provided
        if metadata is None:
            metadata = {
                'title': 'Untitled Content',
                'source': 'Direct Input',
                'date': datetime.now().isoformat()
            }
        
        # Perform philosophical analysis
        analysis = self.philosophical_analyzer.analyze(content, metadata)
        
        # Create Episode object
        episode = Episode(
            episode_id=f"new_{datetime.now().timestamp()}",
            title=metadata.get('title', 'Untitled'),
            youtube_id=metadata.get('youtube_id', ''),
            filename=metadata.get('filename', ''),
            hosts=metadata.get('hosts', []),
            processed_date=datetime.now(),
            content_analysis=analysis.get('content_analysis', {}),
            philosophical_content=analysis.get('philosophical_content', {}),
            connections=analysis.get('connections', {}),
            cultural_analysis=analysis.get('cultural_analysis', {}),
            language_style=analysis.get('language_style', {}),
            practical_wisdom=analysis.get('practical_wisdom', {}),
            episode_metrics=analysis.get('episode_metrics', {}),
            unique_insights=analysis.get('unique_insights', []),
            listener_value=analysis.get('listener_value', {}),
            raw_transcript=content
        )
        
        return episode
    
    def reanalyze_episode(self, episode_id: str, depth: str = 'standard') -> Optional[Episode]:
        """Re-analyze an existing episode with potentially deeper analysis"""
        logger.info(f"Re-analyzing episode {episode_id} with depth={depth}")
        
        episode = self.data_manager.get_episode(episode_id)
        if not episode:
            logger.error(f"Episode {episode_id} not found")
            return None
        
        # Get analysis settings for specified depth
        depth_config = self.config.analysis.depth_levels.get(depth, {})
        
        # Perform re-analysis
        analysis = self.philosophical_analyzer.analyze(
            episode.raw_transcript,
            {
                'title': episode.title,
                'youtube_id': episode.youtube_id,
                'hosts': episode.hosts
            },
            depth_config=depth_config
        )
        
        # Update episode with new analysis
        episode.content_analysis = analysis.get('content_analysis', episode.content_analysis)
        episode.philosophical_content = analysis.get('philosophical_content', episode.philosophical_content)
        episode.connections = analysis.get('connections', episode.connections)
        episode.cultural_analysis = analysis.get('cultural_analysis', episode.cultural_analysis)
        episode.practical_wisdom = analysis.get('practical_wisdom', episode.practical_wisdom)
        episode.unique_insights = analysis.get('unique_insights', episode.unique_insights)
        episode.episode_metrics = analysis.get('episode_metrics', episode.episode_metrics)
        
        return episode
    
    def generate_concept_map(self, concept: Optional[str] = None) -> Dict[str, Any]:
        """Generate a concept map for all episodes or specific concept"""
        logger.info(f"Generating concept map for: {concept or 'all concepts'}")
        
        if concept:
            return self.concept_mapper.map_single_concept(concept)
        else:
            return self.concept_mapper.map_all_concepts()
    
    def generate_insights(self, topic: Optional[str] = None, episodes: Optional[List[str]] = None) -> Dict[str, Any]:
        """Generate insights across episodes"""
        logger.info(f"Generating insights for topic: {topic or 'all'}")
        
        if episodes:
            episode_list = [self.data_manager.get_episode(ep_id) for ep_id in episodes]
            episode_list = [ep for ep in episode_list if ep]
        else:
            episode_list = self.data_manager.get_all_episodes(valid_only=True)
        
        return self.insight_generator.generate(episode_list, topic)
    
    def ask_question(self, question: str, context: Optional[str] = None) -> str:
        """Ask a question about the philosophical content"""
        logger.info(f"Processing question: {question[:50]}...")
        
        # Determine context
        if context == 'episode' and hasattr(self, '_current_episode'):
            # Answer about specific episode
            return self._ask_about_episode(question, self._current_episode)
        else:
            # Answer across all episodes
            return self._ask_across_episodes(question)
    
    def _ask_about_episode(self, question: str, episode: Episode) -> str:
        """Answer a question about a specific episode"""
        context = f"""
Episode: {episode.title}

Summary: {episode.content_analysis.get('summary', {}).get('detailed', '')}

Key Concepts:
{self._format_concepts(episode.philosophical_content.get('concepts_explored', []))}

Practical Wisdom:
{json.dumps(episode.practical_wisdom, indent=2)}

Unique Insights:
{chr(10).join('- ' + insight for insight in episode.unique_insights[:5])}
"""
        
        prompt = f"""You are an expert on philosophical content analysis. 
Answer the following question based on the provided episode context.

{context}

Question: {question}

Provide a thoughtful, accurate answer that references specific content from the episode."""
        
        return self.llm_client.query(prompt, model='qa')
    
    def _ask_across_episodes(self, question: str) -> str:
        """Answer a question using knowledge from all episodes"""
        # Get relevant episodes
        relevant_episodes = self._find_relevant_episodes(question)
        
        # Prepare context from relevant episodes
        context_parts = []
        for episode in relevant_episodes[:5]:  # Limit to top 5
            context_parts.append(f"""
Episode: {episode.title}
Topic: {episode.content_analysis.get('primary_topic', '')}
Key Points: {episode.content_analysis.get('summary', {}).get('brief', '')}
""")
        
        context = "\n---\n".join(context_parts)
        
        prompt = f"""You are an expert on the Mondlandung philosophy podcast.
Answer the following question using knowledge from multiple episodes.

Relevant Episodes:
{context}

Question: {question}

Provide a comprehensive answer that:
1. Synthesizes insights across episodes
2. Shows how ideas connect or evolve
3. Suggests specific episodes for deeper exploration"""
        
        return self.llm_client.query(prompt, model='qa')
    
    def _find_relevant_episodes(self, question: str) -> List[Episode]:
        """Find episodes most relevant to a question"""
        # Simple keyword-based relevance for now
        # TODO: Implement semantic search
        keywords = question.lower().split()
        
        scored_episodes = []
        for episode in self.data_manager.get_all_episodes(valid_only=True):
            score = 0
            
            # Check title
            title_lower = episode.title.lower()
            for keyword in keywords:
                if keyword in title_lower:
                    score += 2
            
            # Check primary topic
            topic_lower = episode.content_analysis.get('primary_topic', '').lower()
            for keyword in keywords:
                if keyword in topic_lower:
                    score += 1
            
            # Check concepts
            concepts_text = ' '.join([
                c.get('concept', '').lower() 
                for c in episode.philosophical_content.get('concepts_explored', [])
                if isinstance(c, dict)
            ])
            for keyword in keywords:
                if keyword in concepts_text:
                    score += 1
            
            if score > 0:
                scored_episodes.append((score, episode))
        
        # Sort by score and return episodes
        scored_episodes.sort(key=lambda x: x[0], reverse=True)
        return [ep for _, ep in scored_episodes]
    
    def _format_concepts(self, concepts: List[Dict]) -> str:
        """Format concepts for display"""
        formatted = []
        for concept in concepts[:5]:  # Limit to top 5
            if isinstance(concept, dict):
                name = concept.get('concept', '')
                definition = concept.get('definition_given', '')
                if name:
                    formatted.append(f"- {name}: {definition}")
        return '\n'.join(formatted)
    
    def export_insights(self, format: str = 'json', filepath: Optional[Path] = None) -> Path:
        """Export generated insights to file"""
        logger.info(f"Exporting insights in {format} format")
        
        # Generate comprehensive insights
        insights = {
            'generated_date': datetime.now().isoformat(),
            'statistics': self.data_manager.get_statistics(),
            'top_concepts': list(self.data_manager.get_all_concepts().items())[:20],
            'top_philosophers': list(self.data_manager.get_all_philosophers().items())[:20],
            'concept_map': self.generate_concept_map(),
            'cross_episode_insights': self.generate_insights()
        }
        
        # Determine filepath
        if filepath is None:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f"simone_insights_{timestamp}.{format}"
            filepath = self.config.paths.exports_dir / filename
        
        # Export based on format
        if format == 'json':
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(insights, f, ensure_ascii=False, indent=2)
        elif format == 'csv':
            # Export episode data as CSV
            self.data_manager.export_to_csv(filepath)
        else:
            raise ValueError(f"Unsupported export format: {format}")
        
        logger.info(f"Insights exported to {filepath}")
        return filepath
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get current statistics"""
        return self.data_manager.get_statistics()
    
    def set_current_episode(self, episode_id: str):
        """Set the current episode for context-aware operations"""
        episode = self.data_manager.get_episode(episode_id)
        if episode:
            self._current_episode = episode
            logger.info(f"Current episode set to: {episode.title}")
        else:
            logger.error(f"Episode {episode_id} not found")