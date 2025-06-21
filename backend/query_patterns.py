"""
Improved Query Pattern System with Semantic Understanding

This module provides an enhanced query pattern matching system that:
1. Understands semantic equivalents (e.g., "employees" = all Person nodes)
2. Handles role categorization (e.g., "developers" = engineering roles)
3. Provides better fallback mechanisms
4. Supports more natural language variations
"""

import re
from typing import Dict, List, Tuple, Optional, Any, Set
from dataclasses import dataclass
import logging

logger = logging.getLogger(__name__)

# Semantic mappings for generic terms
SEMANTIC_MAPPINGS = {
    # Generic terms for all people
    "employees": {"type": "all_people", "description": "All Person nodes"},
    "staff": {"type": "all_people", "description": "All Person nodes"},
    "people": {"type": "all_people", "description": "All Person nodes"},
    "workforce": {"type": "all_people", "description": "All Person nodes"},
    "personnel": {"type": "all_people", "description": "All Person nodes"},
    "team members": {"type": "all_people", "description": "All Person nodes"},
    "colleagues": {"type": "all_people", "description": "All Person nodes"},
    "employees work for the company": {"type": "all_people", "description": "All Person nodes"},
    "staff members": {"type": "all_people", "description": "All Person nodes"},
    
    # Role categories
    "developers": {"type": "role_category", "roles": ["Engineer", "Developer", "Architect"], "exclude": ["Manager", "Director", "VP"]},
    "engineers": {"type": "role_category", "roles": ["Engineer"], "exclude": ["Manager", "Director", "VP", "Sales"]},
    "managers": {"type": "role_category", "roles": ["Manager", "Lead", "Head", "Director", "VP", "Chief"]},
    "executives": {"type": "role_category", "roles": ["VP", "Vice President", "Chief", "CTO", "CEO", "CFO", "CRO", "CISO", "Director"]},
    "leaders": {"type": "role_category", "roles": ["Manager", "Lead", "Head", "Director", "VP", "Chief", "Supervisor"]},
    "analysts": {"type": "role_category", "roles": ["Analyst", "Scientist"], "exclude": ["Manager", "Director"]},
    "consultants": {"type": "role_category", "roles": ["Consultant", "Advisor", "Specialist"]},
    "sales team": {"type": "role_category", "roles": ["Sales", "Account Executive", "AE", "SDR"]},
    
    # Department categories
    "engineering team": {"type": "department_category", "departments": ["Engineering", "Data Platform", "Infrastructure", "DevOps", "Analytics Engineering"]},
    "product team": {"type": "department_category", "departments": ["Product"]},
    "sales organization": {"type": "department_category", "departments": ["Sales"]},
    "support team": {"type": "department_category", "departments": ["Customer Success", "Professional Services", "Support"]},
    "operations": {"type": "department_category", "departments": ["Operations", "People Operations", "Finance", "Legal"]},
}

@dataclass
class QueryPattern:
    """Enhanced query pattern with semantic understanding"""
    name: str
    description: str
    patterns: List[str]
    cypher_template: str
    parameter_extractors: Dict[str, str]
    priority: int = 0
    semantic_aware: bool = False  # Whether this pattern uses semantic mappings
    
@dataclass
class SemanticContext:
    """Context for semantic query understanding"""
    original_term: str
    semantic_type: str
    mapped_values: List[str]
    cypher_conditions: str

class EnhancedQueryPatternMatcher:
    """Enhanced query pattern matcher with semantic understanding"""
    
    def __init__(self):
        self.patterns = self._initialize_patterns()
        self.patterns.sort(key=lambda p: p.priority, reverse=True)
        self.semantic_mappings = SEMANTIC_MAPPINGS
        
    def _initialize_patterns(self) -> List[QueryPattern]:
        """Initialize enhanced query patterns"""
        return [
            # Count queries with semantic understanding
            QueryPattern(
                name="count_semantic",
                description="Count queries that understand semantic terms",
                patterns=[
                    r"how many (.+?)(?:\s+work(?:s)? for the (?:company|organization))?(?:\s+are there)?(?:\s+in the (?:company|organization))?(?:\?|$)",
                    r"(?:what is the )?(?:total )?(?:number|count) of (.+?)(?:\s+in the (?:company|organization))?(?:\?|$)",
                    r"count (?:all )?(?:the )?(.+?)(?:\s+in the (?:company|organization))?(?:\?|$)",
                    r"how many (.+?) do we have(?:\?|$)",
                    r"how many (.+?) are (?:there|employed)(?:\?|$)",
                    r"(?:what's|what is) (?:the )?(?:total )?(?:employee|staff|people) count(?:\?|$)"
                ],
                cypher_template="SEMANTIC_COUNT",  # Special template for semantic processing
                parameter_extractors={"term": "1"},
                priority=20,
                semantic_aware=True
            ),
            
            # List queries with semantic understanding
            QueryPattern(
                name="list_semantic",
                description="List queries that understand semantic terms",
                patterns=[
                    r"(?:show|list|find|get) (?:me )?(?:all )?(?:the )?(.+?)(?:\?|$)",
                    r"who are (?:all )?(?:the |our )?(.+?)(?:\?|$)",
                    r"(?:give me|I need) (?:a list of )?(?:all )?(?:the )?(.+?)(?:\?|$)"
                ],
                cypher_template="SEMANTIC_LIST",
                parameter_extractors={"term": "1"},
                priority=18,
                semantic_aware=True
            ),
            
            # Department with semantic role queries
            QueryPattern(
                name="semantic_role_in_dept",
                description="Find people with semantic roles in departments",
                patterns=[
                    r"(?:show|find|list) (?:all )?(?:the )?(.+?) in (?:the )?(.+?)(?:\s+department)?(?:\?|$)",
                    r"(.+?) (?:who work in|from) (?:the )?(.+?)(?:\s+department)?(?:\?|$)",
                    r"which (.+?) are in (?:the )?(.+?)(?:\?|$)"
                ],
                cypher_template="SEMANTIC_ROLE_DEPT",
                parameter_extractors={"role_term": "1", "dept": "2"},
                priority=15,
                semantic_aware=True
            ),
            
            # Existing patterns (kept for specific queries)
            QueryPattern(
                name="specific_person",
                description="Find a specific person by name",
                patterns=[
                    r"(?:who is|find|show me|tell me about) (.+?)(?:\?|$)",
                    r"(?:information about|details for) (.+?)(?:\?|$)"
                ],
                cypher_template="""MATCH (p:Person) WHERE p.name CONTAINS $name RETURN p.id, p.name, p.email, p.department, p.role, labels(p) as labels""",
                parameter_extractors={"name": "1"},
                priority=12
            ),
            
            QueryPattern(
                name="team_members",
                description="Find members of a specific team",
                patterns=[
                    r"who(?:'s| is| are)? (?:on|in|member of) (?:the )?(.+?)(?:\s+team)?(?:\?|$)",
                    r"members? of (?:the )?(.+?)(?:\s+team)?(?:\?|$)"
                ],
                cypher_template="""MATCH (p:Person)-[:MEMBER_OF]->(t:Team) WHERE t.name CONTAINS $team_name OR t.name CONTAINS $team_name_upper RETURN p.id, p.name, p.email, p.department, p.role, labels(p) as labels LIMIT 50""",
                parameter_extractors={"team_name": "1"},
                priority=10
            ),
            
            QueryPattern(
                name="manager_queries",
                description="Find managers and reporting relationships",
                patterns=[
                    r"who(?:'s| is) (.+?)(?:'s)? manager(?:\?|$)",
                    r"who does (.+?) report to(?:\?|$)",
                    r"(?:find|show) (?:the )?manager (?:of|for) (.+?)(?:\?|$)"
                ],
                cypher_template="""MATCH (p:Person)-[:REPORTS_TO]->(m:Person) WHERE p.name CONTAINS $person_name RETURN m.id, m.name, m.email, m.department, m.role, labels(m) as labels""",
                parameter_extractors={"person_name": "1"},
                priority=10
            ),
            
            QueryPattern(
                name="policy_queries",
                description="Find policies and responsible parties",
                patterns=[
                    r"who(?:'s| is)? (?:responsible for|owns?) (?:the )?(.+?)(?:\s+policy)?(?:\?|$)",
                    r"(?:show|find|list) (?:all )?(.+?) policies?(?:\?|$)",
                    r"policies? (?:for|about|related to) (.+?)(?:\?|$)"
                ],
                cypher_template="""MATCH (t)-[:RESPONSIBLE_FOR]->(p:Policy) WHERE p.name CONTAINS $policy OR p.category CONTAINS $policy OR p.description CONTAINS $policy RETURN t.id, t.name, labels(t) as labels, p.id, p.name, p.category, p.severity LIMIT 25""",
                parameter_extractors={"policy": "1"},
                priority=9
            ),
            
            # Hierarchy queries
            QueryPattern(
                name="org_hierarchy",
                description="Organization hierarchy queries",
                patterns=[
                    r"(?:show|display) (?:the )?(?:org|organization|organizational) (?:chart|hierarchy|structure)(?:\?|$)",
                    r"who reports to whom(?:\?|$)",
                    r"(?:management|reporting) (?:structure|hierarchy)(?:\?|$)"
                ],
                cypher_template="""MATCH (p:Person)-[:REPORTS_TO]->(m:Person) RETURN p.id, p.name, p.role, p.department, m.id as manager_id, m.name as manager_name, m.role as manager_role LIMIT 100""",
                parameter_extractors={},
                priority=8
            ),
            
            # Experience queries
            QueryPattern(
                name="experience_queries",
                description="Find people by experience level",
                patterns=[
                    r"(?:find|show|list) (?:all )?senior (.+?)(?:\?|$)",
                    r"(?:find|show|list) (?:all )?junior (.+?)(?:\?|$)",
                    r"(?:find|show|list) (?:all )?(?:staff|principal|lead) (.+?)(?:\?|$)"
                ],
                cypher_template="""MATCH (p:Person) WHERE p.role CONTAINS $level AND p.role CONTAINS $role RETURN p.id, p.name, p.email, p.department, p.role, labels(p) as labels LIMIT 50""",
                parameter_extractors={"level": "1", "role": "2"},
                priority=7
            ),
        ]
    
    def _get_semantic_context(self, term: str) -> Optional[SemanticContext]:
        """Get semantic context for a term"""
        term_lower = term.lower().strip()
        
        # Check direct mappings
        if term_lower in self.semantic_mappings:
            mapping = self.semantic_mappings[term_lower]
            
            if mapping["type"] == "all_people":
                return SemanticContext(
                    original_term=term,
                    semantic_type="all_people",
                    mapped_values=[],
                    cypher_conditions=""  # No conditions - match all Person nodes
                )
            
            elif mapping["type"] == "role_category":
                conditions = []
                for role_keyword in mapping["roles"]:
                    conditions.append(f"p.role CONTAINS '{role_keyword}'")
                
                # Add exclusions if any
                if "exclude" in mapping:
                    exclude_conditions = []
                    for exclude in mapping["exclude"]:
                        exclude_conditions.append(f"NOT p.role CONTAINS '{exclude}'")
                    
                    cypher_conditions = f"({' OR '.join(conditions)}) AND {' AND '.join(exclude_conditions)}"
                else:
                    cypher_conditions = f"({' OR '.join(conditions)})"
                
                return SemanticContext(
                    original_term=term,
                    semantic_type="role_category",
                    mapped_values=mapping["roles"],
                    cypher_conditions=cypher_conditions
                )
            
            elif mapping["type"] == "department_category":
                conditions = []
                for dept in mapping["departments"]:
                    conditions.append(f"p.department CONTAINS '{dept}'")
                
                return SemanticContext(
                    original_term=term,
                    semantic_type="department_category",
                    mapped_values=mapping["departments"],
                    cypher_conditions=f"({' OR '.join(conditions)})"
                )
        
        # Check for plural forms
        if term_lower.endswith('s') and term_lower[:-1] in self.semantic_mappings:
            return self._get_semantic_context(term_lower[:-1])
        
        return None
    
    def _build_semantic_query(self, pattern: QueryPattern, params: Dict[str, Any]) -> Optional[str]:
        """Build a semantic-aware query"""
        if pattern.cypher_template == "SEMANTIC_COUNT":
            term = params.get("term", "")
            semantic_context = self._get_semantic_context(term)
            
            if semantic_context:
                if semantic_context.semantic_type == "all_people":
                    return "MATCH (p:Person) RETURN count(p) as count"
                else:
                    return f"MATCH (p:Person) WHERE {semantic_context.cypher_conditions} RETURN count(p) as count"
            else:
                # Fallback to role-based search
                return f"MATCH (p:Person) WHERE p.role CONTAINS '{term}' OR p.role CONTAINS '{term.title()}' RETURN count(p) as count"
        
        elif pattern.cypher_template == "SEMANTIC_LIST":
            term = params.get("term", "")
            semantic_context = self._get_semantic_context(term)
            
            if semantic_context:
                if semantic_context.semantic_type == "all_people":
                    return "MATCH (p:Person) RETURN p.id, p.name, p.email, p.department, p.role, labels(p) as labels LIMIT 100"
                else:
                    return f"MATCH (p:Person) WHERE {semantic_context.cypher_conditions} RETURN p.id, p.name, p.email, p.department, p.role, labels(p) as labels LIMIT 100"
            else:
                # Fallback to role-based search
                return f"MATCH (p:Person) WHERE p.role CONTAINS '{term}' OR p.role CONTAINS '{term.title()}' RETURN p.id, p.name, p.email, p.department, p.role, labels(p) as labels LIMIT 50"
        
        elif pattern.cypher_template == "SEMANTIC_ROLE_DEPT":
            role_term = params.get("role_term", "")
            dept = params.get("dept", "")
            semantic_context = self._get_semantic_context(role_term)
            
            if semantic_context:
                base_conditions = semantic_context.cypher_conditions
                dept_condition = f"p.department CONTAINS '{dept}' OR p.department CONTAINS '{dept.title()}'"
                return f"MATCH (p:Person) WHERE ({base_conditions}) AND ({dept_condition}) RETURN p.id, p.name, p.email, p.department, p.role, labels(p) as labels LIMIT 50"
            else:
                # Fallback
                return f"MATCH (p:Person) WHERE (p.role CONTAINS '{role_term}' OR p.role CONTAINS '{role_term.title()}') AND (p.department CONTAINS '{dept}' OR p.department CONTAINS '{dept.title()}') RETURN p.id, p.name, p.email, p.department, p.role, labels(p) as labels LIMIT 50"
        
        return None
    
    def extract_parameters(self, pattern: QueryPattern, match: re.Match) -> Dict[str, Any]:
        """Extract parameters from regex match groups"""
        params = {}
        for param_name, group_num in pattern.parameter_extractors.items():
            if group_num.isdigit():
                value = match.group(int(group_num))
                if value:
                    value = value.strip().strip("'\"")
                    params[param_name] = value
                    
                    # Add uppercase variant for non-semantic patterns
                    if not pattern.semantic_aware and param_name in ['team_name', 'role', 'dept', 'policy', 'group', 'category', 'name', 'person_name']:
                        base_name = param_name.replace('_name', '').replace('_upper', '')
                        params[f"{base_name}_upper"] = ' '.join(word.capitalize() for word in value.split())
        
        return params
    
    def match_query(self, natural_language_query: str) -> Optional[Tuple[str, Dict[str, Any]]]:
        """Match a natural language query to a pattern with semantic understanding"""
        query_lower = natural_language_query.lower().strip()
        
        for pattern in self.patterns:
            for regex_pattern in pattern.patterns:
                match = re.match(regex_pattern, query_lower, re.IGNORECASE)
                if match:
                    logger.info(f"Matched pattern '{pattern.name}' for query: {natural_language_query}")
                    
                    params = self.extract_parameters(pattern, match)
                    
                    # Handle semantic patterns
                    if pattern.semantic_aware:
                        cypher_query = self._build_semantic_query(pattern, params)
                        if cypher_query:
                            return cypher_query, params
                    else:
                        # Standard pattern processing
                        cypher_query = pattern.cypher_template
                        for param_name, param_value in sorted(params.items(), key=lambda x: len(x[0]), reverse=True):
                            cypher_query = cypher_query.replace(f"${param_name}", f"'{param_value}'")
                        return cypher_query, params
        
        logger.debug(f"No pattern matched for query: {natural_language_query}")
        return None
    
    def get_supported_queries(self) -> List[str]:
        """Get list of example queries that are supported"""
        return [
            # Semantic queries
            "How many employees are there?",
            "Show me all staff members",
            "List all developers",
            "How many managers do we have?",
            "Find all engineers in the Data Platform department",
            "Count the executives",
            
            # Specific queries
            "Who is Sarah Chen?",
            "Who is on the Analytics team?",
            "Who reports to Michael Rodriguez?",
            "Find the Data Platform team members",
            "Who owns the data retention policy?",
            
            # Department queries
            "Show me everyone in Engineering",
            "How many people work in Sales?",
            "List Product team members",
            
            # Hierarchy queries
            "Show the org chart",
            "Display reporting structure",
            
            # Complex queries
            "Find senior engineers in Infrastructure",
            "Show all team leads",
            "List principal engineers"
        ]

# Global instance
enhanced_query_matcher = EnhancedQueryPatternMatcher()

def match_and_generate_query(user_message: str) -> Optional[str]:
    """
    Try to match user message to a pattern and generate Cypher query with semantic understanding.
    
    Returns:
        Cypher query string if matched, None otherwise
    """
    result = enhanced_query_matcher.match_query(user_message)
    if result:
        cypher_query, _ = result
        return cypher_query
    return None