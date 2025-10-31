"""
This is the Entity Extractor Module

Purpose: This module extracts city/club identifiers from user questions and 
handles case-insensitive matching and colloquial phrasing.

The challenge document specified these requirements:
- Applies a case-insensitive approach for city names (Berlin, berlin, BERLIN all work)
- Ensusre that entities are extracted from various colloquial question formats as specified in the challenge document
- Ensure that special cases: "Pauli" or "pauli" maps to FC St. Pauli
"""

#required imports
import logging
import re
from typing import Optional


class EntityExtractor:
    """
    This class extracts city/club identifiers from user questions.
    
    It also Handles the challenge requirements to process colloquial questions like:
    - "Who is coaching Berlin?"
    - "What about munich?"
    - "Who is heidenheims manager?"
    - "Who is it for Pauli?"
    """
    
    def __init__(self, logger: logging.Logger):
        """
        Initialize entity extractor.
        
        Args:
            logger: Logger instance for debugging
        """
        self.logger = logger
        
    def extract_city(self, user_question: str) -> Optional[str]:
        """
        This extracts city/club identifier from user question.
        
        The challenge document specified these requirements:
        - Handle case insensitivity (user can write city name in any case)
        - Extract city/club entity from colloquial questions
        
        Args:
            user_question: String involving the user question
            
        Returns:
            Normalized (lowercase) city/club identifier, or None if not found
            
        Examples:
            "Who is coaching Berlin?" -> "berlin"
            "What about munich?" -> "munich"
            "Who is heidenheims manager?" -> "heidenheim"
            "Who is it for Pauli?" -> "pauli"
        """
        self.logger.info(f"Extracting entity from: {user_question}")
        
        # Normalize input: lowercase and strip whitespace
        # This handles the requirement: "handle upper- and lowercase"
        normalized_question = user_question.lower().strip()
        
        # Log normalized input for debugging false answers
        self.logger.debug(f"Normalized question: {normalized_question}")
        
        # Extract entity using pattern matching
        extracted_entity = self._extract_entity_logic(normalized_question)
        
        if extracted_entity:
            self.logger.info(f"Extracted entity: {extracted_entity}")
        else:
            self.logger.warning(f"Could not extract entity from: {user_question}")
            
        return extracted_entity
    
    def _extract_entity_logic(self, normalized_question: str) -> Optional[str]:
        """
        The internal logic to extract entity from normalized question.
        
        Based on the challenge document this function implements parsing 
        for all example patterns from the challenge:
        1. "who is coaching [CITY]?" 
        2. "what about [CITY]?"
        3. "who is [CITY]s manager?"
        4. "who is it for [CITY]?"
        
        Args:
            normalized_question: Lowercase, stripped question string
            
        Returns:
            Extracted city/club identifier or None
        """
        # Pattern 1: "coaching [CITY]" or "coach [CITY]"
        # Example: "Who is coaching Berlin?"
        match = re.search(r'coach(?:ing)?\s+(\w+)', normalized_question)
        if match:
            entity = match.group(1)
            self.logger.debug(f"Matched pattern 'coaching [CITY]': {entity}")
            return entity
        
        # Pattern 2: "about [CITY]"
        # Example: "What about munich?"
        match = re.search(r'about\s+(\w+)', normalized_question)
        if match:
            entity = match.group(1)
            self.logger.debug(f"Matched pattern 'about [CITY]': {entity}")
            return entity
        
        # Pattern 3: "[CITY]s manager" or "[CITY] manager"
        # Example: "Who is heidenheims manager?"
        match = re.search(r'(\w+)s?\s+manager', normalized_question)
        if match:
            entity = match.group(1)
            self.logger.debug(f"Matched pattern '[CITY]s manager': {entity}")
            return entity
        
        # Pattern 4: "for [CITY]"
        # Example: "Who is it for Pauli?"
        match = re.search(r'for\s+(\w+)', normalized_question)
        if match:
            entity = match.group(1)
            self.logger.debug(f"Matched pattern 'for [CITY]': {entity}")
            return entity
        
        # Pattern 5: "in [CITY]"
        # Additional common pattern
        match = re.search(r'in\s+(\w+)', normalized_question)
        if match:
            entity = match.group(1)
            self.logger.debug(f"Matched pattern 'in [CITY]': {entity}")
            return entity
        
        # If no patterns match, try to find any word that could be a city name
        # Look for capitalized words or longer words (likely proper nouns)
        # in the original question before normalization
        self.logger.debug("No standard pattern matched, attempting fallback extraction")
        return None