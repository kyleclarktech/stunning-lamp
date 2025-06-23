"""
Comprehensive query validator for FalkorDB
Validates Cypher queries before execution to catch common errors
"""

import re
from typing import List, Tuple, Dict, Set
import logging

logger = logging.getLogger(__name__)


class QueryValidator:
    """Validates Cypher queries for FalkorDB compatibility"""
    
    # Known FalkorDB functions
    VALID_FUNCTIONS = {
        # String functions
        'toLower', 'toUpper', 'trim', 'left', 'right', 'substring',
        'replace', 'split', 'size', 'reverse', 'toString',
        
        # Math functions
        'abs', 'ceil', 'floor', 'round', 'sqrt', 'sign', 'rand',
        'sin', 'cos', 'tan', 'asin', 'acos', 'atan', 'log', 'exp',
        
        # Aggregation functions
        'count', 'sum', 'avg', 'min', 'max', 'collect', 'stDev',
        
        # Date/Time functions
        'date', 'datetime', 'duration', 'timestamp',
        
        # Graph functions
        'id', 'labels', 'type', 'properties', 'keys', 'nodes', 
        'relationships', 'shortestPath', 'allShortestPaths',
        
        # List functions
        'range', 'head', 'tail', 'last', 'all', 'any', 'none', 'single'
    }
    
    # Invalid function patterns
    INVALID_FUNCTIONS = {
        'lower', 'LOWER', 'upper', 'UPPER', 'TRIM',
        'year', 'month', 'day', 'hour', 'minute', 'second',
        'datetime.truncate', 'date.truncate'
    }
    
    # Keywords that should not appear in certain contexts
    RESERVED_KEYWORDS = {
        'MATCH', 'OPTIONAL', 'WHERE', 'RETURN', 'WITH', 'CREATE',
        'DELETE', 'SET', 'REMOVE', 'MERGE', 'UNION', 'CALL', 'YIELD'
    }
    
    def __init__(self):
        self.errors = []
        self.warnings = []
    
    def validate(self, query: str) -> Tuple[bool, List[str], List[str]]:
        """
        Validate a Cypher query
        
        Args:
            query: The Cypher query to validate
            
        Returns:
            Tuple of (is_valid, errors, warnings)
        """
        self.errors = []
        self.warnings = []
        
        # Run all validation checks
        self._check_basic_structure(query)
        self._check_semicolons(query)
        self._check_function_names(query)
        self._check_aggregations(query)
        self._check_shortest_path(query)
        self._check_variable_definitions(query)
        self._check_parentheses_balance(query)
        self._check_string_quotes(query)
        
        is_valid = len(self.errors) == 0
        return is_valid, self.errors, self.warnings
    
    def _check_basic_structure(self, query: str) -> None:
        """Check if query has basic required structure"""
        query_upper = query.upper()
        
        # Must have at least MATCH or CREATE/MERGE
        if not any(keyword in query_upper for keyword in ['MATCH', 'CREATE', 'MERGE']):
            self.errors.append("Query must contain MATCH, CREATE, or MERGE")
        
        # Must have RETURN (unless it's a write-only query)
        if 'RETURN' not in query_upper and not any(kw in query_upper for kw in ['CREATE', 'MERGE', 'SET', 'DELETE']):
            self.errors.append("Query must have a RETURN clause")
    
    def _check_semicolons(self, query: str) -> None:
        """Check for multiple statements"""
        # Count semicolons not in strings
        semicolons = 0
        in_string = False
        escape_next = False
        string_char = None
        
        for char in query:
            if escape_next:
                escape_next = False
                continue
                
            if char == '\\':
                escape_next = True
                continue
                
            if char in ['"', "'"] and not in_string:
                in_string = True
                string_char = char
            elif char == string_char and in_string:
                in_string = False
                string_char = None
            elif char == ';' and not in_string:
                semicolons += 1
        
        if semicolons > 1:
            self.errors.append(f"Multiple semicolons detected ({semicolons}). Only single statements allowed.")
        elif semicolons == 1 and not query.strip().endswith(';'):
            self.errors.append("Semicolon detected in middle of query. Only trailing semicolons allowed.")
    
    def _check_function_names(self, query: str) -> None:
        """Check for invalid function names"""
        # Look for function calls
        function_pattern = r'\b([a-zA-Z_]\w*)\s*\('
        
        for match in re.finditer(function_pattern, query):
            func_name = match.group(1)
            
            # Check if it's an invalid function
            if func_name in self.INVALID_FUNCTIONS:
                if func_name.lower() == 'lower':
                    self.errors.append(f"Invalid function '{func_name}()'. Use 'toLower()' instead.")
                elif func_name.lower() == 'upper':
                    self.errors.append(f"Invalid function '{func_name}()'. Use 'toUpper()' instead.")
                elif func_name in ['year', 'month', 'day']:
                    self.errors.append(f"Invalid function '{func_name}()'. Date extraction not supported in this way.")
                else:
                    self.errors.append(f"Invalid function '{func_name}()' for FalkorDB.")
            
            # Check if it's not a known valid function (but not a keyword)
            elif func_name not in self.VALID_FUNCTIONS and func_name.upper() not in self.RESERVED_KEYWORDS:
                # Could be a user-defined function or procedure
                self.warnings.append(f"Unknown function '{func_name}()'. Ensure it's available in FalkorDB.")
    
    def _check_aggregations(self, query: str) -> None:
        """Check for aggregations in WHERE clauses"""
        # Split query into clauses
        where_pattern = r'WHERE\s+(.*?)(?:RETURN|WITH|ORDER|LIMIT|$)'
        
        for match in re.finditer(where_pattern, query, re.IGNORECASE | re.DOTALL):
            where_clause = match.group(1)
            
            # Check for aggregation functions
            agg_pattern = r'\b(count|sum|avg|min|max|collect)\s*\('
            if re.search(agg_pattern, where_clause, re.IGNORECASE):
                self.errors.append("Aggregation functions cannot be used directly in WHERE clauses. Use WITH clause first.")
    
    def _check_shortest_path(self, query: str) -> None:
        """Check for correct shortestPath usage"""
        # Check if shortestPath is in MATCH clause
        match_pattern = r'MATCH\s+[^=]*=\s*shortestPath\s*\('
        if re.search(match_pattern, query, re.IGNORECASE):
            self.errors.append("shortestPath() must be used in WITH or RETURN clause, not in MATCH.")
        
        # Check for correct pattern
        sp_pattern = r'shortestPath\s*\(\s*\(.*?\)-\[\*.*?\]-\(.*?\)\s*\)'
        if 'shortestPath' in query and not re.search(sp_pattern, query):
            self.warnings.append("shortestPath() syntax might be incorrect. Use: shortestPath((a)-[*]-(b))")
    
    def _check_variable_definitions(self, query: str) -> None:
        """Check if all used variables are defined"""
        # Extract defined variables
        defined_vars = set()
        
        # Variables from MATCH
        match_vars = re.findall(r'MATCH.*?\(([a-zA-Z_]\w*)(?::|(?:\s|$))', query, re.IGNORECASE)
        defined_vars.update(match_vars)
        
        # Variables from WITH
        with_vars = re.findall(r'WITH.*?(?:^|,)\s*(?:[^,\s]+\s+as\s+)?([a-zA-Z_]\w*)(?:\s|,|$)', query, re.IGNORECASE)
        defined_vars.update(with_vars)
        
        # Variables from relationships
        rel_vars = re.findall(r'-\[([a-zA-Z_]\w*)(?::|])', query)
        defined_vars.update(rel_vars)
        
        # Extract used variables (simplified)
        used_pattern = r'\b([a-zA-Z_]\w*)\.[a-zA-Z_]'
        used_vars = set(re.findall(used_pattern, query))
        
        # Check for undefined variables
        undefined = used_vars - defined_vars - {'date', 'datetime', 'duration', 'timestamp'}
        if undefined:
            self.errors.append(f"Undefined variables: {', '.join(sorted(undefined))}")
    
    def _check_parentheses_balance(self, query: str) -> None:
        """Check if parentheses are balanced"""
        stack = []
        in_string = False
        escape_next = False
        string_char = None
        
        for i, char in enumerate(query):
            if escape_next:
                escape_next = False
                continue
                
            if char == '\\':
                escape_next = True
                continue
                
            if char in ['"', "'"] and not in_string:
                in_string = True
                string_char = char
            elif char == string_char and in_string:
                in_string = False
                string_char = None
            elif not in_string:
                if char in '([{':
                    stack.append((char, i))
                elif char in ')]}':
                    if not stack:
                        self.errors.append(f"Unmatched closing '{char}' at position {i}")
                    else:
                        opening, _ = stack.pop()
                        if (char == ')' and opening != '(') or \
                           (char == ']' and opening != '[') or \
                           (char == '}' and opening != '{'):
                            self.errors.append(f"Mismatched brackets: '{opening}' and '{char}'")
        
        if stack:
            for bracket, pos in stack:
                self.errors.append(f"Unclosed '{bracket}' at position {pos}")
    
    def _check_string_quotes(self, query: str) -> None:
        """Check if string quotes are properly closed"""
        single_quotes = 0
        double_quotes = 0
        escape_next = False
        
        for char in query:
            if escape_next:
                escape_next = False
                continue
            
            if char == '\\':
                escape_next = True
                continue
                
            if char == '"':
                double_quotes += 1
            elif char == "'":
                single_quotes += 1
        
        if single_quotes % 2 != 0:
            self.errors.append("Unclosed single quote detected")
        if double_quotes % 2 != 0:
            self.errors.append("Unclosed double quote detected")


def validate_query(query: str) -> Tuple[bool, List[str], List[str]]:
    """
    Convenience function to validate a query
    
    Args:
        query: The Cypher query to validate
        
    Returns:
        Tuple of (is_valid, errors, warnings)
    """
    validator = QueryValidator()
    return validator.validate(query)


def validate_and_log(query: str) -> bool:
    """
    Validate a query and log any issues
    
    Args:
        query: The Cypher query to validate
        
    Returns:
        True if valid, False otherwise
    """
    is_valid, errors, warnings = validate_query(query)
    
    if errors:
        logger.error(f"Query validation failed with {len(errors)} errors:")
        for error in errors:
            logger.error(f"  - {error}")
    
    if warnings:
        logger.warning(f"Query validation produced {len(warnings)} warnings:")
        for warning in warnings:
            logger.warning(f"  - {warning}")
    
    return is_valid