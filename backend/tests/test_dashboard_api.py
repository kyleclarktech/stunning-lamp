"""
Tests for dashboard API endpoints
"""
import pytest
import asyncio
import json
from datetime import datetime, timedelta
from unittest.mock import patch, MagicMock, AsyncMock
from fastapi.testclient import TestClient
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from main import app
from api.dashboard import execute_query_with_cache

client = TestClient(app)

# Mock data for testing
MOCK_OVERVIEW_DATA = [{
    "total_employees": 500,
    "total_teams": 20,
    "total_groups": 8,
    "total_policies": 45,
    "active_projects": 15,
    "total_offices": 8,
    "total_skills": 50,
    "critical_incidents": 3
}]

MOCK_OFFICES_DATA = [
    {
        "office_name": "New York",
        "location": "New York, NY, USA",
        "timezone": "UTC-5",
        "employee_count": 120,
        "on_call_staff": [
            {"name": "John Doe", "role": "Engineering Lead", "email": "john@example.com"}
        ]
    },
    {
        "office_name": "London",
        "location": "London, UK",
        "timezone": "UTC+0",
        "employee_count": 85,
        "on_call_staff": [
            {"name": "Jane Smith", "role": "Operations Manager", "email": "jane@example.com"}
        ]
    }
]

MOCK_TEAMS_DATA = [
    {
        "team_name": "Platform Engineering",
        "department": "Engineering",
        "focus_area": "Infrastructure",
        "member_count": 25
    },
    {
        "team_name": "Data Science",
        "department": "Engineering",
        "focus_area": "Analytics",
        "member_count": 18
    }
]

class TestDashboardAPI:
    """Test suite for dashboard API endpoints"""

    @pytest.mark.asyncio
    @patch('api.dashboard.execute_query_with_cache')
    async def test_overview_endpoint(self, mock_execute):
        """Test GET /api/dashboard/overview endpoint"""
        # Setup mock
        mock_execute.side_effect = [
            MOCK_OVERVIEW_DATA,  # counts query
            [{"critical_incidents": 3}]  # incidents query
        ]
        
        # Make request
        response = client.get("/api/dashboard/overview")
        
        # Verify response
        assert response.status_code == 200
        data = response.json()
        
        assert data["total_employees"] == 500
        assert data["total_teams"] == 20
        assert data["total_groups"] == 8
        assert data["total_policies"] == 45
        assert data["active_projects"] == 15
        assert data["total_offices"] == 8
        assert data["total_skills"] == 50
        assert data["active_incidents"] == 3
        assert data["system_health"] == "operational"
        assert "last_updated" in data
        
        # Verify mock was called correctly
        assert mock_execute.call_count == 2

    @pytest.mark.asyncio
    @patch('api.dashboard.execute_query_with_cache')
    async def test_offices_endpoint(self, mock_execute):
        """Test GET /api/dashboard/offices endpoint"""
        # Setup mock
        mock_execute.return_value = MOCK_OFFICES_DATA
        
        # Make request
        response = client.get("/api/dashboard/offices")
        
        # Verify response
        assert response.status_code == 200
        data = response.json()
        
        assert len(data) == 2
        assert data[0]["name"] == "New York"
        assert data[0]["employee_count"] == 120
        assert data[0]["status"] in ["online", "offline"]
        assert "local_time" in data[0]
        assert len(data[0]["on_call_staff"]) > 0
        
        # Verify mock was called
        mock_execute.assert_called_once()

    @pytest.mark.asyncio
    @patch('api.dashboard.execute_query_with_cache')
    async def test_incidents_endpoint(self, mock_execute):
        """Test GET /api/dashboard/incidents endpoint"""
        # Setup mock data
        mock_incidents = [
            {
                "title": "Data Privacy Policy",
                "severity": "critical",
                "category": "compliance",
                "assignee_name": "Alice Johnson",
                "assignee_email": "alice@example.com",
                "id": "POL-001"
            },
            {
                "title": "Security Audit Policy",
                "severity": "high",
                "category": "security",
                "assignee_name": "Bob Smith",
                "assignee_email": "bob@example.com",
                "id": "POL-002"
            }
        ]
        mock_execute.return_value = mock_incidents
        
        # Make request
        response = client.get("/api/dashboard/incidents")
        
        # Verify response
        assert response.status_code == 200
        data = response.json()
        
        assert "critical" in data
        assert "high" in data
        assert "medium" in data
        assert "low" in data
        
        # Check critical incidents
        assert len(data["critical"]) > 0
        incident = data["critical"][0]
        assert "id" in incident
        assert "title" in incident
        assert "severity" in incident
        assert "assignee" in incident
        assert "created_at" in incident
        
        # Verify mock was called
        mock_execute.assert_called_once()

    @pytest.mark.asyncio
    async def test_metrics_endpoint(self):
        """Test GET /api/dashboard/metrics endpoint"""
        # No mocking needed - this endpoint generates synthetic data
        response = client.get("/api/dashboard/metrics")
        
        # Verify response
        assert response.status_code == 200
        data = response.json()
        
        assert "timestamps" in data
        assert "query_response_time" in data
        assert "active_users" in data
        assert "api_requests" in data
        assert "cache_hit_rate" in data
        assert "error_rate" in data
        
        # Verify data structure
        assert len(data["timestamps"]) > 0
        assert len(data["query_response_time"]["data"]) == len(data["timestamps"])
        assert data["query_response_time"]["unit"] == "ms"

    @pytest.mark.asyncio
    @patch('api.dashboard.execute_query_with_cache')
    async def test_teams_endpoint(self, mock_execute):
        """Test GET /api/dashboard/teams endpoint"""
        # Setup mocks for multiple queries
        mock_execute.side_effect = [
            MOCK_TEAMS_DATA,  # teams query
            [{"department": "Engineering", "count": 150}, {"department": "Sales", "count": 80}],  # dept query
            [{"skill": "Python", "count": 120}, {"skill": "React", "count": 85}]  # skills query
        ]
        
        # Make request
        response = client.get("/api/dashboard/teams")
        
        # Verify response
        assert response.status_code == 200
        data = response.json()
        
        assert "teams" in data
        assert "departments" in data
        assert "top_skills" in data
        assert "total_teams" in data
        assert "avg_team_size" in data
        
        assert len(data["teams"]) == 2
        assert data["teams"][0]["name"] == "Platform Engineering"
        assert data["departments"][0]["name"] == "Engineering"
        assert data["top_skills"][0]["skill"] == "Python"
        
        # Verify mock was called correctly
        assert mock_execute.call_count == 3

    @pytest.mark.asyncio
    @patch('api.dashboard.execute_query_with_cache')
    async def test_visas_endpoint(self, mock_execute):
        """Test GET /api/dashboard/visas endpoint"""
        # Setup mock data
        mock_visa_data = [
            {
                "employee_name": "Carlos Rodriguez",
                "department": "Engineering",
                "office": "Madrid",
                "visa_type": "H-1B",
                "hire_date": "2022-01-15T00:00:00Z",
                "email": "carlos@example.com"
            },
            {
                "employee_name": "Yuki Tanaka",
                "department": "Sales",
                "office": "Tokyo",
                "visa_type": "Work Permit",
                "hire_date": "2021-06-01T00:00:00Z",
                "email": "yuki@example.com"
            }
        ]
        mock_execute.return_value = mock_visa_data
        
        # Make request
        response = client.get("/api/dashboard/visas")
        
        # Verify response
        assert response.status_code == 200
        data = response.json()
        
        assert "summary" in data
        assert "timeline" in data
        
        # Check summary
        summary = data["summary"]
        assert "expired" in summary
        assert "expiring_30_days" in summary
        assert "expiring_90_days" in summary
        assert "expiring_180_days" in summary
        assert "total_visa_holders" in summary
        
        # Check timeline
        timeline = data["timeline"]
        assert "expired" in timeline
        assert "expiring_30_days" in timeline
        
        # Verify mock was called
        mock_execute.assert_called_once()

    @pytest.mark.asyncio
    @patch('api.dashboard.get_redis_client')
    @patch('api.dashboard.get_falkor_client')
    async def test_caching_behavior(self, mock_falkor, mock_redis):
        """Test that caching works correctly"""
        # Setup mocks
        mock_redis_instance = MagicMock()
        mock_redis_instance.get.return_value = json.dumps(MOCK_OVERVIEW_DATA)
        mock_redis.return_value = mock_redis_instance
        
        # Make request (should hit cache)
        response = client.get("/api/dashboard/overview")
        
        # Verify response
        assert response.status_code == 200
        
        # Verify Redis was checked
        mock_redis_instance.get.assert_called()
        
        # Verify FalkorDB was NOT called (cache hit)
        mock_falkor.assert_not_called()

    @pytest.mark.asyncio
    @patch('api.dashboard.execute_query_with_cache')
    async def test_error_handling(self, mock_execute):
        """Test error handling in dashboard endpoints"""
        # Setup mock to raise exception
        mock_execute.side_effect = Exception("Database connection failed")
        
        # Make request
        response = client.get("/api/dashboard/overview")
        
        # Verify error response
        assert response.status_code == 500
        assert "detail" in response.json()

    @pytest.mark.asyncio
    @patch('api.dashboard.execute_query_with_cache')
    async def test_timeout_handling(self, mock_execute):
        """Test timeout handling in dashboard endpoints"""
        # Setup mock to raise timeout
        mock_execute.side_effect = asyncio.TimeoutError()
        
        # Make request
        response = client.get("/api/dashboard/overview")
        
        # Verify timeout response
        assert response.status_code == 504
        assert response.json()["detail"] == "Query timeout"


if __name__ == "__main__":
    # Run tests
    pytest.main([__file__, "-v"])