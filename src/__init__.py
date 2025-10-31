"""
Source package for Germany`s 1. Bundesliga RAG-Chatbot Coach Information System

This package contains all modules for the RAG-Chatbot system:
- logger_config: this is for Logging configuration
- entity_extractor: this is for Entity extraction from user queries
- wikidata_client: this is for Wikidata SPARQL queries
- wikipedia_client: this is for Wikipedia API client
- prompt_builder: this is for LLM prompt construction
"""
#required imports
from src.logger_config import setup_logger
from src.entity_extractor import EntityExtractor
from src.wikidata_client import WikidataClient
from src.wikipedia_client import WikipediaClient
from src.wikipedia_client_alternative import WikipediaClient
from src.prompt_builder import PromptBuilder

__all__ = [
    'setup_logger',
    'EntityExtractor',
    'WikidataClient',
    'WikipediaClient',
    'PromptBuilder'
]

__version__ = '1.0.0'
__author__ = 'Bangalu Apollos Yohanna'
__doc__ = 'for Pantopix code challenge - 30th October, 2025'