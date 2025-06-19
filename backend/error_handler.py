"""
Enhanced Error Handler for FalkorDB Chat Interface

This module provides user-friendly error messages, query suggestions, 
and "did you mean?" functionality for failed queries.
"""

import re
import difflib
from typing import Dict, List, Optional, Tuple
import logging

logger = logging.getLogger(__name__)

class QueryErrorHandler:
    """Handles query errors and provides helpful suggestions"""
    
    def __init__(self):
        self.common_entities = self._load_common_entities()
        self.error_mappings = self._initialize_error_mappings()
        
    def _load_common_entities(self) -> Dict[str, List[str]]:
        """Load common entity names that users might search for"""
        return {
            "teams": [
                "mobile", "mobile apps", "backend", "frontend", "qa", "quality assurance",
                "devops", "infrastructure", "data", "analytics", "security", "platform",
                "product", "design", "marketing", "sales", "support", "engineering"
            ],
            "roles": [
                "engineer", "developer", "manager", "lead", "director", "cto", "ceo",
                "architect", "analyst", "designer", "product manager", "team lead",
                "senior", "junior", "principal", "staff", "vp", "president"
            ],
            "departments": [
                "engineering", "product", "design", "marketing", "sales", "hr",
                "human resources", "finance", "operations", "it", "legal", "support"
            ],
            "policies": [
                "security", "privacy", "compliance", "code review", "access", "data",
                "incident", "change management", "third party", "encryption", "backup"
            ],
            "groups": [
                "governance", "technical", "operational", "security", "compliance",
                "architecture", "leadership", "steering committee"
            ]
        }
    
    def _initialize_error_mappings(self) -> Dict[str, Dict[str, str]]:
        """Initialize mappings from FalkorDB error patterns to user-friendly messages"""
        return {
            "syntax_errors": {
                r"Invalid input '(.+?)':": "Syntax error near '{0}'. Check your query syntax.",
                r"Variable `(.+?)` not defined": "Unknown reference '{0}'. Make sure all variables are properly defined.",
                r"Unknown function '(.+?)'": "Function '{0}' is not supported. Try using a different approach.",
                r"Type mismatch": "Type error in query. Check that you're comparing compatible data types."
            },
            "runtime_errors": {
                r"Property '(.+?)' not found": "The property '{0}' doesn't exist. Available properties depend on the node type.",
                r"Label '(.+?)' not found": "The label '{0}' doesn't exist. Valid labels are: Person, Team, Group, Policy.",
                r"Relationship '(.+?)' not found": "The relationship '{0}' doesn't exist. Valid relationships are: MEMBER_OF, REPORTS_TO, RESPONSIBLE_FOR."
            },
            "timeout_errors": {
                r"timeout|timed out": "Query took too long to execute. Try a simpler query or add more specific filters."
            }
        }
    
    def find_similar_entities(self, search_term: str, entity_type: str = None) -> List[Tuple[str, float]]:
        """Find similar entity names using fuzzy matching"""
        candidates = []
        
        if entity_type and entity_type in self.common_entities:
            candidates = self.common_entities[entity_type]
        else:
            # Search across all entity types
            for entities in self.common_entities.values():
                candidates.extend(entities)
        
        # Use difflib to find close matches
        close_matches = difflib.get_close_matches(
            search_term.lower(), 
            [c.lower() for c in candidates], 
            n=3, 
            cutoff=0.6
        )
        
        # Calculate similarity scores
        results = []
        for match in close_matches:
            ratio = difflib.SequenceMatcher(None, search_term.lower(), match).ratio()
            # Find original case version
            original = next((c for c in candidates if c.lower() == match), match)
            results.append((original, ratio))
        
        return sorted(results, key=lambda x: x[1], reverse=True)
    
    def parse_falkor_error(self, error_message: str) -> Dict[str, any]:
        """Parse FalkorDB error message and return structured error info"""
        result = {
            "original_error": error_message,
            "user_message": "An error occurred while executing your query.",
            "suggestions": [],
            "examples": []
        }
        
        # Check error patterns
        for error_type, patterns in self.error_mappings.items():
            for pattern, message_template in patterns.items():
                match = re.search(pattern, error_message, re.IGNORECASE)
                if match:
                    result["user_message"] = message_template.format(*match.groups())
                    result["error_type"] = error_type
                    
                    # Add specific suggestions based on error type
                    if error_type == "syntax_errors":
                        result["suggestions"].append("Check that all parentheses and quotes are balanced")
                        result["suggestions"].append("Ensure WHERE clauses come after the full pattern match")
                    elif error_type == "runtime_errors":
                        if "Property" in message_template:
                            result["suggestions"].append("Person nodes have: name, email, department, role")
                            result["suggestions"].append("Team nodes have: name, department, focus")
                            result["suggestions"].append("Policy nodes have: name, category, description, severity")
                    
                    return result
        
        # Generic error handling
        if "no results" in error_message.lower() or "empty" in error_message.lower():
            result["user_message"] = "No results found for your query."
            result["suggestions"] = [
                "Try using broader search terms",
                "Check spelling of names and departments",
                "Use partial matches instead of exact names"
            ]
        
        return result
    
    def suggest_alternative_queries(self, user_query: str, error_context: Dict) -> List[str]:
        """Suggest alternative queries based on the failed query"""
        suggestions = []
        query_lower = user_query.lower()
        
        # Extract potential search terms
        # Look for quoted strings first
        quoted_terms = re.findall(r'"([^"]+)"', user_query) + re.findall(r"'([^']+)'", user_query)
        
        # Look for potential entity names (capitalized words)
        potential_names = re.findall(r'\b[A-Z][a-z]+(?:\s+[A-Z][a-z]+)*\b', user_query)
        
        # Check for common patterns and suggest alternatives
        if "who is" in query_lower or "who's" in query_lower:
            if potential_names:
                name = potential_names[0]
                suggestions.append(f"Find people with name containing '{name}'")
                suggestions.append(f"Show me all people in {name}'s department")
        
        if "team" in query_lower:
            # Find similar team names
            for term in quoted_terms + potential_names:
                similar = self.find_similar_entities(term, "teams")
                for similar_term, score in similar[:2]:
                    suggestions.append(f"Who's on the {similar_term} team?")
        
        if "policy" in query_lower or "policies" in query_lower:
            # Suggest policy categories
            suggestions.append("Show me all security policies")
            suggestions.append("Find compliance-related policies")
            suggestions.append("Who owns data protection policies?")
        
        if any(role in query_lower for role in ["manager", "lead", "director"]):
            suggestions.append("Show me all team leads")
            suggestions.append("Find people with 'Manager' in their role")
            suggestions.append("Who are the department heads?")
        
        return suggestions[:5]  # Limit to 5 suggestions
    
    def format_error_response(self, error: Exception, user_query: str, cypher_query: str = None) -> Dict[str, any]:
        """Format a comprehensive error response with helpful information"""
        error_str = str(error)
        parsed_error = self.parse_falkor_error(error_str)
        
        # Get alternative query suggestions
        suggestions = self.suggest_alternative_queries(user_query, parsed_error)
        
        # Build the response
        response = {
            "error": True,
            "message": parsed_error["user_message"],
            "details": {
                "query": user_query,
                "cypher": cypher_query if cypher_query else "Query generation failed"
            },
            "help": {
                "suggestions": parsed_error["suggestions"],
                "alternative_queries": suggestions,
                "tips": [
                    "Use partial names instead of full names",
                    "Try broader categories like 'engineering' instead of specific team names",
                    "Check the list of available teams, departments, and roles"
                ]
            }
        }
        
        # Add "did you mean?" suggestions if we can identify typos
        did_you_mean = []
        words = re.findall(r'\b\w+\b', user_query.lower())
        for word in words:
            if len(word) > 3:  # Only check longer words
                for entity_type, entities in self.common_entities.items():
                    similar = self.find_similar_entities(word, entity_type)
                    if similar and similar[0][1] > 0.8:  # High similarity
                        did_you_mean.append(f"Did you mean '{similar[0][0]}' instead of '{word}'?")
        
        if did_you_mean:
            response["help"]["did_you_mean"] = did_you_mean[:2]
        
        return response

# Global instance
error_handler = QueryErrorHandler()

def handle_query_error(error: Exception, user_query: str, cypher_query: str = None) -> Dict[str, any]:
    """Main entry point for error handling"""
    return error_handler.format_error_response(error, user_query, cypher_query)