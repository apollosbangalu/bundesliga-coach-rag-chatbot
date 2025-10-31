"""
This is the Wikidata SPARQL Client Module

Purpose: This module queries Wikidata for current Germany`s 1. Bundesliga coach and club information.

The challenge document specified these requirements:
- The club-to-city mappings must be retrieved from Wikidata.
- The current coach information must be retrieved via SPARQL on EVERY question.
- The current season's Bundesliga clubs must be retrieved.
- The Wikidata API with SPARQL queries must be used.
"""

#required imports
import logging
from typing import Optional, Dict, List
from SPARQLWrapper import SPARQLWrapper, JSON


class WikidataClient:
    """
    This is the client for querying Wikidata via SPARQL.
    
    The challenge document specified these requirements:
    - Coach name information must come from Wikidata
    - Must be queried via SPARQL via Wikidata API
    - Must be retrieved on every question
    """
    
    WIKIDATA_ENDPOINT = "https://query.wikidata.org/sparql" #this is the wikidata endpoint api used
    
    def __init__(self, logger: logging.Logger):
        """
        Initializing the Wikidata client.
        
        Args:
            logger: Logger instance for debugging false answers
        """
        self.logger = logger
        self.sparql = SPARQLWrapper(self.WIKIDATA_ENDPOINT)
        self.sparql.setReturnFormat(JSON)
        # Set user agent to comply with Wikidata API guidelines
        self.sparql.addCustomHttpHeader("User-Agent", "BundesligaCoachRAGChatbot/1.0")
        
    def get_bundesliga_clubs(self) -> List[Dict[str, str]]:
        """
        This function retrieves all clubs currently in Germany`s 1. Bundesliga.
        
        The challenge document specified these requirements: "which clubs are part of the current season"
        can be retrieved "on every question or not" - implementer's choice.
        
        Returns:
            List of dicts with club information:
            [{"club_name": "...", "city": "...", "club_uri": "...", "club_qid": "..."}]
            
        Raises:
            Exception: If query fails or network error occurs
        """
        self.logger.info("Querying Wikidata for current Germany`s 1. Bundesliga clubs")
        
        #The Wikidata graph has a standardised structure and identifiers for each entity - concepts, object and data properties etc
        # SPARQL query to get clubs in Germany`s 1. Bundesliga
        # Q82595: Germany`s 1. Bundesliga
        # P118: league (property)
        # P159: headquarters location (for city)
        # P2094: competition class (for current season participation)
        query = """
        SELECT DISTINCT ?club ?clubLabel ?city ?cityLabel WHERE {
          # Clubs that participate in Bundesliga
          ?club wdt:P118 wd:Q82595.
          
          # Get headquarters location (city)
          OPTIONAL { ?club wdt:P159 ?city. }
          
          # Ensure it's a football club
          ?club wdt:P31/wdt:P279* wd:Q476028.
          
          SERVICE wikibase:label { bd:serviceParam wikibase:language "en,de". }
        }
        ORDER BY ?clubLabel
        """
        
        self.logger.debug(f"SPARQL Query for clubs:\n{query}")
        
        try:
            self.sparql.setQuery(query)
            results = self.sparql.query().convert()
            
            # Log raw results for debugging false answers
            self.logger.debug(f"Raw Wikidata response for clubs: {results}")
            
            # Process results
            clubs = self._process_club_results(results)
            self.logger.info(f"Retrieved {len(clubs)} Germany`s 1. Bundesliga clubs from Wikidata")
            
            return clubs
            
        except Exception as e:
            self.logger.error(f"Error querying Wikidata for Germany`s 1. Bundesliga clubs: {str(e)}", exc_info=True)
            raise
    
    def get_coach_for_club(self, club_qid: str) -> Optional[Dict[str, str]]:
        """
        This function retrieves current coach for a specific club.
        
        The challenge document specified these requirements:
        - "This must be retrieved on every question" (explicitly stated)
        - The query of Wikidata must be via SPARQL
        
        Args:
            club_qid: Wikidata QID for the club (e.g., "Q15789")
            
        Returns:
            Dict with coach information: {"name": "...", "qid": "..."}
            None if no coach found
            
        Raises:
            Exception: If query fails or network error occurs
        """
        self.logger.info(f"Querying Wikidata for coach of club: {club_qid}")
        
        #The coach name details
        # SPARQL query to get current head coach
        # P286: head coach property
        # We want the current coach, not historical ones
        query = f"""
        SELECT ?coach ?coachLabel WHERE {{
          wd:{club_qid} wdt:P286 ?coach.
          
          SERVICE wikibase:label {{ bd:serviceParam wikibase:language "en,de". }}
        }}
        LIMIT 1
        """
        
        self.logger.debug(f"SPARQL Query for coach:\n{query}")
        
        try:
            self.sparql.setQuery(query)
            results = self.sparql.query().convert()
            
            # Log raw results for debugging false answers
            self.logger.debug(f"Raw Wikidata response for coach: {results}")
            
            # Process results
            coach_info = self._process_coach_results(results)
            
            if coach_info:
                self.logger.info(f"Retrieved coach: {coach_info['name']}")
            else:
                self.logger.warning(f"No coach found for club: {club_qid}")
                
            return coach_info
            
        except Exception as e:
            self.logger.error(f"Error querying Wikidata for coach: {str(e)}", exc_info=True)
            raise
    
    def _process_club_results(self, results: Dict) -> List[Dict[str, str]]:
        """
        this function processes raw SPARQL results for clubs.
        
        Args:
            results: Raw JSON response from Wikidata SPARQL endpoint
            
        Returns:
            List of processed club information dicts
        """
        clubs = []
        
        if 'results' not in results or 'bindings' not in results['results']:
            self.logger.warning("No results found in Wikidata response")
            return clubs
        
        for binding in results['results']['bindings']:
            try:
                # Extract club URI and QID
                club_uri = binding.get('club', {}).get('value', '')
                club_qid = club_uri.split('/')[-1] if club_uri else ''
                
                # Extract club name
                club_name = binding.get('clubLabel', {}).get('value', '')
                
                # Extract city name
                city_name = binding.get('cityLabel', {}).get('value', '')
                
                if club_name and club_qid:
                    club_info = {
                        'club_name': club_name,
                        'city': city_name if city_name else 'Unknown',
                        'club_uri': club_uri,
                        'club_qid': club_qid
                    }
                    clubs.append(club_info)
                    self.logger.debug(f"Processed club: {club_info}")
                    
            except Exception as e:
                self.logger.warning(f"Error processing club binding: {str(e)}")
                continue
        
        return clubs
    
    def _process_coach_results(self, results: Dict) -> Optional[Dict[str, str]]:
        """
        This function processes raw SPARQL results for coach.
        
        Args:
            results: Raw JSON response from Wikidata SPARQL endpoint
            
        Returns:
            Dict with coach information or None if not found
        """
        if 'results' not in results or 'bindings' not in results['results']:
            self.logger.warning("No results found in Wikidata response")
            return None
        
        bindings = results['results']['bindings']
        
        if not bindings:
            return None
        
        try:
            # Get first result (should be current coach)
            binding = bindings[0]
            
            # Extract coach name
            coach_name = binding.get('coachLabel', {}).get('value', '')
            
            # Extract coach URI and QID
            coach_uri = binding.get('coach', {}).get('value', '')
            coach_qid = coach_uri.split('/')[-1] if coach_uri else ''
            
            if coach_name:
                coach_info = {
                    'name': coach_name,
                    'qid': coach_qid
                }
                self.logger.debug(f"Processed coach: {coach_info}")
                return coach_info
                
        except Exception as e:
            self.logger.warning(f"Error processing coach binding: {str(e)}")
            
        return None