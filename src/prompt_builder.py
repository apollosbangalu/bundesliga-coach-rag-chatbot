"""
This is the Prompt Builder Module

Purpose: This constructs the final LLM prompt - with system prompt, user question, 
and retrieved contextual information.

The challenge document specified these requirements:
- Output must be a string involving the final prompt for an LLM
- Must involve system prompt for the LLM
- Must involve user question
- Must involve additional retrieved information.
"""

#required imports
import logging
from typing import Optional


class PromptBuilder:
    """
    This class builds complete prompt for LLM.
    
    The challenge document specified these requirements:
    The output must be "A string that involves the final prompt for an LLM. 
    This should involve the system prompt for the llm, the user question 
    and the additional retrieved information."
    """
    
    def __init__(self, logger: logging.Logger):
        """
        Initialize prompt builder.
        
        Args:
            logger: Logger instance for debugging
        """
        self.logger = logger
        
    def build_prompt(
        self,
        user_question: str,
        club_name: str,
        city: str,
        coach_name: str,
        coach_intro: Optional[str]
    ) -> str:
        """
        Build final prompt string for LLM.
        
        The challenge document specified these requirements:
        1. System prompt for the LLM
        2. User question
        3. Additional retrieved information
        
        Args:
            user_question: Original user question (input string)
            club_name: Name of the football club
            city: City name
            coach_name: Name of the current coach
            coach_intro: Biographical information from Wikipedia (can be None)
            
        Returns:
            Complete prompt string ready for LLM consumption
        """
        self.logger.info("Building LLM prompt")
        
        # System prompt - defines LLM's role and instructions
        system_prompt = self._get_system_prompt()
        
        # Context section - retrieved information from Wikidata and Wikipedia
        context = self._build_context(club_name, city, coach_name, coach_intro)
        
        # Combine all components into final prompt
        # Structure: System Prompt -> Retrieved Context -> User Question
        final_prompt = f"""{system_prompt}

RETRIEVED CONTEXT:
{context}

USER QUESTION:
{user_question}

Please answer the user's question using the provided context."""
        
        self.logger.debug(f"Built prompt ({len(final_prompt)} chars)")
        self.logger.debug(f"Full prompt:\n{final_prompt}")
        
        return final_prompt
    
    def _get_system_prompt(self) -> str:
        """
        Generate system prompt for the LLM.
        
        Defines the chatbot's role and behavior per challenge scenario:
        - Chatbot is about football clubs in Germany
        - Answers questions about coaches
        - Uses retrieved information
        
        Returns:
            System prompt string
        """
        return """SYSTEM PROMPT:
You are a helpful assistant an expert in Germany`s 1. Bundesliga football (soccer).
You answer questions about coaches of clubs in Germany's 1. Bundesliga.
You must use only the information provided in the retrieved context below. You must never assume.
Be concise but informative in your responses.
Provide the coach's name and relevant information about them."""
    
    def _build_context(
        self,
        club_name: str,
        city: str,
        coach_name: str,
        coach_intro: Optional[str]
    ) -> str:
        """
        Build context section with retrieved information.
        
        This is the "additional retrieved information" mentioned in 
        the challenge requirements.
        
        Args:
            club_name: Club name from Wikidata
            city: City name from Wikidata
            coach_name: Coach name from Wikidata
            coach_intro: Coach biography from Wikipedia
            
        Returns:
            Formatted context string
        """
        # Build context with retrieved data
        context_parts = [
            f"City: {city}",
            f"Club: {club_name}",
            f"Current Coach: {coach_name}"
        ]
        
        # Add Wikipedia intro if available
        if coach_intro:
            context_parts.append(f"\nCoach Information from Wikipedia:\n{coach_intro}")
        else:
            # Handle case where Wikipedia intro is not available
            context_parts.append("\nCoach Information: No additional biographical information available from Wikipedia.")
            
        return "\n".join(context_parts)