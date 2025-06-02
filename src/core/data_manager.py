"""Data management for Project Simone - handles loading and managing analyzed content"""

import json
import logging
from pathlib import Path
from typing import Dict, List, Optional, Any
from datetime import datetime
import pandas as pd
from dataclasses import dataclass, field

logger = logging.getLogger(__name__)


@dataclass
class Episode:
    """Represents a single analyzed episode"""
    episode_id: str
    title: str
    youtube_id: str
    filename: str
    hosts: List[str]
    processed_date: datetime
    content_analysis: Dict[str, Any]
    philosophical_content: Dict[str, Any]
    connections: Dict[str, Any]
    cultural_analysis: Dict[str, Any]
    language_style: Dict[str, Any]
    practical_wisdom: Dict[str, Any]
    episode_metrics: Dict[str, Any]
    unique_insights: List[str]
    listener_value: Dict[str, Any]
    raw_transcript: str
    
    @classmethod
    def from_json(cls, data: Dict[str, Any]) -> 'Episode':
        """Create Episode from JSON data"""
        metadata = data.get('metadata', {})
        
        # Parse date
        processed_date = metadata.get('processed_date', '')
        if processed_date:
            try:
                processed_date = datetime.fromisoformat(processed_date)
            except:
                processed_date = datetime.now()
        else:
            processed_date = datetime.now()
        
        return cls(
            episode_id=data.get('episode_id', ''),
            title=metadata.get('title', ''),
            youtube_id=metadata.get('youtube_id', ''),
            filename=metadata.get('filename', ''),
            hosts=metadata.get('hosts', []),
            processed_date=processed_date,
            content_analysis=data.get('content_analysis', {}),
            philosophical_content=data.get('philosophical_content', {}),
            connections=data.get('connections', {}),
            cultural_analysis=data.get('cultural_analysis', {}),
            language_style=data.get('language_style', {}),
            practical_wisdom=data.get('practical_wisdom', {}),
            episode_metrics=data.get('episode_metrics', {}),
            unique_insights=data.get('unique_insights', []),
            listener_value=data.get('listener_value', {}),
            raw_transcript=data.get('raw_transcript', '')
        )
    
    def is_valid(self) -> bool:
        """Check if episode has valid analysis data"""
        return (
            self.content_analysis.get('primary_topic') != 'Analysis failed' and
            bool(self.content_analysis.get('summary', {}).get('brief')) and
            self.content_analysis.get('summary', {}).get('brief') != 'Analysis could not be completed'
        )


class DataManager:
    """Manages all data operations for Project Simone"""
    
    def __init__(self, config):
        """Initialize data manager with configuration"""
        self.config = config
        self.episodes: Dict[str, Episode] = {}
        self.df: Optional[pd.DataFrame] = None
        
        # Load existing analyzed data
        self._load_analyzed_episodes()
        
        # Create indexes
        self._create_indexes()
    
    def _load_analyzed_episodes(self):
        """Load all analyzed episodes from existing JSON files"""
        logger.info(f"Loading analyzed episodes from {self.config.paths.existing_analysis}")
        
        json_files = list(self.config.paths.existing_analysis.glob("*.json"))
        
        for json_file in json_files:
            # Skip index files and batch results
            if json_file.name in ['episode_index.json', 'processing_checkpoint.json']:
                continue
            if 'batch_results' in str(json_file):
                continue
                
            try:
                with open(json_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                
                episode = Episode.from_json(data)
                self.episodes[episode.episode_id] = episode
                
            except Exception as e:
                logger.error(f"Error loading {json_file}: {e}")
        
        # Log statistics
        valid_episodes = sum(1 for ep in self.episodes.values() if ep.is_valid())
        logger.info(f"Loaded {len(self.episodes)} episodes ({valid_episodes} with valid analysis)")
    
    def _create_indexes(self):
        """Create various indexes for efficient querying"""
        # Create DataFrame for easy querying
        episodes_data = []
        
        for ep_id, episode in self.episodes.items():
            # Extract key concepts
            concepts = []
            if episode.philosophical_content:
                concepts_list = episode.philosophical_content.get('concepts_explored', [])
                concepts = [c.get('concept', '') for c in concepts_list if isinstance(c, dict)]
            
            # Extract themes
            themes = episode.connections.get('recurring_themes', [])
            
            # Extract philosophers mentioned
            philosophers = []
            if episode.connections:
                philosophers = episode.connections.get('philosophers_mentioned', [])
            
            episodes_data.append({
                'episode_id': ep_id,
                'title': episode.title,
                'primary_topic': episode.content_analysis.get('primary_topic', ''),
                'summary': episode.content_analysis.get('summary', {}).get('brief', ''),
                'concepts': concepts,
                'themes': themes,
                'philosophers': philosophers,
                'complexity_score': episode.episode_metrics.get('complexity_score', 0),
                'concepts_count': episode.episode_metrics.get('concepts_count', 0),
                'is_valid': episode.is_valid(),
                'processed_date': episode.processed_date
            })
        
        self.df = pd.DataFrame(episodes_data)
        logger.info(f"Created index with {len(self.df)} episodes")
    
    def get_episode(self, episode_id: str) -> Optional[Episode]:
        """Get a single episode by ID"""
        return self.episodes.get(episode_id)
    
    def get_all_episodes(self, valid_only: bool = True) -> List[Episode]:
        """Get all episodes, optionally filtering for valid ones"""
        episodes = list(self.episodes.values())
        
        if valid_only:
            episodes = [ep for ep in episodes if ep.is_valid()]
        
        return episodes
    
    def search_episodes(self, query: str, field: str = 'all') -> List[Episode]:
        """Search episodes by query in specified field"""
        results = []
        query_lower = query.lower()
        
        for episode in self.episodes.values():
            if field == 'all' or field == 'title':
                if query_lower in episode.title.lower():
                    results.append(episode)
                    continue
            
            if field == 'all' or field == 'transcript':
                if query_lower in episode.raw_transcript.lower():
                    results.append(episode)
                    continue
            
            if field == 'all' or field == 'concepts':
                concepts_text = ' '.join([
                    c.get('concept', '').lower() 
                    for c in episode.philosophical_content.get('concepts_explored', [])
                    if isinstance(c, dict)
                ])
                if query_lower in concepts_text:
                    results.append(episode)
                    continue
        
        return results
    
    def get_all_concepts(self) -> Dict[str, int]:
        """Get all unique concepts with their frequency"""
        concepts_freq = {}
        
        for episode in self.episodes.values():
            if not episode.is_valid():
                continue
                
            concepts = episode.philosophical_content.get('concepts_explored', [])
            for concept in concepts:
                if isinstance(concept, dict):
                    concept_name = concept.get('concept', '')
                    if concept_name:
                        concepts_freq[concept_name] = concepts_freq.get(concept_name, 0) + 1
        
        return dict(sorted(concepts_freq.items(), key=lambda x: x[1], reverse=True))
    
    def get_all_philosophers(self) -> Dict[str, int]:
        """Get all mentioned philosophers with frequency"""
        philosophers_freq = {}
        
        for episode in self.episodes.values():
            if not episode.is_valid():
                continue
                
            philosophers = episode.connections.get('philosophers_mentioned', [])
            for philosopher in philosophers:
                if philosopher:
                    philosophers_freq[philosopher] = philosophers_freq.get(philosopher, 0) + 1
        
        return dict(sorted(philosophers_freq.items(), key=lambda x: x[1], reverse=True))
    
    def get_episodes_by_concept(self, concept: str) -> List[Episode]:
        """Get all episodes that explore a specific concept"""
        results = []
        concept_lower = concept.lower()
        
        for episode in self.episodes.values():
            if not episode.is_valid():
                continue
                
            concepts = episode.philosophical_content.get('concepts_explored', [])
            for c in concepts:
                if isinstance(c, dict) and concept_lower in c.get('concept', '').lower():
                    results.append(episode)
                    break
        
        return results
    
    def get_episodes_by_philosopher(self, philosopher: str) -> List[Episode]:
        """Get all episodes that mention a specific philosopher"""
        results = []
        philosopher_lower = philosopher.lower()
        
        for episode in self.episodes.values():
            if not episode.is_valid():
                continue
                
            philosophers = episode.connections.get('philosophers_mentioned', [])
            for p in philosophers:
                if philosopher_lower in p.lower():
                    results.append(episode)
                    break
        
        return results
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get overall statistics about the episodes"""
        valid_episodes = [ep for ep in self.episodes.values() if ep.is_valid()]
        
        return {
            'total_episodes': len(self.episodes),
            'valid_episodes': len(valid_episodes),
            'failed_episodes': len(self.episodes) - len(valid_episodes),
            'total_concepts': len(self.get_all_concepts()),
            'total_philosophers': len(self.get_all_philosophers()),
            'avg_complexity': self.df['complexity_score'].mean() if len(self.df) > 0 else 0,
            'avg_concepts_per_episode': self.df['concepts_count'].mean() if len(self.df) > 0 else 0
        }
    
    def export_to_csv(self, filepath: Path):
        """Export episode data to CSV"""
        if self.df is not None:
            # Flatten lists for CSV export
            df_export = self.df.copy()
            df_export['concepts'] = df_export['concepts'].apply(lambda x: ', '.join(x))
            df_export['themes'] = df_export['themes'].apply(lambda x: ', '.join(x))
            df_export['philosophers'] = df_export['philosophers'].apply(lambda x: ', '.join(x))
            
            df_export.to_csv(filepath, index=False)
            logger.info(f"Exported data to {filepath}")