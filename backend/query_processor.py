"""
Query post-processor for FalkorDB
Fixes common query generation errors to improve success rates
"""

import re
import logging

logger = logging.getLogger(__name__)


class QueryProcessor:
    """Post-processes Cypher queries to fix common FalkorDB-specific issues"""
    
    # Function name mappings
    FUNCTION_MAPPINGS = {
        # String functions
        r'\blower\s*\(': 'toLower(',
        r'\bLOWER\s*\(': 'toLower(',
        r'\bupper\s*\(': 'toUpper(',
        r'\bUPPER\s*\(': 'toUpper(',
        r'\bTRIM\s*\(': 'trim(',
        
        # Math functions (ensure lowercase)
        r'\bROUND\s*\(': 'round(',
        r'\bABS\s*\(': 'abs(',
        r'\bCEIL\s*\(': 'ceil(',
        r'\bFLOOR\s*\(': 'floor(',
        r'\bSQRT\s*\(': 'sqrt(',
        
        # Date functions that need special handling
        r'\byear\s*\(': 'date(',  # Simplified - may need custom logic
        r'\bmonth\s*\(': 'date(',  # Simplified - may need custom logic
        r'\bdatetime\.truncate\s*\(': 'date(',  # Not supported, use date()
    }
    
    def __init__(self):
        self.fixes_applied = []
    
    def process(self, query: str) -> str:
        """
        Apply all post-processing fixes to a query
        
        Args:
            query: The original Cypher query
            
        Returns:
            The fixed query
        """
        self.fixes_applied = []
        original_query = query
        
        # Apply fixes in order
        query = self._fix_function_names(query)
        query = self._fix_multiple_statements(query)
        query = self._fix_shortest_path(query)
        query = self._fix_aggregation_in_where(query)
        query = self._remove_trailing_semicolon(query)
        
        if query != original_query:
            logger.info(f"Query processed. Fixes applied: {', '.join(self.fixes_applied)}")
            logger.debug(f"Original: {original_query}")
            logger.debug(f"Fixed: {query}")
        
        return query
    
    def _fix_function_names(self, query: str) -> str:
        """Replace incorrect function names with FalkorDB-compatible ones"""
        fixed_query = query
        
        for pattern, replacement in self.FUNCTION_MAPPINGS.items():
            if re.search(pattern, fixed_query, re.IGNORECASE):
                fixed_query = re.sub(pattern, replacement, fixed_query, flags=re.IGNORECASE)
                self.fixes_applied.append(f"function_name: {pattern} -> {replacement}")
        
        return fixed_query
    
    def _fix_multiple_statements(self, query: str) -> str:
        """Remove multiple statements and comments after semicolons"""
        # Check for semicolons not in strings
        if ';' in query:
            # Simple approach: take everything before the first semicolon
            # that's not inside quotes
            parts = re.split(r';(?=(?:[^"\']*["\'][^"\']*["\'])*[^"\']*$)', query)
            if len(parts) > 1:
                self.fixes_applied.append("removed_multiple_statements")
                return parts[0].strip()
        
        return query
    
    def _fix_shortest_path(self, query: str) -> str:
        """Fix shortestPath placement - move from MATCH to WITH/RETURN"""
        # Pattern to find shortestPath in MATCH clause
        match_pattern = r'MATCH\s+.*?=\s*shortestPath\s*\('
        
        if re.search(match_pattern, query, re.IGNORECASE):
            # Complex fix - need to restructure query
            # For now, log warning as this requires deeper parsing
            logger.warning("shortestPath in MATCH clause detected - manual fix may be needed")
            self.fixes_applied.append("shortest_path_warning")
        
        return query
    
    def _fix_aggregation_in_where(self, query: str) -> str:
        """Fix aggregation functions used directly in WHERE clauses"""
        # Pattern to find COUNT/SUM/AVG/etc in WHERE
        agg_pattern = r'WHERE\s+.*?\b(COUNT|SUM|AVG|MIN|MAX)\s*\('
        
        match = re.search(agg_pattern, query, re.IGNORECASE)
        if match:
            # This is complex to fix automatically as it requires restructuring
            # Log warning for now
            logger.warning(f"Aggregation function '{match.group(1)}' in WHERE clause detected")
            self.fixes_applied.append("aggregation_in_where_warning")
        
        return query
    
    def _remove_trailing_semicolon(self, query: str) -> str:
        """Remove trailing semicolon from query"""
        query = query.strip()
        if query.endswith(';'):
            self.fixes_applied.append("removed_trailing_semicolon")
            return query[:-1].strip()
        return query
    
    def validate_query(self, query: str) -> tuple[bool, list[str]]:
        """
        Validate a query for common issues
        
        Returns:
            Tuple of (is_valid, list_of_issues)
        """
        issues = []
        
        # Check for multiple semicolons
        if query.count(';') > 1:
            issues.append("Multiple semicolons detected")
        
        # Check for undefined variables (simplified check)
        # This would need more sophisticated parsing for accuracy
        used_vars = re.findall(r'\b([a-zA-Z_]\w*)\.[a-zA-Z_]', query)
        defined_vars = re.findall(r'MATCH.*?\(([a-zA-Z_]\w*):', query)
        defined_vars.extend(re.findall(r'WITH.*?\s+as\s+([a-zA-Z_]\w*)', query))
        
        undefined = set(used_vars) - set(defined_vars) - {'date', 'datetime', 'duration'}
        if undefined:
            issues.append(f"Potentially undefined variables: {', '.join(undefined)}")
        
        # Check for aggregations in WHERE
        if re.search(r'WHERE\s+.*?\b(COUNT|SUM|AVG|MIN|MAX)\s*\(', query, re.IGNORECASE):
            issues.append("Aggregation function in WHERE clause")
        
        # Check for shortestPath in MATCH
        if re.search(r'MATCH\s+.*?=\s*shortestPath\s*\(', query, re.IGNORECASE):
            issues.append("shortestPath in MATCH clause (should be in WITH/RETURN)")
        
        return len(issues) == 0, issues


def process_query(query: str) -> str:
    """
    Convenience function to process a query
    
    Args:
        query: The original Cypher query
        
    Returns:
        The processed query
    """
    processor = QueryProcessor()
    return processor.process(query)


def validate_query(query: str) -> tuple[bool, list[str]]:
    """
    Convenience function to validate a query
    
    Args:
        query: The Cypher query to validate
        
    Returns:
        Tuple of (is_valid, list_of_issues)
    """
    processor = QueryProcessor()
    return processor.validate_query(query)