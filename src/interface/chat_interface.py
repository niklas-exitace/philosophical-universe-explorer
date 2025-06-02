"""Philosophical chat interface using Anthropic Claude"""

import os
import logging
from typing import List, Dict, Optional
import anthropic
from datetime import datetime

logger = logging.getLogger(__name__)


class PhilosophicalChatInterface:
    """Chat interface for philosophical discussions using Claude"""
    
    def __init__(self, data_manager, config):
        self.data_manager = data_manager
        self.config = config
        
        # Initialize Anthropic client if API key is available
        self.anthropic_key = os.getenv("ANTHROPIC_API_KEY") or config.api.anthropic_key
        if self.anthropic_key:
            self.client = anthropic.Anthropic(api_key=self.anthropic_key)
            self.model = "claude-opus-4-20250514"  # Claude Opus 4
            logger.info("Anthropic Claude initialized")
        else:
            self.client = None
            logger.warning("No Anthropic API key found - using fallback mode")
    
    def chat(self, 
             message: str, 
             context: Optional[str] = None,
             episode_context: Optional[List[str]] = None,
             conversation_history: Optional[List[Dict]] = None) -> str:
        """
        Chat about philosophical content
        
        Args:
            message: User's message
            context: Optional context type ('episode', 'concept', 'general')
            episode_context: List of episode IDs to consider
            conversation_history: Previous messages in conversation
        """
        
        if not self.client:
            return self._fallback_response(message)
        
        # Build context
        system_prompt = self._build_system_prompt(context, episode_context)
        
        # Prepare messages
        messages = []
        
        # Add conversation history if provided
        if conversation_history:
            for msg in conversation_history[-10:]:  # Last 10 messages
                messages.append({
                    "role": msg["role"],
                    "content": msg["content"]
                })
        
        # Add current message
        messages.append({
            "role": "user",
            "content": message
        })
        
        try:
            # Query Claude
            response = self.client.messages.create(
                model=self.model,
                max_tokens=1000,
                temperature=0.7,
                system=system_prompt,
                messages=messages
            )
            
            return response.content[0].text
            
        except Exception as e:
            logger.error(f"Error in Claude chat: {e}")
            return self._fallback_response(message)
    
    def _build_system_prompt(self, context: Optional[str], episode_ids: Optional[List[str]]) -> str:
        """Build system prompt with relevant context"""
        
        base_prompt = """You are a philosophical guide helping explore ideas from the Mondlandung podcast. 
You have deep knowledge of philosophy and can discuss concepts in an engaging, accessible way.
You reference specific episodes and concepts when relevant, and help users discover connections between ideas.
Your tone is thoughtful, curious, and encouraging of philosophical exploration."""
        
        # Add episode context if provided
        if episode_ids:
            episodes_context = "\n\nRelevant episodes for this conversation:\n"
            for ep_id in episode_ids[:5]:  # Limit to 5 episodes
                episode = self.data_manager.get_episode(ep_id)
                if episode:
                    episodes_context += f"\n- {episode.title}: {episode.content_analysis.get('summary', {}).get('brief', '')}"
                    
                    # Add key concepts
                    concepts = episode.philosophical_content.get('concepts_explored', [])[:3]
                    if concepts:
                        concept_names = [c.get('concept', '') for c in concepts if isinstance(c, dict)]
                        episodes_context += f"\n  Key concepts: {', '.join(concept_names)}"
            
            base_prompt += episodes_context
        
        # Add general statistics
        stats = self.data_manager.get_statistics()
        base_prompt += f"\n\nThe podcast collection contains {stats['total_episodes']} episodes exploring {stats['total_concepts']} unique philosophical concepts."
        
        return base_prompt
    
    def _fallback_response(self, message: str) -> str:
        """Fallback response when Claude is not available"""
        return """I apologize, but I'm currently unable to process your request as the Anthropic Claude API is not configured. 
        
To enable philosophical chat:
1. Add your Anthropic API key to the environment
2. Or use the OpenAI-based chat functionality

You can still explore episodes, visualize concepts, and use other features of the app!"""
    
    def generate_philosophical_question(self, episode_id: str) -> str:
        """Generate a thought-provoking question about an episode"""
        episode = self.data_manager.get_episode(episode_id)
        if not episode:
            return "What philosophical questions arise from this episode?"
        
        if not self.client:
            # Simple fallback
            return f"What does '{episode.title}' teach us about the human condition?"
        
        try:
            prompt = f"""Based on this philosophical podcast episode, generate one thought-provoking question that encourages deep reflection.

Episode: {episode.title}
Summary: {episode.content_analysis.get('summary', {}).get('brief', '')}
Key concepts: {', '.join([c.get('concept', '') for c in episode.philosophical_content.get('concepts_explored', [])[:3]])}

Generate a single question that:
1. Connects to the episode's themes
2. Encourages personal reflection
3. Has no simple answer
4. Relates to everyday life"""

            response = self.client.messages.create(
                model=self.model,
                max_tokens=100,
                temperature=0.8,
                messages=[{"role": "user", "content": prompt}]
            )
            
            return response.content[0].text.strip()
            
        except Exception as e:
            logger.error(f"Error generating question: {e}")
            return f"How do the ideas in '{episode.title}' apply to your own life?"
    
    def create_learning_path(self, 
                           starting_concept: str,
                           target_understanding: str,
                           max_episodes: int = 5) -> List[Dict]:
        """Create a personalized learning path"""
        
        if not self.client:
            # Simple fallback - return episodes with the concept
            episodes = self.data_manager.get_episodes_by_concept(starting_concept)
            return [{
                'episode_id': ep.episode_id,
                'title': ep.title,
                'reason': f"Explores {starting_concept}"
            } for ep in episodes[:max_episodes]]
        
        # Get relevant episodes
        concept_episodes = self.data_manager.get_episodes_by_concept(starting_concept)
        
        # Get all concepts for context
        all_concepts = list(self.data_manager.get_all_concepts().keys())[:50]
        
        try:
            prompt = f"""Create a learning path for someone interested in understanding "{target_understanding}" starting from "{starting_concept}".

Available episodes that discuss {starting_concept}:
{chr(10).join([f"- {ep.title}" for ep in concept_episodes[:10]])}

Other philosophical concepts covered in the podcast:
{', '.join(all_concepts[:30])}

Create a sequence of 3-5 episodes that would best guide someone from basic understanding to deeper insight.
For each episode, explain why it's included and what it contributes to the journey.

Format as a JSON list with: episode_title, reason, key_concepts"""

            response = self.client.messages.create(
                model=self.model,
                max_tokens=500,
                temperature=0.7,
                messages=[{"role": "user", "content": prompt}]
            )
            
            # Parse response and match to actual episodes
            # This is simplified - in production you'd want more robust parsing
            path = []
            for ep in concept_episodes[:max_episodes]:
                path.append({
                    'episode_id': ep.episode_id,
                    'title': ep.title,
                    'reason': f"Explores {starting_concept} and related concepts",
                    'concepts': [c.get('concept', '') for c in ep.philosophical_content.get('concepts_explored', [])[:3]]
                })
            
            return path
            
        except Exception as e:
            logger.error(f"Error creating learning path: {e}")
            return self.create_learning_path(starting_concept, target_understanding, max_episodes)