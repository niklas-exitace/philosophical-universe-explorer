"""Caching system for Project Simone"""

import json
import pickle
import logging
from pathlib import Path
from typing import Any, Optional
from datetime import datetime, timedelta
import hashlib

logger = logging.getLogger(__name__)


class Cache:
    """Simple file-based cache for LLM responses and analysis results"""
    
    def __init__(self, cache_dir: Path, ttl_days: int = 30):
        """Initialize cache with directory and time-to-live"""
        self.cache_dir = Path(cache_dir)
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        self.ttl = timedelta(days=ttl_days)
        
        logger.info(f"Cache initialized at {self.cache_dir} with TTL={ttl_days} days")
    
    def get(self, key: str) -> Optional[Any]:
        """Retrieve item from cache"""
        cache_file = self._get_cache_path(key)
        
        if not cache_file.exists():
            return None
        
        try:
            # Check if cache is expired
            if self._is_expired(cache_file):
                logger.debug(f"Cache expired for key: {key}")
                cache_file.unlink()
                return None
            
            # Load from cache
            with open(cache_file, 'rb') as f:
                data = pickle.load(f)
                logger.debug(f"Cache hit for key: {key}")
                return data
                
        except Exception as e:
            logger.error(f"Error reading cache for key {key}: {e}")
            return None
    
    def set(self, key: str, value: Any) -> None:
        """Store item in cache"""
        cache_file = self._get_cache_path(key)
        
        try:
            with open(cache_file, 'wb') as f:
                pickle.dump(value, f)
                logger.debug(f"Cached data for key: {key}")
                
        except Exception as e:
            logger.error(f"Error writing cache for key {key}: {e}")
    
    def delete(self, key: str) -> None:
        """Delete item from cache"""
        cache_file = self._get_cache_path(key)
        
        if cache_file.exists():
            cache_file.unlink()
            logger.debug(f"Deleted cache for key: {key}")
    
    def clear(self) -> None:
        """Clear all cache files"""
        count = 0
        for cache_file in self.cache_dir.glob("*.pkl"):
            cache_file.unlink()
            count += 1
        
        logger.info(f"Cleared {count} cache files")
    
    def cleanup_expired(self) -> int:
        """Remove expired cache files"""
        count = 0
        for cache_file in self.cache_dir.glob("*.pkl"):
            if self._is_expired(cache_file):
                cache_file.unlink()
                count += 1
        
        logger.info(f"Cleaned up {count} expired cache files")
        return count
    
    def get_stats(self) -> dict:
        """Get cache statistics"""
        cache_files = list(self.cache_dir.glob("*.pkl"))
        total_size = sum(f.stat().st_size for f in cache_files)
        
        expired_count = sum(1 for f in cache_files if self._is_expired(f))
        
        return {
            'total_files': len(cache_files),
            'total_size_mb': round(total_size / (1024 * 1024), 2),
            'expired_files': expired_count,
            'cache_directory': str(self.cache_dir)
        }
    
    def _get_cache_path(self, key: str) -> Path:
        """Generate cache file path from key"""
        # Create safe filename from key
        safe_key = hashlib.md5(key.encode()).hexdigest()
        return self.cache_dir / f"{safe_key}.pkl"
    
    def _is_expired(self, cache_file: Path) -> bool:
        """Check if cache file is expired"""
        mtime = datetime.fromtimestamp(cache_file.stat().st_mtime)
        return datetime.now() - mtime > self.ttl


class JSONCache(Cache):
    """JSON-based cache for human-readable storage"""
    
    def get(self, key: str) -> Optional[Any]:
        """Retrieve item from JSON cache"""
        cache_file = self._get_cache_path(key)
        
        if not cache_file.exists():
            return None
        
        try:
            if self._is_expired(cache_file):
                cache_file.unlink()
                return None
            
            with open(cache_file, 'r', encoding='utf-8') as f:
                return json.load(f)
                
        except Exception as e:
            logger.error(f"Error reading JSON cache for key {key}: {e}")
            return None
    
    def set(self, key: str, value: Any) -> None:
        """Store item in JSON cache"""
        cache_file = self._get_cache_path(key)
        
        try:
            with open(cache_file, 'w', encoding='utf-8') as f:
                json.dump(value, f, ensure_ascii=False, indent=2)
                
        except Exception as e:
            logger.error(f"Error writing JSON cache for key {key}: {e}")
    
    def _get_cache_path(self, key: str) -> Path:
        """Generate cache file path from key"""
        safe_key = hashlib.md5(key.encode()).hexdigest()
        return self.cache_dir / f"{safe_key}.json"