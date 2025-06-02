"""Enhanced Philosophical chat interface with episode content search"""

import os
import logging
from typing import List, Dict, Optional, Tuple
import anthropic
from datetime import datetime
import json

logger = logging.getLogger(__name__)


class EnhancedPhilosophicalChat:
    """Enhanced chat interface that searches through actual episode content"""
    
    def __init__(self, data_manager, config, api_key: Optional[str] = None):
        self.data_manager = data_manager
        self.config = config
        
        # Use provided API key (session-based) or fall back to environment/config
        self.anthropic_key = api_key or os.getenv("ANTHROPIC_API_KEY") or getattr(config.api, 'anthropic_key', None)
        
        if self.anthropic_key:
            self.client = anthropic.Anthropic(api_key=self.anthropic_key)
            self.model = "claude-opus-4-20250514"  # Claude Opus 4 - most intelligent model
            logger.info("Anthropic Claude Opus 4 initialized with enhanced capabilities")
        else:
            self.client = None
            logger.warning("No Anthropic API key found - using fallback mode")
    
    def update_api_key(self, api_key: str):
        """Update API key during session"""
        self.anthropic_key = api_key
        if api_key:
            self.client = anthropic.Anthropic(api_key=api_key)
            logger.info("API key updated")
        else:
            self.client = None
    
    def search_episode_content(self, query: str, max_results: int = 5) -> List[Tuple[str, str, float]]:
        """
        Search through all episode content for relevant passages
        Returns: List of (episode_id, relevant_text, relevance_score)
        """
        results = []
        query_lower = query.lower()
        query_words = set(query_lower.split())
        
        for episode in self.data_manager.episodes.values():
            # Search in various fields
            relevance_score = 0
            relevant_texts = []
            
            # Check title
            if any(word in episode.title.lower() for word in query_words):
                relevance_score += 3
                relevant_texts.append(f"Title: {episode.title}")
            
            # Check summary
            summary = episode.content_analysis.get('summary', {})
            if isinstance(summary, dict):
                brief = summary.get('brief', '')
                if any(word in brief.lower() for word in query_words):
                    relevance_score += 2
                    relevant_texts.append(f"Summary: {brief[:200]}...")
            
            # Check concepts
            for concept in episode.philosophical_content.get('concepts_explored', []):
                if isinstance(concept, dict):
                    concept_name = concept.get('concept', '').lower()
                    concept_desc = concept.get('description', '').lower()
                    if any(word in concept_name for word in query_words):
                        relevance_score += 5
                        relevant_texts.append(f"Concept: {concept.get('concept', '')} - {concept.get('description', '')[:150]}...")
                    elif any(word in concept_desc for word in query_words):
                        relevance_score += 2
                        relevant_texts.append(f"Concept: {concept.get('concept', '')} - {concept.get('description', '')[:150]}...")
            
            # Check secondary topics (themes)
            secondary_topics = episode.content_analysis.get('secondary_topics', [])
            for theme in secondary_topics:
                if any(word in theme.lower() for word in query_words):
                    relevance_score += 3
                    relevant_texts.append(f"Theme: {theme}")
            
            # Check unique insights (quotes)
            for quote in episode.unique_insights[:3]:
                if any(word in quote.lower() for word in query_words):
                    relevance_score += 2
                    relevant_texts.append(f"Insight: \"{quote[:150]}...\"")
            
            # Check key takeaways
            takeaways = episode.listener_value.get('key_takeaways', [])
            for takeaway in takeaways[:2]:
                if any(word in takeaway.lower() for word in query_words):
                    relevance_score += 2
                    relevant_texts.append(f"Takeaway: {takeaway[:150]}...")
            
            if relevance_score > 0:
                # Combine relevant texts
                combined_text = "\n".join(relevant_texts[:3])  # Top 3 most relevant
                results.append((episode.episode_id, combined_text, relevance_score))
        
        # Sort by relevance and return top results
        results.sort(key=lambda x: x[2], reverse=True)
        return results[:max_results]
    
    def chat_with_content(self, 
                         message: str, 
                         conversation_history: Optional[List[Dict]] = None) -> str:
        """
        Chat about philosophical content with full episode search
        """
        
        # Search for relevant content first
        search_results = self.search_episode_content(message, max_results=5)
        
        if not self.client:
            return self._enhanced_fallback_response(message, search_results)
        
        # Build context with actual episode content
        context_parts = []
        
        if search_results:
            context_parts.append("I found relevant content in these episodes:\n")
            for episode_id, relevant_text, score in search_results:
                episode = self.data_manager.get_episode(episode_id)
                if episode:
                    context_parts.append(f"\n**{episode.title}**")
                    context_parts.append(relevant_text)
                    context_parts.append("---")
        
        context_text = "\n".join(context_parts)
        
        # Build system prompt
        system_prompt = f"""You are a philosophical guide with deep knowledge of the Mondlandung podcast content. 
You have access to actual episode transcripts and can reference specific discussions, concepts, and quotes.
When users ask about when something was discussed, search through the provided context to find specific episodes.
Always cite specific episodes when referencing content.
Your tone is thoughtful, curious, and precise about sources.

Episode Database Summary:
- Total episodes: {len(self.data_manager.episodes)}
- Topics covered: Philosophy, psychology, literature, film analysis, and practical wisdom
- Format: Deep philosophical exploration of concepts through various media

Current Context from Episodes:
{context_text}"""
        
        # Prepare messages
        messages = []
        
        # Add conversation history if provided
        if conversation_history:
            for msg in conversation_history[-6:]:  # Last 6 messages for context
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
            # Query Claude with episode context
            response = self.client.messages.create(
                model=self.model,
                max_tokens=1000,
                temperature=0.7,
                system=system_prompt,
                messages=messages
            )
            
            return response.content[0].text
            
        except Exception as e:
            logger.error(f"Error in enhanced Claude chat: {e}")
            return self._enhanced_fallback_response(message, search_results)
    
    def _enhanced_fallback_response(self, message: str, search_results: List[Tuple[str, str, float]]) -> str:
        """Enhanced fallback when API is not available"""
        if not search_results:
            return "I couldn't find specific episodes about that topic. Try asking about concepts like Stoicism, consciousness, freedom, or specific philosophers."
        
        response = "Based on the episode content, here's what I found:\n\n"
        
        for episode_id, relevant_text, score in search_results[:3]:
            episode = self.data_manager.get_episode(episode_id)
            if episode:
                response += f"**{episode.title}**\n{relevant_text}\n\n"
        
        response += "\nNote: For deeper philosophical discussion, please configure the Anthropic API key."
        return response
    
    def get_episode_deep_dive(self, episode_id: str) -> str:
        """Generate a deep philosophical analysis of a specific episode"""
        episode = self.data_manager.get_episode(episode_id)
        if not episode:
            return "Episode not found."
        
        if not self.client:
            # Detailed fallback using episode data
            return self._generate_fallback_deep_dive(episode)
        
        try:
            # Prepare comprehensive episode context
            episode_context = f"""Episode: {episode.title}
Summary: {episode.content_analysis.get('summary', {}).get('brief', '')}

Key Themes: {', '.join(episode.content_analysis.get('secondary_topics', []))}

Philosophical Concepts Explored:
{self._format_concepts(episode.philosophical_content.get('concepts_explored', []))}

Key Insights:
{chr(10).join(['- "' + q + '"' for q in episode.unique_insights[:3]])}

Key Takeaways:
{chr(10).join(['- ' + i for i in episode.listener_value.get('key_takeaways', [])[:3]])}

Thinkers Referenced: {', '.join(episode.philosophical_content.get('thinkers_referenced', []))}
"""
            
            prompt = f"""Provide a deep philosophical analysis of this episode. Include:
1. The central philosophical questions raised
2. How these ideas connect to broader philosophical traditions
3. Practical applications for modern life
4. Questions for further reflection

{episode_context}"""
            
            response = self.client.messages.create(
                model=self.model,
                max_tokens=1500,
                temperature=0.7,
                messages=[{"role": "user", "content": prompt}]
            )
            
            return response.content[0].text
            
        except Exception as e:
            logger.error(f"Error in deep dive: {e}")
            return self._generate_fallback_deep_dive(episode)
    
    def _generate_fallback_deep_dive(self, episode) -> str:
        """Generate deep dive without API"""
        analysis = f"""## Deep Dive: {episode.title}

### Overview
{episode.content_analysis.get('summary', {}).get('brief', 'No summary available.')}

### Key Philosophical Concepts
"""
        
        for concept in episode.philosophical_content.get('concepts_explored', [])[:5]:
            if isinstance(concept, dict):
                analysis += f"\n**{concept.get('concept', 'Unknown')}**\n"
                analysis += f"{concept.get('description', 'No description available.')}\n"
        
        analysis += f"""
### Central Themes
{chr(10).join(['- ' + theme for theme in episode.content_analysis.get('secondary_topics', [])])}

### Notable Insights
{chr(10).join(['- "' + quote + '"' for quote in episode.unique_insights[:3]])}

### Key Takeaways
{chr(10).join(['- ' + takeaway for takeaway in episode.listener_value.get('key_takeaways', [])[:3]])}

### Philosophical Traditions
This episode connects to the work of: {', '.join(episode.philosophical_content.get('thinkers_referenced', ['Various thinkers']))}

### Questions for Reflection
- How do these ideas apply to your own life?
- What assumptions are being challenged?
- How might these concepts change your perspective?
"""
        
        return analysis
    
    def _format_concepts(self, concepts: List[Dict]) -> str:
        """Format concepts for display"""
        formatted = []
        for concept in concepts[:5]:
            if isinstance(concept, dict):
                formatted.append(f"- {concept.get('concept', 'Unknown')}: {concept.get('description', '')[:100]}...")
        return "\n".join(formatted)
    
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
                'reason': f"Explores {starting_concept}",
                'concepts': [c.get('concept', '') for c in ep.philosophical_content.get('concepts_explored', [])[:3]]
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
            # Fallback to simple path
            return [{
                'episode_id': ep.episode_id,
                'title': ep.title,
                'reason': f"Explores {starting_concept}",
                'concepts': [c.get('concept', '') for c in ep.philosophical_content.get('concepts_explored', [])[:3]]
            } for ep in concept_episodes[:max_episodes]]
    
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