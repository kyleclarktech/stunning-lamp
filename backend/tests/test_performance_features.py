"""
Unit tests for performance optimization features
"""

import pytest
import asyncio
from unittest.mock import Mock, MagicMock, patch
from query_patterns import QueryPatternMatcher, match_and_generate_query
from error_handler import QueryErrorHandler, handle_query_error
from streaming_utils import ResponseStreamer, StreamChunk, StreamingFormatter

class TestQueryPatternMatcher:
    """Test the query pattern matching system"""
    
    def setup_method(self):
        self.matcher = QueryPatternMatcher()
    
    def test_team_member_patterns(self):
        """Test team member query patterns"""
        queries = [
            "who's on the mobile team?",
            "show me mobile team members",
            "members of the engineering team"
        ]
        
        for query in queries:
            result = self.matcher.match_query(query)
            assert result is not None, f"Failed to match: {query}"
            cypher, params = result
            assert "MATCH (p:Person)-[:MEMBER_OF]->(t:Team)" in cypher
            assert "WHERE t.name CONTAINS" in cypher
    
    def test_manager_patterns(self):
        """Test manager query patterns"""
        queries = [
            "who is Sarah's manager?",
            "find the manager of John Smith",
            "who does Alice report to?"
        ]
        
        for query in queries:
            result = self.matcher.match_query(query)
            assert result is not None, f"Failed to match: {query}"
            cypher, params = result
            assert "MATCH (p:Person)-[:REPORTS_TO]->(m:Person)" in cypher
            assert "WHERE p.name CONTAINS" in cypher
    
    def test_role_based_patterns(self):
        """Test role-based query patterns"""
        queries = [
            "who's the CTO?",
            "find all engineers",
            "show people who are managers"
        ]
        
        for query in queries:
            result = self.matcher.match_query(query)
            assert result is not None, f"Failed to match: {query}"
            cypher, params = result
            assert "MATCH (p:Person)" in cypher
            assert "WHERE p.role CONTAINS" in cypher
    
    def test_policy_patterns(self):
        """Test policy query patterns"""
        queries = [
            "who's responsible for security policy?",
            "find the owner of data protection policy"
        ]
        
        for query in queries:
            result = self.matcher.match_query(query)
            assert result is not None, f"Failed to match: {query}"
            cypher, params = result
            assert "MATCH (t)-[:RESPONSIBLE_FOR]->(p:Policy)" in cypher
    
    def test_parameter_extraction(self):
        """Test parameter extraction from patterns"""
        query = "who's on the mobile apps team?"
        result = self.matcher.match_query(query)
        assert result is not None
        cypher, params = result
        
        # Check that parameters were extracted
        assert "'mobile apps'" in cypher.lower()
        assert "'Mobile Apps'" in cypher  # Capitalized version
    
    def test_no_match(self):
        """Test queries that don't match any pattern"""
        queries = [
            "what's the weather like?",
            "hello there",
            "calculate 2 + 2"
        ]
        
        for query in queries:
            result = self.matcher.match_query(query)
            assert result is None, f"Unexpected match for: {query}"
    
    def test_pattern_priority(self):
        """Test that higher priority patterns match first"""
        # Team pattern should match before generic role pattern
        query = "who's on the lead team?"
        result = self.matcher.match_query(query)
        assert result is not None
        cypher, _ = result
        # Should match team pattern, not role pattern
        assert "MEMBER_OF]->(t:Team)" in cypher

class TestQueryErrorHandler:
    """Test the enhanced error handling system"""
    
    def setup_method(self):
        self.handler = QueryErrorHandler()
    
    def test_syntax_error_parsing(self):
        """Test parsing of syntax errors"""
        error = Exception("Invalid input 'WHER': expected WHERE")
        response = self.handler.parse_falkor_error(str(error))
        
        assert "Syntax error near 'WHER'" in response["user_message"]
        assert response["error_type"] == "syntax_errors"
        assert len(response["suggestions"]) > 0
    
    def test_property_error_parsing(self):
        """Test parsing of property not found errors"""
        error = Exception("Property 'nam' not found")
        response = self.handler.parse_falkor_error(str(error))
        
        assert "property 'nam' doesn't exist" in response["user_message"]
        assert response["error_type"] == "runtime_errors"
        assert any("Person nodes have: name" in s for s in response["suggestions"])
    
    def test_similar_entity_suggestions(self):
        """Test fuzzy matching for entity names"""
        # Test team suggestions
        similar = self.handler.find_similar_entities("mobil", "teams")
        assert len(similar) > 0
        assert similar[0][0] == "mobile"
        assert similar[0][1] > 0.8  # High similarity score
        
        # Test role suggestions
        similar = self.handler.find_similar_entities("enginer", "roles")
        assert len(similar) > 0
        assert similar[0][0] == "engineer"
    
    def test_alternative_query_suggestions(self):
        """Test generation of alternative queries"""
        user_query = "who is John Smiths manager?"
        error_context = {"error_type": "no_results"}
        
        suggestions = self.handler.suggest_alternative_queries(user_query, error_context)
        assert len(suggestions) > 0
        assert any("Find people with name containing" in s for s in suggestions)
    
    def test_comprehensive_error_response(self):
        """Test full error response formatting"""
        error = Exception("No results found")
        user_query = "find the mobil team"
        cypher = "MATCH (t:Team) WHERE t.name = 'mobil'"
        
        response = handle_query_error(error, user_query, cypher)
        
        assert response["error"] is True
        assert "No results found" in response["message"]
        assert "alternative_queries" in response["help"]
        assert "suggestions" in response["help"]
        assert len(response["help"]["alternative_queries"]) > 0

class TestResponseStreamer:
    """Test the response streaming functionality"""
    
    @pytest.mark.asyncio
    async def test_send_chunk(self):
        """Test sending chunks through websocket"""
        mock_websocket = Mock()
        mock_websocket.send_text = MagicMock(return_value=asyncio.Future())
        mock_websocket.send_text.return_value.set_result(None)
        
        streamer = ResponseStreamer(mock_websocket)
        chunk = StreamChunk(type="test", data={"value": 42})
        
        await streamer.send_chunk(chunk)
        
        mock_websocket.send_text.assert_called_once()
        sent_data = mock_websocket.send_text.call_args[0][0]
        assert '"chunk_type": "test"' in sent_data
        assert '"value": 42' in sent_data
    
    @pytest.mark.asyncio
    async def test_stream_results(self):
        """Test streaming results in chunks"""
        mock_websocket = Mock()
        mock_websocket.send_text = MagicMock(return_value=asyncio.Future())
        mock_websocket.send_text.return_value.set_result(None)
        
        streamer = ResponseStreamer(mock_websocket, chunk_size=2)
        results = [
            {"id": 1, "name": "Alice"},
            {"id": 2, "name": "Bob"},
            {"id": 3, "name": "Charlie"},
            {"id": 4, "name": "David"},
            {"id": 5, "name": "Eve"}
        ]
        
        await streamer.stream_results(results, len(results))
        
        # Should send: metadata + 3 chunks + completion = 5 calls
        assert mock_websocket.send_text.call_count == 5
        
        # Check metadata was sent
        first_call = mock_websocket.send_text.call_args_list[0][0][0]
        assert '"chunk_type": "result_metadata"' in first_call
        assert '"total_count": 5' in first_call
    
    @pytest.mark.asyncio
    async def test_streaming_formatter(self):
        """Test the streaming formatter"""
        results = [
            {"name": "Alice", "role": "Engineer", "email": "alice@example.com", "department": "Engineering"},
            {"name": "Bob", "role": "Manager", "email": "bob@example.com", "department": "Engineering"}
        ]
        
        chunks = []
        async for chunk in StreamingFormatter.format_results_streaming(results, "team_members"):
            chunks.append(chunk)
        
        formatted = "".join(chunks)
        assert "## Team Members" in formatted
        assert "Alice" in formatted
        assert "Engineer" in formatted
        assert "bob@example.com" in formatted

class TestIntegration:
    """Integration tests for the performance features"""
    
    def test_pattern_matching_integration(self):
        """Test the full pattern matching flow"""
        query = "who's on the mobile team?"
        cypher = match_and_generate_query(query)
        
        assert cypher is not None
        assert "MATCH (p:Person)-[:MEMBER_OF]->(t:Team)" in cypher
        assert "mobile" in cypher.lower()
    
    def test_error_handling_integration(self):
        """Test error handling with real-like errors"""
        error = Exception("Runtime error: Property 'nmae' not found on node Person")
        user_query = "find person with nmae John"
        
        response = handle_query_error(error, user_query)
        
        assert response["error"] is True
        assert "property 'nmae' doesn't exist" in response["message"].lower()
        assert len(response["help"]["suggestions"]) > 0
        
        # Should suggest correct property names
        suggestions_text = str(response["help"]["suggestions"])
        assert "name" in suggestions_text

if __name__ == "__main__":
    pytest.main([__file__, "-v"])