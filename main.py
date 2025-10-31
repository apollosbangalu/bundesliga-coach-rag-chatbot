"""
Main Application - Bundesliga Coach RAG System

Purpose: Orchestrate all components for information retrieval in a RAG chatbot
about football clubs in Germany's 1. Bundesliga.

Requirements:
- Console-based interface (input and output via console)
- Input: String involving user question
- Output: String involving final prompt for LLM
- Handle errors gracefully with user-friendly messages
- No actual LLM inference required
"""

#required imports
import logging
from typing import Optional, Dict, List
from src.logger_config import setup_logger
from src.entity_extractor import EntityExtractor
from src.wikidata_client import WikidataClient
from src.wikipedia_client import WikipediaClient
from src.prompt_builder import PromptBuilder


class BundesligaCoachRAGChatbot:
    """
    This is the main application class for the Germany`s 1. Bundesliga Coach RAG-chatbot 
    developed for Pantonix code challenge by Bangalu Apollos Yohanna.
    
    The basic functions of the class is to orchestrates:
    1. Extraction of "Entity" from user input
    2. Data retrieval from Wikidata about - who is coach of the club of a specific city
    3. Data retrieval from Wikipedia about - an introductory information about the coach 
    4. Generation of prompt for a large language  model (LLM)
    
    The basic requirements as contained in the challenge document:
    - Processes user questions in colloquial format
    - Retrieves coach and city information from Wikidata (on every question)
    - Retrieves coach bio from Wikipedia (on every question)
    - Builds prompt with system prompt + context + user question
    """
    
    def __init__(self):
        """Initializing the Germany`s 1. Bundesliga Coach RAG-Chatbot system with all components."""
        # Initialize logger first - used by all other components
        self.logger = setup_logger("BundesligaCoachRAGChatbot")
        self.logger.info("Initializing the Germany`s 1. Bundesliga Coach RAG-Chatbot System")
        
        # Initialize all components
        self.entity_extractor = EntityExtractor(self.logger)
        self.wikidata_client = WikidataClient(self.logger)
        self.wikipedia_client = WikipediaClient(self.logger)
        self.prompt_builder = PromptBuilder(self.logger)
        
        # Cache for  Germany`s 1. Bundesliga clubs
        # The challenge document specified: "Whether you retrieve it on every question or not is up to you"
        # My Decision: I created a cache clubs list to avoid repeated queries (football clubs do not change during session)
        self.clubs_cache: Optional[List[Dict[str, str]]] = None
        
    def initialize_clubs_data(self) -> bool:
        """
        Initializing clubs data from Wikidata.
        
        The challenge document specified these requirements:
        - "Information about which clubs are part of the current season"
        - This can be retrieved once or on every question based on my choice
        
        My Decision: I retrieve once and cache for performance.
        
        Returns:
            True if successful, False otherwise
        """
        try:
            self.logger.info("Initializing Germany`s 1. Bundesliga clubs data from Wikidata")
            self.clubs_cache = self.wikidata_client.get_bundesliga_clubs()
            
            if not self.clubs_cache:
                self.logger.warning("No clubs retrieved from Wikidata")
                return False
                
            self.logger.info(f"Successfully cached {len(self.clubs_cache)} clubs")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to initialize clubs data: {str(e)}", exc_info=True)
            self.clubs_cache = None
            return False
    
    def find_club_by_city(self, city_identifier: str) -> Optional[Dict[str, str]]:
        """
        Find Germany`s 1. Bundesliga club information based on city identifier.
        
        The challenge document specified these requirements:
        - Handle special case (uppercase and lowercase): "Pauli" or "pauli" -> FC St. Pauli
        - Hamburg has two clubs: assume "pauli" for St. Pauli, "hamburg" for HSV
        
        Args:
            city_identifier: Normalized (lowercase) city/club identifier
            
        Returns:
            Club information dict or None if not found
        """
        if not self.clubs_cache:
            self.logger.error("The Clubs and City cache is not initialized")
            return None
        
        self.logger.info(f"Finding club for city identifier: {city_identifier}")
        
        # The special case: "pauli" -> FC St. Pauli
        # Assumption based on challenge document: "you can assume for FC St. Pauli that the user will ask for 'Pauli' or 'pauli'"
        if city_identifier == "pauli":
            self.logger.info("The special case detected: pauli -> FC St. Pauli")
            for club in self.clubs_cache:
                if "pauli" in club['club_name'].lower():
                    self.logger.info(f"Found St. Pauli: {club['club_name']}")
                    return club
        
        # The normal case: match city identifier to club
        # Try exact match first (case-insensitive)
        for club in self.clubs_cache:
            club_city_lower = club['city'].lower()
            club_name_lower = club['club_name'].lower()
            
            # Match against city name
            if city_identifier in club_city_lower or club_city_lower in city_identifier:
                self.logger.info(f"Found club by city match: {club['club_name']}")
                return club
            
            # Match against club name (e.g., "heidenheim" in "1. FC Heidenheim")
            if city_identifier in club_name_lower:
                self.logger.info(f"Found club by name match: {club['club_name']}")
                return club
        
        self.logger.warning(f"No club found for identifier: {city_identifier}")
        return None
    
    def process_query(self, user_question: str) -> str:
        """
        Here is the main processing pipeline flow for user query.
        
        The challenge document specified these requirements:
        - Input: String involving user question
        - Output: String involving final prompt for LLM (This should involve the system 
          prompt for the llm, the user question and the additional retrieved information)
        - All errors are to be handled gracefully
        
        Pipeline/flow steps:
        1. Extract city/club from question
        2. Find matching Bundesliga club
        3. Get current coach and city from Wikidata (every question)
        4. Get coach introductory bio from Wikipedia (every question)
        5. Build final LLM prompt with all the required details
        
        Args:
            user_question: String involving the user question
            
        Returns:
            String involving final prompt for LLM
        """
        self.logger.info(f"Processing query: {user_question}")
        
        try:
            # Step 1: Extract city/club identifier from question
            # Note: based on challenge requirement: handle case-insensitive input
            city_identifier = self.entity_extractor.extract_city(user_question)
            
            if not city_identifier:
                error_msg = "Dear user, I could not identify a city or club in your question. Please, use the required question format and specify which city or club you're asking about."
                self.logger.warning(error_msg)
                return self._format_error_response(error_msg)
            
            # Step 2: Find club based on city identifier
            club_info = self.find_club_by_city(city_identifier)
            
            if not club_info:
                error_msg = f"Dear user, I could not find a Bundesliga club for '{city_identifier}'. Please, use the required question format or check the city name."
                self.logger.warning(error_msg)
                return self._format_error_response(error_msg)
            
            # Step 3: Retrieve current coach and city from Wikidata (every question)
            # Note: based on challenge requirement: "should be retrieved on every question"
            coach_info = self.wikidata_client.get_coach_for_club(club_info['club_qid'])
            
            if not coach_info:
                error_msg = f"Could not find current coach information for {club_info['club_name']}. The data may not be available in Wikidata."
                self.logger.warning(error_msg)
                return self._format_error_response(error_msg)
            
            # Step 4: Retrieve coach introductory information from Wikipedia
            # Note: based on challenge requirement: "this should be retrieved on every question"
            coach_intro = self.wikipedia_client.get_coach_intro(coach_info['name'])
            
            # Note: Missing coach wikipedia introductory information is not a fatal error
            # We can still build a prompt with available data
            if not coach_intro:
                self.logger.info("The wikipedia introductory information is unavailable, proceeding with available data")
            
            # Step 5: Build final prompt
            # Per challenge: output must involve system prompt, user question, and retrieved info
            final_prompt = self.prompt_builder.build_prompt(
                user_question=user_question,
                club_name=club_info['club_name'],
                city=club_info['city'],
                coach_name=coach_info['name'],
                coach_intro=coach_intro
            )
            
            self.logger.info("Successfully built final prompt")
            return final_prompt
            
        except Exception as e:
            self.logger.error(f"There was an unexpected error processing query: {str(e)}", exc_info=True)
            error_msg = "Dear user, an unexpected error occurred while processing your question. Please try again."
            return self._format_error_response(error_msg)
    
    def _format_error_response(self, error_message: str) -> str:
        """
        Format error message in a user-friendly way.
        
        The challenge document specified these requirements: "handle errors related to data that are not available 
        or missing in a way that makes sense for the user"
        
        Args:
            error_message: User-friendly error description
            
        Returns:
            Formatted error response (still returns a string as required)
        """
        return f"""ERROR: {error_message}

Dear user, the Germany`s 1. Bundesliga RAG-Chatbot system was unable to retrieve the necessary information to answer your question.
Please check your input and try again.

Examples of valid questions:
  - Who is coaching Berlin?
  - What about munich?
  - Who is heidenheims manager?
  - Who is it for Pauli?"""


def main():
    """
    This is the main entry point - the console interface.
    
    The challenge document specified these requirements:
    - "A frontend is not required"
    - "Input and output can be provided via the console"
    - "The interface is the console"
    """
    print("=" * 60)
    print("Germany`s 1. Bundesliga RAG-Chatbot Coach Information System")
    print("=" * 60)
    print()
    
    # Initialize Germany`s 1. Bundesliga RAG-Chatbot system
    rag_system = BundesligaCoachRAGChatbot()
    
    # Initialize clubs data
    print("Initializing system (retrieving Germany`s 1. Bundesliga clubs data)...")
    success = rag_system.initialize_clubs_data()
    
    if not success:
        print("ERROR: Failed to initialize system. Please check your internet connection and try again.")
        return
    
    print("System ready!")
    print()
    
    # Console interface instructions
    print("Dear user, I am a Chatbot for Germany`s 1. Bundesliga Coach Information System")
    print()
    print("You can ask questions about Germany`s 1. Bundesliga coaches (or type 'quit' or 'exit' to end or close the app)")
    print()
    print("Please to get the correct search results, you must ask questions in the format given in the examples below")
    print("Examples:")
    print("  - Who is coaching Berlin?")
    print("  - What about munich?")
    print("  - Who is heidenheims manager?")
    print("  - Who is it for Pauli?")
    print()
    
    # The main interaction steps or loop
    while True:
        try:
            # Get user input from console
            # The challenge document specified these requirements: "Input: String involving the user question"
            user_input = input("Your question: ").strip()
            
            if not user_input:
                continue
                
            if user_input.lower() in ['quit', 'exit', 'q']:
                print("I hope to see you soon. Goodbye!")
                break
            
            # Process query and get prompt
            # The challenge document specified these requirements: "Output: A string that involves the final prompt for an LLM"
            result_prompt = rag_system.process_query(user_input)
            
            # Output prompt to console
            print("\n" + "=" * 60)
            print("GENERATED LLM PROMPT:")
            print("=" * 60)
            print(result_prompt)
            print("=" * 60 + "\n")
            
        except KeyboardInterrupt:
            print("\n I hope to see you soon. Goodbye!")
            break
        except Exception as e:
            print(f"Error: {str(e)}")
            print("Please try again.\n")


if __name__ == "__main__":
    main()