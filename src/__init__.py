"""
Project Simone: Intelligent Philosophical Content Analysis System
"""

__version__ = "0.1.0"
__author__ = "Project Simone Team"

from .core.engine import SimoneEngine
from .core.config import Config

__all__ = ["SimoneEngine", "Config"]