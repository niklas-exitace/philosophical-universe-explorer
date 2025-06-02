"""Generate cross-episode insights and philosophical synthesis"""

import logging
from typing import Dict, List, Any, Optional
import json
from collections import defaultdict

logger = logging.getLogger(__name__)


class InsightGenerator:
    """Generates insights by synthesizing content across episodes"""
    
    def __init__(self, llm_client, data_manager):
        """Initialize insight generator"""
        self.llm_client = llm_client
        self.data_manager = data_manager
    
    def generate(self, episodes: List, topic: Optional[str] = None) -> Dict[str, Any]:
        """Generate insights from episodes"""
        logger.info(f"Generating insights for {len(episodes)} episodes on topic: {topic or 'all'}")
        
        if not episodes:
            return {'error': 'No episodes provided'}
        
        # Generate different types of insights
        insights = {
            'topic': topic or 'General Philosophy',
            'episode_count': len(episodes),
            'thematic_evolution': self._trace_thematic_evolution(episodes, topic),
            'synthesized_wisdom': self._synthesize_wisdom(episodes, topic),
            'philosophical_patterns': self._identify_patterns(episodes),
            'contradictions_paradoxes': self._find_contradictions(episodes),
            'unique_contributions': self._extract_unique_contributions(episodes),
            'practical_applications': self._compile_practical_applications(episodes, topic)
        }
        
        # Generate meta-insights
        insights['meta_insights'] = self._generate_meta_insights(insights)
        
        return insights
    
    def _trace_thematic_evolution(self, episodes: List, topic: Optional[str]) -> List[Dict[str, Any]]:
        """Trace how themes evolve across episodes"""
        # Sort episodes by date
        sorted_episodes = sorted(episodes, key=lambda e: e.processed_date)
        
        # Prepare episode summaries
        summaries = []
        for ep in sorted_episodes[:10]:  # Limit to prevent token overflow
            summary = {
                'title': ep.title,
                'date': ep.processed_date.isoformat(),
                'topic': ep.content_analysis.get('primary_topic', ''),
                'key_concepts': [c.get('concept', '') for c in ep.philosophical_content.get('concepts_explored', [])[:3]]
            }
            summaries.append(summary)
        
        prompt = f"""Analyze how philosophical themes evolve across these episodes:

{json.dumps(summaries, indent=2)}

{"Focus on topic: " + topic if topic else ""}

Identify:
1. How understanding deepens over time
2. New perspectives introduced
3. Shifts in approach or emphasis
4. Building of complex ideas from simple ones

Provide a JSON array of evolution points, each with: theme, evolution_type, episodes_involved, description"""

        response = self.llm_client.query(prompt, model='analysis')
        
        try:
            return json.loads(response)
        except:
            return [{'description': 'Theme evolution analysis', 'theme': topic or 'Philosophy'}]
    
    def _synthesize_wisdom(self, episodes: List, topic: Optional[str]) -> Dict[str, Any]:
        """Synthesize practical wisdom across episodes"""
        # Collect all wisdom
        all_wisdom = defaultdict(list)
        
        for ep in episodes:
            wisdom = ep.practical_wisdom
            if wisdom.get('life_advice'):
                all_wisdom['life_advice'].extend(wisdom['life_advice'])
            if wisdom.get('mindset_shifts'):
                all_wisdom['mindset_shifts'].extend(wisdom['mindset_shifts'])
            if wisdom.get('implementation_tips'):
                all_wisdom['implementation_tips'].extend(wisdom['implementation_tips'])
        
        # Synthesize using LLM
        prompt = f"""Synthesize this practical wisdom from multiple philosophical discussions:

Life Advice:
{json.dumps(all_wisdom['life_advice'][:20], indent=2)}

Mindset Shifts:
{json.dumps(all_wisdom['mindset_shifts'][:20], indent=2)}

{"Focus on topic: " + topic if topic else ""}

Create a synthesized wisdom guide with:
1. Core principles (3-5)
2. Key practices (3-5)
3. Common pitfalls to avoid
4. Integration strategies

Respond in JSON format."""

        response = self.llm_client.query(prompt, model='analysis')
        
        try:
            return json.loads(response)
        except:
            return {
                'core_principles': ['Examine life deeply', 'Question assumptions', 'Seek practical wisdom'],
                'key_practices': ['Daily reflection', 'Socratic questioning', 'Mindful action']
            }
    
    def _identify_patterns(self, episodes: List) -> List[Dict[str, Any]]:
        """Identify philosophical patterns across episodes"""
        # Collect argument structures
        all_arguments = []
        for ep in episodes:
            if hasattr(ep, 'arguments'):
                all_arguments.extend(ep.arguments)
        
        # Collect recurring themes
        theme_frequency = defaultdict(int)
        for ep in episodes:
            for theme in ep.connections.get('recurring_themes', []):
                theme_frequency[theme] += 1
        
        # Find patterns
        patterns = []
        
        # Pattern 1: Common argument structures
        if all_arguments:
            patterns.append({
                'pattern_type': 'argument_structure',
                'description': 'Recurring logical patterns in philosophical arguments',
                'frequency': len(all_arguments),
                'examples': all_arguments[:3]
            })
        
        # Pattern 2: Thematic patterns
        top_themes = sorted(theme_frequency.items(), key=lambda x: x[1], reverse=True)[:5]
        if top_themes:
            patterns.append({
                'pattern_type': 'thematic_recurrence',
                'description': 'Themes that appear across multiple episodes',
                'top_themes': [{'theme': t, 'count': c} for t, c in top_themes]
            })
        
        # Pattern 3: Conceptual patterns using LLM
        concept_sample = []
        for ep in episodes[:10]:
            concepts = ep.philosophical_content.get('concepts_explored', [])
            concept_sample.extend([c.get('concept', '') for c in concepts[:2]])
        
        if concept_sample:
            prompt = f"""Identify philosophical patterns in these concepts:
{json.dumps(concept_sample)}

Find patterns like:
- Conceptual hierarchies
- Opposing pairs
- Cultural influences
- Philosophical traditions

Respond with a JSON array of patterns."""

            try:
                llm_patterns = json.loads(self.llm_client.query(prompt, model='analysis'))
                patterns.extend(llm_patterns)
            except:
                pass
        
        return patterns
    
    def _find_contradictions(self, episodes: List) -> List[Dict[str, Any]]:
        """Find contradictions and paradoxes across episodes"""
        contradictions = []
        
        # Collect all stated positions
        positions = []
        for ep in episodes[:10]:  # Limit for analysis
            summary = ep.content_analysis.get('summary', {}).get('brief', '')
            main_thesis = ep.content_analysis.get('main_thesis', '')
            positions.append({
                'episode': ep.title,
                'position': f"{summary} {main_thesis}"
            })
        
        # Use LLM to find contradictions
        prompt = f"""Analyze these philosophical positions for contradictions, tensions, or paradoxes:

{json.dumps(positions, indent=2)}

Identify:
1. Direct contradictions between episodes
2. Philosophical tensions or paradoxes
3. Evolving views that seem contradictory
4. Dialectical oppositions

For each finding, provide:
- type (contradiction/tension/paradox/dialectic)
- episodes_involved
- description
- philosophical_significance

Respond as a JSON array."""

        response = self.llm_client.query(prompt, model='analysis')
        
        try:
            contradictions = json.loads(response)
        except:
            contradictions = []
        
        return contradictions
    
    def _extract_unique_contributions(self, episodes: List) -> List[Dict[str, Any]]:
        """Extract unique philosophical contributions"""
        unique_insights = []
        
        # Collect unique insights from episodes
        for ep in episodes:
            if ep.unique_insights:
                for insight in ep.unique_insights[:2]:  # Top 2 from each
                    unique_insights.append({
                        'insight': insight,
                        'episode': ep.title,
                        'context': ep.content_analysis.get('primary_topic', '')
                    })
        
        # Use LLM to identify truly unique contributions
        if unique_insights:
            prompt = f"""From these insights, identify the most unique and valuable philosophical contributions:

{json.dumps(unique_insights[:20], indent=2)}

Select 5-10 insights that:
1. Offer genuinely novel perspectives
2. Challenge conventional thinking
3. Provide practical value
4. Bridge different philosophical traditions

For each, explain why it's uniquely valuable.

Respond as a JSON array with: insight, episode, uniqueness_reason, practical_value"""

            response = self.llm_client.query(prompt, model='analysis')
            
            try:
                return json.loads(response)
            except:
                return unique_insights[:5]
        
        return []
    
    def _compile_practical_applications(self, episodes: List, topic: Optional[str]) -> Dict[str, Any]:
        """Compile practical applications of philosophical ideas"""
        applications = {
            'daily_practices': [],
            'decision_frameworks': [],
            'mindset_tools': [],
            'life_experiments': []
        }
        
        # Collect practical elements
        for ep in episodes:
            wisdom = ep.practical_wisdom
            if wisdom.get('implementation_tips'):
                applications['daily_practices'].extend(wisdom['implementation_tips'])
            if wisdom.get('life_advice'):
                applications['mindset_tools'].extend(wisdom['life_advice'])
        
        # Synthesize into actionable framework
        prompt = f"""Create a practical application framework from this philosophical wisdom:

Daily Practices:
{json.dumps(applications['daily_practices'][:10], indent=2)}

Mindset Tools:
{json.dumps(applications['mindset_tools'][:10], indent=2)}

{"Focus on applications for: " + topic if topic else ""}

Design:
1. A 30-day practice plan
2. Decision-making frameworks
3. Thought experiments
4. Integration strategies

Make it practical and actionable.

Respond in JSON format with keys: thirty_day_plan, decision_frameworks, experiments, integration_tips"""

        response = self.llm_client.query(prompt, model='analysis')
        
        try:
            return json.loads(response)
        except:
            return applications
    
    def _generate_meta_insights(self, insights: Dict[str, Any]) -> List[str]:
        """Generate meta-level insights about the insights"""
        prompt = f"""Based on this philosophical analysis across multiple episodes:

Thematic Evolution: {len(insights.get('thematic_evolution', []))} patterns identified
Philosophical Patterns: {len(insights.get('philosophical_patterns', []))} patterns found
Contradictions: {len(insights.get('contradictions_paradoxes', []))} tensions identified
Unique Contributions: {len(insights.get('unique_contributions', []))} novel insights

Generate 3-5 meta-insights about:
1. The overall philosophical approach of the podcast
2. Unique contributions to philosophical discourse
3. Practical value for listeners
4. Areas for deeper exploration

Provide as a JSON array of insight strings."""

        response = self.llm_client.query(prompt, model='analysis')
        
        try:
            return json.loads(response)
        except:
            return [
                "The podcast bridges academic philosophy with practical life application",
                "Emphasis on making complex ideas accessible through examples",
                "Regular integration of Eastern and Western philosophical traditions"
            ]