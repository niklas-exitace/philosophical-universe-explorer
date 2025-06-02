"""LLM client for interacting with various language models"""

import logging
from typing import Dict, Any, Optional, List
import json
import openai
import tiktoken

logger = logging.getLogger(__name__)


class LLMClient:
    """Unified client for interacting with LLMs"""
    
    def __init__(self, config):
        """Initialize LLM client with configuration"""
        self.config = config
        
        # Set OpenAI API key
        openai.api_key = config.api.openai_key
        
        # Initialize tokenizer
        try:
            self.encoding = tiktoken.encoding_for_model("gpt-4")
        except:
            self.encoding = tiktoken.get_encoding("cl100k_base")
        
        # Model mapping
        self.models = {
            'analysis': config.api.openai_models.get('analysis', 'gpt-4o-mini'),
            'qa': config.api.openai_models.get('qa', 'gpt-4o'),
            'embedding': config.api.openai_models.get('embedding', 'text-embedding-3-small')
        }
        
        logger.info(f"LLM Client initialized with models: {self.models}")
    
    def query(self, prompt: str, model: str = 'analysis', temperature: float = 0.7, 
              max_tokens: Optional[int] = None) -> str:
        """Query an LLM with a prompt"""
        model_name = self.models.get(model, model)
        
        logger.debug(f"Querying {model_name} with prompt length: {len(prompt)}")
        
        try:
            # Check if it's a chat model
            if 'gpt-4' in model_name or 'gpt-3.5' in model_name:
                response = openai.ChatCompletion.create(
                    model=model_name,
                    messages=[
                        {"role": "system", "content": "You are an expert philosophical analyst with deep knowledge of philosophy, logic, and practical wisdom."},
                        {"role": "user", "content": prompt}
                    ],
                    temperature=temperature,
                    max_tokens=max_tokens
                )
                return response.choices[0].message.content
            else:
                # Use completion API for older models
                response = openai.Completion.create(
                    model=model_name,
                    prompt=prompt,
                    temperature=temperature,
                    max_tokens=max_tokens or 2000
                )
                return response.choices[0].text.strip()
            
        except Exception as e:
            logger.error(f"Error querying LLM: {e}")
            raise
    
    def query_json(self, prompt: str, model: str = 'analysis') -> Dict[str, Any]:
        """Query LLM and parse JSON response"""
        response = self.query(prompt + "\n\nRespond only with valid JSON.", model, temperature=0.3)
        
        try:
            # Try to extract JSON from response
            if "```json" in response:
                json_str = response.split("```json")[1].split("```")[0].strip()
            elif "```" in response:
                json_str = response.split("```")[1].split("```")[0].strip()
            else:
                json_str = response.strip()
            
            return json.loads(json_str)
        except Exception as e:
            logger.error(f"Failed to parse JSON response: {e}")
            logger.debug(f"Response was: {response[:500]}")
            return {}
    
    def embed(self, text: str) -> List[float]:
        """Generate embeddings for text"""
        try:
            response = openai.Embedding.create(
                model=self.models['embedding'],
                input=text
            )
            return response['data'][0]['embedding']
        except Exception as e:
            logger.error(f"Error generating embedding: {e}")
            raise
    
    def chunk_text(self, text: str, chunk_size: int = 4000, overlap: int = 200) -> List[str]:
        """Split text into chunks for processing"""
        tokens = self.encoding.encode(text)
        chunks = []
        
        start = 0
        while start < len(tokens):
            end = start + chunk_size
            chunk_tokens = tokens[start:end]
            chunk_text = self.encoding.decode(chunk_tokens)
            chunks.append(chunk_text)
            start = end - overlap
        
        return chunks
    
    def count_tokens(self, text: str) -> int:
        """Count tokens in text"""
        return len(self.encoding.encode(text))
    
    def stream_query(self, prompt: str, model: str = 'analysis', on_token=None):
        """Stream response from LLM"""
        model_name = self.models.get(model, model)
        
        try:
            # Note: The old OpenAI API doesn't support streaming in the same way
            # We'll simulate streaming by returning the full response
            response = self.query(prompt, model)
            
            if on_token:
                # Simulate streaming by calling on_token for each word
                words = response.split()
                for i, word in enumerate(words):
                    if i > 0:
                        on_token(' ')
                    on_token(word)
            
            return response
            
        except Exception as e:
            logger.error(f"Error in streaming query: {e}")
            raise