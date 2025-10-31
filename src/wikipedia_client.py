"""
This is the Wikipedia API Client Module

Purpose: This module retrieves coach introductory biographical information from Wikipedia.

The challenge document specified these requirements:
- Information about coach must come from introductory information of the respective Wikipedia article
- This information must be retrieved on EVERY question
- Handle missing articles gracefully
"""

#required imports
import logging
import requests
from typing import Optional, Dict


class WikipediaClient:
    """
    This is the client for retrieving coach introductory biographical information from Wikipedia.
    
    The challenge document specified these requirements:
    - "Information about the coach should come from the introductory information of their 
      respective Wikipedia article"
    - "This information must be retrieved on EVERY question"
    """
    
    WIKIPEDIA_API_URL = "https://en.wikipedia.org/w/api.php" #this is the api url for wikipedia
    
    def __init__(self, logger: logging.Logger):
        """
        Initializing the Wikipedia client.
        
        Args:
            logger: Logger instance for debugging false answers
        """
        self.logger = logger
        
    def get_coach_intro(self, coach_name: str) -> Optional[str]:
        """
        This retrieves the introductory paragraph from coach's Wikipedia article.
        
        The challenge document specified these requirements:
        - This information must be retrieved on EVERY question
        - Information about coach must come from introductory information of the respective Wikipedia article
        
        Args:
            coach_name: Name of the coach
            
        Returns:
            Introduction text from Wikipedia article
            None if article not found or error occurs
        """
        self.logger.info(f"Retrieving Wikipedia introductory information for coach: {coach_name}")
        
        #The followwing are parameters of wikipedia API
        # Wikipedia API parameters for getting page extract (introductory information section)
        # extracts: Get page content extracts
        # exintro: Only return content before first section
        # explaintext: Return plain text instead of HTML
        # redirects: Follow redirects automatically
        params = {
            "action": "query",
            "format": "json",
            "titles": coach_name,
            "prop": "extracts",
            "exintro": True,      # Only introduction section
            "explaintext": True,  # Plain text, no HTML formatting
            "redirects": 1        # Follow redirects
        }
        
        # The required User-Agent header by Wikipedia API
        # Format: Application/Version (Contact Information)
        headers = {
            "User-Agent": "BundesligaCoachRAGChatbot/1.0 (https://github.com/user/bundesliga-coach-rag-chatbot; contact@example.com)"
        }
        
        self.logger.debug(f"Wikipedia API request params: {params}")
        self.logger.debug(f"Wikipedia API request headers: {headers}")
        
        try:
            # Make request to Wikipedia API with proper User-Agent
            response = requests.get(
                self.WIKIPEDIA_API_URL, 
                params=params,
                headers=headers,
                timeout=10  # 10 second timeout
            )
            response.raise_for_status()
            data = response.json()
            
            # Log raw response for debugging false answers
            self.logger.debug(f"Raw Wikipedia response: {data}")
            
            # Extract introductory information text from response
            intro_text = self._extract_intro_from_response(data)
            
            if intro_text:
                self.logger.info(f"Retrieved introductory information text ({len(intro_text)} chars)")
                # Log first 200 chars for debugging without flooding logs
                self.logger.debug(f"introductory information text preview: {intro_text[:200]}...")
            else:
                self.logger.warning(f"No introductory information text found for coach: {coach_name}")
                
            return intro_text
            
        except requests.Timeout:
            self.logger.error(f"Wikipedia API request timed out for: {coach_name}")
            return None
        except requests.RequestException as e:
            self.logger.error(f"Error retrieving Wikipedia data: {str(e)}")
            return None
        except Exception as e:
            self.logger.error(f"Unexpected error processing Wikipedia data: {str(e)}", exc_info=True)
            return None
    
    def _extract_intro_from_response(self, data: Dict) -> Optional[str]:
        """
        Extract introductory information text from Wikipedia API response.
        
        Wikipedia API response structure:
        {
            "query": {
                "pages": {
                    "page_id": {
                        "title": "...",
                        "extract": "introductory information text here"
                    }
                }
            }
        }
        
        Args:
            data: Raw JSON response from Wikipedia API
            
        Returns:
            Extracted intro text or None
        """
        try:
            # Navigate and scan through response structure
            query = data.get('query', {})
            pages = query.get('pages', {})
            
            # The Pages are a dictionary with page IDs as keys
            # First get the page (and should be only)
            for page_id, page_data in pages.items():
                # Check if page exists (page_id != -1 means page found)
                if page_id == '-1':
                    self.logger.debug("Wikipedia page not found (page_id=-1)")
                    return None
                
                # Extract the introductory information text
                extract = page_data.get('extract', '')
                
                if extract:
                    return extract.strip()
            
            return None
            
        except Exception as e:
            self.logger.warning(f"Error extracting introductory information from response: {str(e)}")
            return None