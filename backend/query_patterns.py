"""
Query Pattern Pre-compilation System

This module provides pre-compiled Cypher query patterns for common natural language queries.
It bypasses the LLM for pattern-matched queries, significantly reducing response time.
"""

import re
from typing import Dict, List, Tuple, Optional, Any
from dataclasses import dataclass
import logging

logger = logging.getLogger(__name__)

@dataclass
class QueryPattern:
    """Represents a pre-compiled query pattern"""
    name: str
    description: str
    patterns: List[str]  # Regex patterns to match
    cypher_template: str
    parameter_extractors: Dict[str, str]  # Maps parameter names to regex groups
    priority: int = 0  # Higher priority patterns are checked first

class QueryPatternMatcher:
    """Matches natural language queries to pre-compiled Cypher patterns"""
    
    def __init__(self):
        self.patterns = self._initialize_patterns()
        # Sort patterns by priority (descending)
        self.patterns.sort(key=lambda p: p.priority, reverse=True)
        
    def _initialize_patterns(self) -> List[QueryPattern]:
        """Initialize the pre-compiled query patterns"""
        return [
            # Team membership queries
            QueryPattern(
                name="team_members",
                description="Find members of a specific team",
                patterns=[
                    r"who(?:'s| is| are)? (?:on|in|member of) (?:the )?(.+?)(?:\s+team)?(?:\?|$)",
                    r"(?:show|find|list) (?:me )?(?:the )?(.+?)(?:\s+team)? members?(?:\?|$)",
                    r"members? of (?:the )?(.+?)(?:\s+team)?(?:\?|$)"
                ],
                cypher_template="""MATCH (p:Person)-[:MEMBER_OF]->(t:Team) WHERE t.name CONTAINS $team_name OR t.name CONTAINS $team_name_upper RETURN p.id, p.name, p.email, p.department, p.role, labels(p) as labels LIMIT 25""",
                parameter_extractors={"team_name": "1"},
                priority=10
            ),
            
            # Manager queries
            QueryPattern(
                name="find_manager",
                description="Find someone's manager",
                patterns=[
                    r"who(?:'s| is) (.+?)(?:'s)? manager(?:\?|$)",
                    r"(?:find|show|get) (?:the )?manager (?:of|for) (.+?)(?:\?|$)",
                    r"who does (.+?) report to(?:\?|$)"
                ],
                cypher_template="""MATCH (p:Person)-[:REPORTS_TO]->(m:Person) WHERE p.name CONTAINS $person_name RETURN m.id, m.name, m.email, m.department, m.role, labels(m) as labels""",
                parameter_extractors={"person_name": "1"},
                priority=10
            ),
            
            # Direct reports queries
            QueryPattern(
                name="direct_reports",
                description="Find who reports to someone",
                patterns=[
                    r"who reports to (.+?)(?:\?|$)",
                    r"(?:show|find|list) (.+?)(?:'s)? (?:direct )?reports(?:\?|$)",
                    r"(?:show|find|list) people who report to (.+?)(?:\?|$)"
                ],
                cypher_template="""MATCH (p:Person)-[:REPORTS_TO]->(m:Person) WHERE m.name CONTAINS $manager_name OR m.role CONTAINS $manager_name RETURN p.id, p.name, p.email, p.department, p.role, labels(p) as labels LIMIT 25""",
                parameter_extractors={"manager_name": "1"},
                priority=10
            ),
            
            # Role-based queries
            QueryPattern(
                name="find_by_role",
                description="Find people by their role",
                patterns=[
                    r"who(?:'s| is| are) (?:the |our )?(.+?)(?:\?|$)",
                    r"(?:find|show|list) (?:all )?(?:the )?(.+?)s?(?:\?|$)",
                    r"(?:find|show|list) people (?:who are |with role )?(.+?)(?:\?|$)"
                ],
                cypher_template="""MATCH (p:Person) WHERE p.role CONTAINS $role OR p.role CONTAINS $role_upper RETURN p.id, p.name, p.email, p.department, p.role, labels(p) as labels LIMIT 25""",
                parameter_extractors={"role": "1"},
                priority=5
            ),
            
            # Department queries
            QueryPattern(
                name="department_members",
                description="Find people in a department",
                patterns=[
                    r"(?:who works in|people in|employees in|show me) (?:the )?(.+?)(?:\s+department)?(?:\?|$)",
                    r"(?:list|find|show) (?:all )?(.+?)(?:\s+department)? (?:employees|people|staff)(?:\?|$)",
                    r"(?:list|find|show|get) (?:all )?members of (?:the )?(.+?)(?:\s+department)?(?:\?|$)",
                    r"members of (?:the )?(.+?)(?:\s+department)?(?:\?|$)"
                ],
                cypher_template="""MATCH (p:Person) WHERE p.department CONTAINS $dept OR p.department CONTAINS $dept_upper RETURN p.id, p.name, p.email, p.role, labels(p) as labels LIMIT 25""",
                parameter_extractors={"dept": "1"},
                priority=8
            ),
            
            # Policy ownership queries
            QueryPattern(
                name="policy_owners",
                description="Find who owns or is responsible for policies",
                patterns=[
                    r"who(?:'s| is)? (?:responsible for|owns?) (?:the )?(.+?)(?:\s+policy)?(?:\?|$)",
                    r"(?:find|show) (?:the )?(?:owner|responsible party) (?:for|of) (?:the )?(.+?)(?:\s+policy)?(?:\?|$)"
                ],
                cypher_template="""MATCH (t)-[:RESPONSIBLE_FOR]->(p:Policy) WHERE p.name CONTAINS $policy OR p.category CONTAINS $policy OR p.description CONTAINS $policy RETURN t.id, t.name, labels(t) as labels, p.id, p.name, p.category, p.severity LIMIT 25""",
                parameter_extractors={"policy": "1"},
                priority=9
            ),
            
            # Group membership queries
            QueryPattern(
                name="group_members",
                description="Find members of a group",
                patterns=[
                    r"who(?:'s| is| are)? (?:in|member of) (?:the )?(.+?)(?:\s+group)?(?:\?|$)",
                    r"(?:show|find|list) (?:the )?(.+?)(?:\s+group)? members?(?:\?|$)"
                ],
                cypher_template="""MATCH (p:Person)-[:MEMBER_OF]->(g:Group) WHERE g.name CONTAINS $group OR g.name CONTAINS $group_upper RETURN p.id, p.name, p.email, p.department, p.role, labels(p) as labels LIMIT 25""",
                parameter_extractors={"group": "1"},
                priority=8
            ),
            
            # Team lead queries
            QueryPattern(
                name="team_leads",
                description="Find team leads",
                patterns=[
                    r"(?:who are|find|show|list) (?:the )?team leads?(?:\?|$)",
                    r"(?:who are|find|show|list) (?:all )?(?:the )?leads?(?:\?|$)",
                    r"team leads? (?:in|for) (?:the )?(.+?)(?:\s+department)?(?:\?|$)"
                ],
                cypher_template="""MATCH (p:Person) WHERE p.role CONTAINS 'Lead' OR p.role CONTAINS 'lead' OR p.role CONTAINS 'Manager' OR p.role CONTAINS 'manager' OR p.role CONTAINS 'Head' RETURN p.id, p.name, p.email, p.department, p.role, labels(p) as labels LIMIT 25""",
                parameter_extractors={},
                priority=7
            ),
            
            # Policy category queries
            QueryPattern(
                name="policies_by_category",
                description="Find policies by category",
                patterns=[
                    r"(?:show|find|list) (?:all )?(.+?) policies?(?:\?|$)",
                    r"(?:what are|find) (?:the )?(.+?) (?:related )?policies?(?:\?|$)",
                    r"policies? (?:for|about|related to) (.+?)(?:\?|$)"
                ],
                cypher_template="""MATCH (p:Policy) WHERE p.category CONTAINS $category OR p.name CONTAINS $category OR p.description CONTAINS $category RETURN p.id, p.name, p.category, p.description, p.severity LIMIT 25""",
                parameter_extractors={"category": "1"},
                priority=7
            ),
            
            # Count queries
            QueryPattern(
                name="count_people_dept",
                description="Count people in a department",
                patterns=[
                    r"how many (?:people|employees) (?:are )?(?:in|work in) (?:the )?(.+?)(?:\s+department)?(?:\?|$)",
                    r"count (?:of )?(?:people|employees) in (?:the )?(.+?)(?:\s+department)?(?:\?|$)"
                ],
                cypher_template="""MATCH (p:Person) WHERE p.department CONTAINS $dept OR p.department CONTAINS $dept_upper RETURN count(p) as count""",
                parameter_extractors={"dept": "1"},
                priority=6
            )
        ]
    
    def extract_parameters(self, pattern: QueryPattern, match: re.Match) -> Dict[str, Any]:
        """Extract parameters from regex match groups"""
        params = {}
        for param_name, group_num in pattern.parameter_extractors.items():
            if group_num.isdigit():
                value = match.group(int(group_num))
                if value:
                    # Clean up the extracted value
                    value = value.strip().strip("'\"")
                    params[param_name] = value
                    
                    # Add uppercase variant for case-insensitive matching
                    if param_name.endswith('_name') or param_name in ['team_name', 'role', 'dept', 'policy', 'group', 'category']:
                        # Create uppercase variant
                        base_name = param_name.replace('_name', '').replace('_upper', '')
                        # Title case for multi-word values
                        params[f"{base_name}_upper"] = ' '.join(word.capitalize() for word in value.split())
                        
        return params
    
    def match_query(self, natural_language_query: str) -> Optional[Tuple[str, Dict[str, Any]]]:
        """
        Match a natural language query to a pre-compiled pattern.
        
        Returns:
            Tuple of (cypher_query, parameters) if matched, None otherwise
        """
        query_lower = natural_language_query.lower().strip()
        
        for pattern in self.patterns:
            for regex_pattern in pattern.patterns:
                match = re.match(regex_pattern, query_lower, re.IGNORECASE)
                if match:
                    logger.info(f"Matched pattern '{pattern.name}' for query: {natural_language_query}")
                    
                    # Extract parameters
                    params = self.extract_parameters(pattern, match)
                    
                    # Substitute parameters into the Cypher template
                    cypher_query = pattern.cypher_template
                    for param_name, param_value in sorted(params.items(), key=lambda x: len(x[0]), reverse=True):
                        # Use parameter substitution for FalkorDB
                        cypher_query = cypher_query.replace(f"${param_name}", f"'{param_value}'")
                    
                    return cypher_query, params
        
        logger.debug(f"No pattern matched for query: {natural_language_query}")
        return None
    
    def get_pattern_coverage_stats(self) -> Dict[str, Any]:
        """Get statistics about pattern coverage"""
        return {
            "total_patterns": len(self.patterns),
            "pattern_names": [p.name for p in self.patterns],
            "total_regex_patterns": sum(len(p.patterns) for p in self.patterns)
        }

# Global instance
query_matcher = QueryPatternMatcher()

def match_and_generate_query(user_message: str) -> Optional[str]:
    """
    Try to match user message to a pre-compiled pattern and generate Cypher query.
    
    Returns:
        Cypher query string if matched, None otherwise
    """
    result = query_matcher.match_query(user_message)
    if result:
        cypher_query, _ = result
        return cypher_query
    return None