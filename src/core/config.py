"""Configuration management for Project Simone"""

import os
import yaml
from pathlib import Path
from typing import Dict, Any, Optional
from dataclasses import dataclass, field
import logging

logger = logging.getLogger(__name__)


@dataclass
class APIConfig:
    """API configuration settings"""
    openai_key: str = ""
    anthropic_key: str = ""
    openai_models: Dict[str, str] = field(default_factory=dict)
    anthropic_models: Dict[str, str] = field(default_factory=dict)


@dataclass
class PathConfig:
    """Path configuration settings"""
    raw_transcripts: Path
    existing_analysis: Path
    cache_dir: Path
    processed_dir: Path
    exports_dir: Path
    
    def __post_init__(self):
        """Convert string paths to Path objects"""
        self.raw_transcripts = Path(self.raw_transcripts)
        self.existing_analysis = Path(self.existing_analysis)
        self.cache_dir = Path(self.cache_dir)
        self.processed_dir = Path(self.processed_dir)
        self.exports_dir = Path(self.exports_dir)


@dataclass
class AnalysisConfig:
    """Analysis configuration settings"""
    chunk_size: int = 4000
    overlap: int = 200
    max_retries: int = 3
    batch_size: int = 5
    cache_enabled: bool = True
    depth_levels: Dict[str, Dict] = field(default_factory=dict)


class Config:
    """Main configuration class for Project Simone"""
    
    def __init__(self, config_path: Optional[str] = None):
        """Initialize configuration from YAML file"""
        if config_path is None:
            config_path = Path(__file__).parent.parent.parent / "config" / "settings.yaml"
        
        self.config_path = Path(config_path)
        self._raw_config = self._load_config()
        
        # Initialize sub-configurations
        self.api = self._parse_api_config()
        self.paths = self._parse_path_config()
        self.analysis = self._parse_analysis_config()
        self.philosophy = self._raw_config.get("philosophy", {})
        self.interface = self._raw_config.get("interface", {})
        self.processing = self._raw_config.get("processing", {})
        self.logging = self._raw_config.get("logging", {})
        
        # Set up logging
        self._setup_logging()
        
        # Create necessary directories
        self._create_directories()
    
    def _load_config(self) -> Dict[str, Any]:
        """Load configuration from YAML file"""
        if not self.config_path.exists():
            raise FileNotFoundError(f"Configuration file not found: {self.config_path}")
        
        with open(self.config_path, 'r') as f:
            return yaml.safe_load(f)
    
    def _parse_api_config(self) -> APIConfig:
        """Parse API configuration"""
        api_config = self._raw_config.get("api", {})
        
        return APIConfig(
            openai_key=api_config.get("openai", {}).get("api_key", ""),
            anthropic_key=api_config.get("anthropic", {}).get("api_key", ""),
            openai_models=api_config.get("openai", {}).get("models", {}),
            anthropic_models=api_config.get("anthropic", {}).get("models", {})
        )
    
    def _parse_path_config(self) -> PathConfig:
        """Parse path configuration"""
        path_config = self._raw_config.get("paths", {})
        
        # Convert relative paths to absolute paths based on project root
        project_root = Path(__file__).parent.parent.parent
        
        def resolve_path(path_str: str) -> Path:
            path = Path(path_str)
            if not path.is_absolute():
                # If path starts with .., resolve from project root's parent
                if path_str.startswith(".."):
                    return (project_root.parent / path).resolve()
                else:
                    return (project_root / path).resolve()
            return path
        
        return PathConfig(
            raw_transcripts=resolve_path(path_config.get("raw_transcripts", "data/raw")),
            existing_analysis=resolve_path(path_config.get("existing_analysis", "data/processed")),
            cache_dir=resolve_path(path_config.get("cache_dir", "data/cache")),
            processed_dir=resolve_path(path_config.get("processed_dir", "data/processed")),
            exports_dir=resolve_path(path_config.get("exports_dir", "data/exports"))
        )
    
    def _parse_analysis_config(self) -> AnalysisConfig:
        """Parse analysis configuration"""
        analysis_config = self._raw_config.get("analysis", {})
        
        return AnalysisConfig(
            chunk_size=analysis_config.get("chunk_size", 4000),
            overlap=analysis_config.get("overlap", 200),
            max_retries=analysis_config.get("max_retries", 3),
            batch_size=analysis_config.get("batch_size", 5),
            cache_enabled=analysis_config.get("cache_enabled", True),
            depth_levels=analysis_config.get("depth_levels", {})
        )
    
    def _setup_logging(self):
        """Set up logging configuration"""
        log_config = self.logging
        log_level = getattr(logging, log_config.get("level", "INFO"))
        log_format = log_config.get("format", "%(asctime)s - %(name)s - %(levelname)s - %(message)s")
        
        # Create logs directory if needed
        log_file = log_config.get("file", "logs/simone.log")
        if log_file:
            log_path = Path(log_file)
            if not log_path.is_absolute():
                log_path = Path(__file__).parent.parent.parent / log_path
            log_path.parent.mkdir(parents=True, exist_ok=True)
            
            logging.basicConfig(
                level=log_level,
                format=log_format,
                handlers=[
                    logging.FileHandler(log_path),
                    logging.StreamHandler()
                ]
            )
        else:
            logging.basicConfig(level=log_level, format=log_format)
    
    def _create_directories(self):
        """Create necessary directories if they don't exist"""
        directories = [
            self.paths.cache_dir,
            self.paths.processed_dir,
            self.paths.exports_dir
        ]
        
        for directory in directories:
            directory.mkdir(parents=True, exist_ok=True)
            logger.debug(f"Ensured directory exists: {directory}")
    
    def get(self, key: str, default: Any = None) -> Any:
        """Get configuration value by dot-notation key"""
        keys = key.split('.')
        value = self._raw_config
        
        for k in keys:
            if isinstance(value, dict) and k in value:
                value = value[k]
            else:
                return default
        
        return value
    
    def __repr__(self) -> str:
        return f"Config(config_path={self.config_path})"