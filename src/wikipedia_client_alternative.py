"""
This is an alternative approach for the Wikipedia API Client Module.
I realised that sometimes the direct Wikipedia API fails.

This alternative implementation uses the wikipedia-api package from python library.
To use this version you must do the following steps:
1. Install: pip install wikipedia-api (or use pipenv)
2. Replace the import statement in main.py:
   
   change - "from src.wikipedia_client import WikipediaClient" 
   
   to

   "from src.wikipedia_client_alternative import WikipediaClient"

Purpose: This retrieves coach biographical information from Wikipedia.

The challenge document specified these requirements:
- Information about coach must come from introductory information of Wikipedia article
- This must be retrieved on EVERY question
- Handle missing articles gracefully
"""

#required imports
import logging
from typing import Optional, Dict

try:
    import wikipediaapi
    WIKIPEDIAAPI_AVAILABLE = True
except ImportError:
    WIKIPEDIAAPI_AVAILABLE = False


class WikipediaClient:
    """
    This class is for retrieving information from Wikipedia using wikipedia-api library.
    
    The challenge document specified these requirements:
    - "Information about the coach should come from the introductory information of their 
      respective Wikipedia article"
    - "This information must be retrieved on every question"
    
    Note: This implementation uses the wikipedia-api library which handles
    User-Agent requirements automatically.
    """
    
    def __init__(self, logger: logging.Logger):
        """
        Initialize Wikipedia client.
        
        Args:
            logger: Logger instance for debugging false answers
            
        Raises:
            ImportError: If wikipedia-api package is not installed
        """
        self.logger = logger
        # an error feedback if the wikipedia-api python package is not installed 
        if not WIKIPEDIAAPI_AVAILABLE:
            error_msg = "wikipedia-api package not installed. Install with: pip install wikipedia-api"
            self.logger.error(error_msg)
            raise ImportError(error_msg)
        
        # Initialize Wikipedia API client
        # Based on the wikipedia-api documentation: user_agent format should be 'ProjectName (contact@example.com)'
        self.wiki = wikipediaapi.Wikipedia(
            user_agent='BundesligaCoachRAGChatbot/1.0 (https://github.com/apollosbangalu/bundesliga-coach-rag-chatbot)',
            language='en'
        )
        
        self.logger.info("Wikipedia client initialized with wikipedia-api library")
        
    def get_coach_intro(self, coach_name: str) -> Optional[str]:
        """
        This function retrieves introductory information paragraph from coach's Wikipedia article.
        
        The challenge document specified these requirements:
        - This will be called on every user question
        - The information must be from the introductory information of the Wikipedia article
        
        Args:
            coach_name: Name of the coach
            
        Returns:
            Introduction text from Wikipedia article
            None if article not found or error occurs
        """
        self.logger.info(f"Retrieving Wikipedia intro for coach: {coach_name}")
        
        try:
            # Get Wikipedia page
            page = self.wiki.page(coach_name)
            
            # Log request for debugging
            self.logger.debug(f"Wikipedia page request for: {coach_name}")
            
            # Check if page exists
            if not page.exists():
                self.logger.warning(f"Wikipedia page not found for: {coach_name}")
                return None
            
            # Get summary (introduction section)
            summary = page.summary
            
            if summary:
                self.logger.info(f"Retrieved intro text ({len(summary)} chars)")
                self.logger.debug(f"Intro text preview: {summary[:200]}...")
                return summary.strip()
            else:
                self.logger.warning(f"No summary available for: {coach_name}")
                return None
                
        except Exception as e:
            self.logger.error(f"Error retrieving Wikipedia data: {str(e)}", exc_info=True)
            return None