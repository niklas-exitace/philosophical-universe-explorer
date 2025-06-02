"""Advanced philosophical content analyzer using LLMs"""

import json
import logging
from typing import Dict, List, Any, Optional
from datetime import datetime

logger = logging.getLogger(__name__)


class PhilosophicalAnalyzer:
    """Analyzes philosophical content using advanced LLM techniques"""
    
    def __init__(self, llm_client, cache):
        """Initialize the analyzer"""
        self.llm_client = llm_client
        self.cache = cache
        
    def analyze(self, content: str, metadata: Dict, depth_config: Optional[Dict] = None) -> Dict[str, Any]:
        """Perform comprehensive philosophical analysis"""
        logger.info(f"Analyzing content: {metadata.get('title', 'Unknown')}")
        
        # Check cache first
        cache_key = self._generate_cache_key(content, metadata, depth_config)
        cached_result = self.cache.get(cache_key)
        if cached_result:
            logger.info("Using cached analysis result")
            return cached_result
        
        # Determine analysis depth
        if depth_config is None:
            depth_config = {
                'passes': 2,
                'focus': ['topics', 'concepts', 'arguments', 'wisdom']
            }
        
        # Perform multi-pass analysis
        analysis_results = {}
        
        for pass_num in range(depth_config['passes']):
            logger.info(f"Analysis pass {pass_num + 1}/{depth_config['passes']}")
            
            if 'topics' in depth_config['focus']:
                analysis_results['content_analysis'] = self._analyze_content(content, metadata)
            
            if 'concepts' in depth_config['focus']:
                analysis_results['philosophical_content'] = self._analyze_philosophy(content, metadata)
            
            if 'arguments' in depth_config['focus']:
                analysis_results['arguments'] = self._analyze_arguments(content)
            
            if 'wisdom' in depth_config['focus']:
                analysis_results['practical_wisdom'] = self._extract_wisdom(content)
            
            if 'connections' in depth_config['focus']:
                analysis_results['connections'] = self._find_connections(content)
            
            if 'contradictions' in depth_config['focus']:
                analysis_results['contradictions'] = self._find_contradictions(content)
            
            if 'meta_analysis' in depth_config['focus'] and pass_num > 0:
                analysis_results['meta_analysis'] = self._meta_analyze(analysis_results)
        
        # Calculate metrics
        analysis_results['episode_metrics'] = self._calculate_metrics(analysis_results)
        
        # Extract unique insights
        analysis_results['unique_insights'] = self._extract_unique_insights(content, analysis_results)
        
        # Cache the result
        self.cache.set(cache_key, analysis_results)
        
        return analysis_results
    
    def _analyze_content(self, content: str, metadata: Dict) -> Dict[str, Any]:
        """Analyze general content structure and themes"""
        prompt = f"""Analyze this philosophical discussion transcript and provide:

1. Primary topic/theme
2. Brief summary (2-3 sentences)
3. Detailed summary (1-2 paragraphs)
4. Hook question that captures the essence
5. Main thesis or argument

Transcript excerpt:
{content[:3000]}...

Respond in JSON format with keys: primary_topic, summary (with brief and detailed), hook_question, main_thesis"""

        response = self.llm_client.query(prompt, model='analysis')
        
        try:
            return json.loads(response)
        except:
            return {
                'primary_topic': 'Philosophy',
                'summary': {
                    'brief': 'Philosophical discussion',
                    'detailed': response
                }
            }
    
    def _analyze_philosophy(self, content: str) -> Dict[str, Any]:
        """Extract philosophical concepts and arguments"""
        prompt = f"""Analyze the philosophical content and extract:

1. Concepts explored (with definitions and practical applications)
2. Philosophical traditions referenced
3. Questions raised (philosophical, practical, rhetorical)
4. Paradoxes or contradictions discussed

Format each concept as:
{{
    "concept": "name",
    "definition_given": "how it's explained",
    "practical_application": "real-world usage",
    "examples_used": ["example1", "example2"]
}}

Transcript excerpt:
{content[:4000]}...

Respond in JSON format."""

        response = self.llm_client.query(prompt, model='analysis')
        
        try:
            return json.loads(response)
        except:
            return {'concepts_explored': [], 'questions_raised': {}}
    
    def _analyze_arguments(self, content: str) -> List[Dict[str, Any]]:
        """Extract and analyze arguments presented"""
        prompt = f"""Identify and analyze arguments in this philosophical discussion:

For each argument, provide:
1. Main claim
2. Supporting premises
3. Evidence or examples used
4. Potential counterarguments mentioned
5. Logical structure (deductive/inductive/abductive)

Transcript excerpt:
{content[:3000]}...

Respond as a JSON array of argument objects."""

        response = self.llm_client.query(prompt, model='analysis')
        
        try:
            return json.loads(response)
        except:
            return []
    
    def _extract_wisdom(self, content: str) -> Dict[str, Any]:
        """Extract practical wisdom and life advice"""
        prompt = f"""Extract practical wisdom and life advice from this discussion:

1. Life advice given
2. Mindset shifts suggested
3. Implementation tips
4. Real-world applications
5. Actionable takeaways

Transcript excerpt:
{content[:3000]}...

Respond in JSON format with keys: life_advice, mindset_shifts, implementation_tips, applications, takeaways"""

        response = self.llm_client.query(prompt, model='analysis')
        
        try:
            return json.loads(response)
        except:
            return {'life_advice': [], 'mindset_shifts': []}
    
    def _find_connections(self, content: str) -> Dict[str, Any]:
        """Find connections to other philosophical ideas and thinkers"""
        prompt = f"""Identify connections in this philosophical discussion:

1. Philosophers mentioned or referenced
2. Philosophical schools/traditions
3. Books or works cited
4. Historical examples used
5. Cross-cultural references

Transcript excerpt:
{content[:3000]}...

Respond in JSON format."""

        response = self.llm_client.query(prompt, model='analysis')
        
        try:
            return json.loads(response)
        except:
            return {'philosophers_mentioned': [], 'traditions': []}
    
    def _find_contradictions(self, content: str) -> List[Dict[str, Any]]:
        """Identify contradictions, paradoxes, and tensions"""
        prompt = f"""Identify contradictions, paradoxes, and philosophical tensions in this discussion:

For each finding:
1. Description of the contradiction/paradox
2. How it's addressed (if at all)
3. Philosophical significance
4. Related philosophical problems

Transcript excerpt:
{content[:3000]}...

Respond as a JSON array."""

        response = self.llm_client.query(prompt, model='analysis')
        
        try:
            return json.loads(response)
        except:
            return []
    
    def _meta_analyze(self, analysis_results: Dict) -> Dict[str, Any]:
        """Perform meta-analysis on the analysis results"""
        prompt = f"""Based on this philosophical analysis, provide meta-insights:

1. Overall philosophical approach/style
2. Depth of analysis (surface/medium/deep)
3. Originality of insights
4. Pedagogical effectiveness
5. Potential blindspots or biases

Analysis data:
{json.dumps(analysis_results, indent=2)[:2000]}...

Respond in JSON format."""

        response = self.llm_client.query(prompt, model='analysis')
        
        try:
            return json.loads(response)
        except:
            return {'approach': 'Unknown', 'depth': 'medium'}
    
    def _extract_unique_insights(self, content: str, analysis: Dict) -> List[str]:
        """Extract unique or surprising insights"""
        concepts_str = json.dumps(analysis.get('philosophical_content', {}).get('concepts_explored', []))
        
        prompt = f"""Based on this philosophical discussion and analysis, identify 3-5 unique, surprising, or particularly insightful points that aren't commonly found in typical discussions of these topics.

Content themes: {analysis.get('content_analysis', {}).get('primary_topic', '')}
Concepts discussed: {concepts_str[:500]}

Transcript excerpt:
{content[:2000]}...

Provide a JSON array of insight strings."""

        response = self.llm_client.query(prompt, model='analysis')
        
        try:
            return json.loads(response)
        except:
            return ["Philosophical insights extracted from discussion"]
    
    def _calculate_metrics(self, analysis: Dict) -> Dict[str, Any]:
        """Calculate various metrics from the analysis"""
        philosophical_content = analysis.get('philosophical_content', {})
        
        # Count concepts
        concepts = philosophical_content.get('concepts_explored', [])
        concepts_count = len(concepts)
        
        # Count arguments
        arguments = analysis.get('arguments', [])
        arguments_count = len(arguments)
        
        # Calculate complexity score (0-10)
        complexity_score = min(10, (concepts_count * 0.5 + arguments_count * 0.3 + 
                                   len(analysis.get('contradictions', [])) * 0.2))
        
        # Determine complexity level
        if complexity_score < 3:
            complexity_level = 'beginner'
        elif complexity_score < 6:
            complexity_level = 'intermediate'
        else:
            complexity_level = 'advanced'
        
        return {
            'concepts_count': concepts_count,
            'arguments_count': arguments_count,
            'unique_insights_count': len(analysis.get('unique_insights', [])),
            'complexity_score': round(complexity_score, 2),
            'complexity_level': complexity_level,
            'practical_advice_count': len(analysis.get('practical_wisdom', {}).get('life_advice', []))
        }
    
    def _generate_cache_key(self, content: str, metadata: Dict, depth_config: Optional[Dict]) -> str:
        """Generate a cache key for the analysis"""
        import hashlib
        
        key_parts = [
            metadata.get('title', ''),
            content[:1000],  # First 1000 chars
            str(depth_config)
        ]
        
        key_string = '|'.join(key_parts)
        return hashlib.md5(key_string.encode()).hexdigest()