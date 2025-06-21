"""
Dashboard API endpoints for real-time analytics and visualization
"""
import asyncio
import json
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
from fastapi import APIRouter, HTTPException
from concurrent.futures import ThreadPoolExecutor
import redis
from falkordb import FalkorDB

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/dashboard", tags=["dashboard"])

# Redis cache configuration
CACHE_TTL = 60  # 60 seconds cache for dashboard data
redis_client = None

def get_redis_client():
    """Get or create Redis client for caching"""
    global redis_client
    if redis_client is None:
        try:
            redis_client = redis.Redis(host='redis', port=6380, decode_responses=True)
            redis_client.ping()
        except Exception as e:
            logger.warning(f"Redis not available for caching: {e}")
            redis_client = None
    return redis_client

def get_falkor_client():
    """Create FalkorDB client"""
    try:
        return FalkorDB(host="falkordb", port=6379)
    except Exception as e:
        logger.error(f"Failed to connect to FalkorDB: {e}")
        raise HTTPException(status_code=500, detail="Database connection failed")

async def execute_query_with_cache(
    cache_key: str, 
    query: str, 
    params: Optional[Dict] = None,
    timeout: float = 15.0
) -> List[Dict[str, Any]]:
    """Execute FalkorDB query with Redis caching"""
    # Try to get from cache first
    cache = get_redis_client()
    if cache:
        try:
            cached = cache.get(cache_key)
            if cached:
                logger.info(f"Cache hit for {cache_key}")
                return json.loads(cached)
        except Exception as e:
            logger.warning(f"Cache read error: {e}")
    
    # Execute query
    loop = asyncio.get_event_loop()
    db = get_falkor_client()
    graph = db.select_graph("agent_poc")
    
    with ThreadPoolExecutor() as executor:
        try:
            result = await asyncio.wait_for(
                loop.run_in_executor(executor, graph.query, query, params),
                timeout=timeout
            )
            
            # Process results
            data = []
            for record in result.result_set:
                row = {}
                for i, key in enumerate(result.header):
                    value = record[i]
                    if hasattr(value, 'properties'):
                        row[key] = value.properties
                    else:
                        row[key] = value
                data.append(row)
            
            # Cache the results
            if cache and data:
                try:
                    cache.setex(cache_key, CACHE_TTL, json.dumps(data))
                except Exception as e:
                    logger.warning(f"Cache write error: {e}")
            
            return data
            
        except asyncio.TimeoutError:
            logger.error(f"Query timeout for {cache_key}")
            raise HTTPException(status_code=504, detail="Query timeout")
        except Exception as e:
            logger.error(f"Query error for {cache_key}: {e}")
            raise HTTPException(status_code=500, detail=str(e))
        finally:
            db.close()

@router.get("/overview")
async def get_dashboard_overview() -> Dict[str, Any]:
    """Get global metrics summary including total employees, teams, policies, and system health"""
    
    # Query for basic counts
    counts_query = """
    MATCH (p:Person) WITH COUNT(p) as total_employees
    MATCH (t:Team) WITH total_employees, COUNT(t) as total_teams
    MATCH (g:Group) WITH total_employees, total_teams, COUNT(g) as total_groups
    MATCH (pol:Policy) WITH total_employees, total_teams, total_groups, COUNT(pol) as total_policies
    MATCH (pr:Project) WHERE pr.status = 'active' WITH total_employees, total_teams, total_groups, total_policies, COUNT(pr) as active_projects
    MATCH (o:Office) WITH total_employees, total_teams, total_groups, total_policies, active_projects, COUNT(o) as total_offices
    MATCH (s:Skill) WITH total_employees, total_teams, total_groups, total_policies, active_projects, total_offices, COUNT(DISTINCT s) as total_skills
    RETURN total_employees, total_teams, total_groups, total_policies, active_projects, total_offices, total_skills
    """
    
    # Query for active incidents (simulated - in real system would have Incident nodes)
    # For now, we'll count critical policies as potential incidents
    incidents_query = """
    MATCH (p:Policy) WHERE p.severity = 'critical'
    RETURN COUNT(p) as critical_incidents
    """
    
    # Execute queries
    counts = await execute_query_with_cache("dashboard:overview:counts", counts_query)
    incidents = await execute_query_with_cache("dashboard:overview:incidents", incidents_query)
    
    # Build response
    overview = {
        "total_employees": counts[0]["total_employees"] if counts else 0,
        "total_teams": counts[0]["total_teams"] if counts else 0,
        "total_groups": counts[0]["total_groups"] if counts else 0,
        "total_policies": counts[0]["total_policies"] if counts else 0,
        "active_projects": counts[0]["active_projects"] if counts else 0,
        "total_offices": counts[0]["total_offices"] if counts else 0,
        "total_skills": counts[0]["total_skills"] if counts else 0,
        "active_incidents": incidents[0]["critical_incidents"] if incidents else 0,
        "system_health": "operational",  # Would be calculated based on metrics
        "last_updated": datetime.utcnow().isoformat()
    }
    
    return overview

@router.get("/offices")
async def get_office_status() -> List[Dict[str, Any]]:
    """Get office status with on-call data and employee counts"""
    
    query = """
    MATCH (o:Office)
    OPTIONAL MATCH (p:Person)-[:WORKS_IN]->(o)
    WITH o, COUNT(DISTINCT p) as employee_count
    OPTIONAL MATCH (lead:Person)-[:WORKS_IN]->(o) WHERE lead.role CONTAINS 'Lead' OR lead.role CONTAINS 'Manager'
    WITH o, employee_count, COLLECT(DISTINCT lead) as office_leads
    RETURN o.name as office_name, 
           o.location as location, 
           o.timezone as timezone,
           employee_count,
           [l IN office_leads | {name: l.name, role: l.role, email: l.email}] as on_call_staff
    ORDER BY o.name
    """
    
    offices_data = await execute_query_with_cache("dashboard:offices", query)
    
    # Process and enhance office data
    offices = []
    for office in offices_data:
        # Determine office status based on local time
        tz_offset = int(office.get('timezone', 'UTC+0').replace('UTC', '').replace('+', ''))
        current_utc = datetime.utcnow()
        local_hour = (current_utc.hour + tz_offset) % 24
        
        status = "online" if 8 <= local_hour <= 18 else "offline"
        
        offices.append({
            "name": office["office_name"],
            "location": office["location"],
            "timezone": office["timezone"],
            "status": status,
            "employee_count": office["employee_count"],
            "on_call_staff": office["on_call_staff"][:3] if office["on_call_staff"] else [],  # Top 3 on-call
            "local_time": (current_utc + timedelta(hours=tz_offset)).strftime("%H:%M")
        })
    
    return offices

@router.get("/incidents")
async def get_active_incidents() -> Dict[str, List[Dict[str, Any]]]:
    """Get active incidents grouped by severity (simulated using policy violations)"""
    
    # In a real system, we'd have Incident nodes. For now, simulate with policies
    query = """
    MATCH (p:Policy)
    OPTIONAL MATCH (person:Person)-[:RESPONSIBLE_FOR]->(p)
    WITH p, COLLECT(DISTINCT person)[0] as assignee
    RETURN p.name as title,
           p.severity as severity,
           p.category as category,
           assignee.name as assignee_name,
           assignee.email as assignee_email,
           p.name as id
    ORDER BY 
        CASE p.severity 
            WHEN 'critical' THEN 1
            WHEN 'high' THEN 2
            WHEN 'medium' THEN 3
            WHEN 'low' THEN 4
            ELSE 5
        END
    """
    
    incidents_data = await execute_query_with_cache("dashboard:incidents", query)
    
    # Group by severity and simulate incident data
    incidents_by_severity = {
        "critical": [],
        "high": [],
        "medium": [],
        "low": []
    }
    
    for idx, incident in enumerate(incidents_data[:20]):  # Limit to 20 for dashboard
        severity = incident.get("severity", "medium")
        
        incident_obj = {
            "id": f"INC-{idx+1001}",
            "title": f"Policy Review: {incident['title']}",
            "severity": severity,
            "category": incident.get("category", "compliance"),
            "status": "active" if severity in ["critical", "high"] else "monitoring",
            "assignee": {
                "name": incident.get("assignee_name", "Unassigned"),
                "email": incident.get("assignee_email", "")
            },
            "created_at": (datetime.utcnow() - timedelta(hours=idx*3)).isoformat(),
            "updated_at": datetime.utcnow().isoformat()
        }
        
        if severity in incidents_by_severity:
            incidents_by_severity[severity].append(incident_obj)
    
    return incidents_by_severity

@router.get("/metrics")
async def get_performance_metrics() -> Dict[str, Any]:
    """Get performance metrics timeseries data for charts"""
    
    # Generate sample timeseries data for the last 7 days
    # In production, this would query actual metrics storage
    
    end_date = datetime.utcnow()
    start_date = end_date - timedelta(days=7)
    
    # Generate hourly data points
    timestamps = []
    current = start_date
    while current <= end_date:
        timestamps.append(current.isoformat())
        current += timedelta(hours=1)
    
    # Simulate different metrics
    import random
    random.seed(42)  # For consistent demo data
    
    metrics = {
        "timestamps": timestamps,
        "query_response_time": {
            "label": "Query Response Time (ms)",
            "data": [random.randint(50, 200) + random.randint(-20, 20) for _ in timestamps],
            "unit": "ms"
        },
        "active_users": {
            "label": "Active Users",
            "data": [random.randint(20, 100) for _ in timestamps],
            "unit": "users"
        },
        "api_requests": {
            "label": "API Requests/hour",
            "data": [random.randint(100, 500) for _ in timestamps],
            "unit": "requests"
        },
        "cache_hit_rate": {
            "label": "Cache Hit Rate (%)",
            "data": [random.randint(70, 95) for _ in timestamps],
            "unit": "%"
        },
        "error_rate": {
            "label": "Error Rate (%)",
            "data": [random.uniform(0.1, 2.0) for _ in timestamps],
            "unit": "%"
        }
    }
    
    return metrics

@router.get("/teams")
async def get_team_distribution() -> Dict[str, Any]:
    """Get team distribution data across offices and departments"""
    
    # Query for team distribution
    teams_query = """
    MATCH (t:Team)
    OPTIONAL MATCH (p:Person)-[:MEMBER_OF]->(t)
    WITH t, COUNT(DISTINCT p) as member_count
    RETURN t.name as team_name,
           t.department as department,
           t.focus_area as focus_area,
           member_count
    ORDER BY member_count DESC
    """
    
    # Query for department distribution
    dept_query = """
    MATCH (p:Person)
    RETURN p.department as department, COUNT(p) as count
    ORDER BY count DESC
    """
    
    # Query for skills distribution
    skills_query = """
    MATCH (p:Person)-[:HAS_SKILL]->(s:Skill)
    RETURN s.name as skill, COUNT(DISTINCT p) as count
    ORDER BY count DESC
    LIMIT 10
    """
    
    teams_data = await execute_query_with_cache("dashboard:teams", teams_query)
    dept_data = await execute_query_with_cache("dashboard:departments", dept_query)
    skills_data = await execute_query_with_cache("dashboard:skills", skills_query)
    
    return {
        "teams": [
            {
                "name": team["team_name"],
                "department": team["department"],
                "focus_area": team["focus_area"],
                "member_count": team["member_count"]
            }
            for team in teams_data
        ],
        "departments": [
            {
                "name": dept["department"],
                "count": dept["count"]
            }
            for dept in dept_data
        ],
        "top_skills": [
            {
                "skill": skill["skill"],
                "count": skill["count"]
            }
            for skill in skills_data
        ],
        "total_teams": len(teams_data),
        "avg_team_size": sum(t["member_count"] for t in teams_data) / len(teams_data) if teams_data else 0
    }

@router.get("/visas")
async def get_visa_timeline() -> Dict[str, Any]:
    """Get visa expiry timeline data for employees"""
    
    # Query for visa expiry data
    # In this simulation, we'll use hire_date + random offset as visa expiry
    query = """
    MATCH (p:Person) WHERE p.visa_status IS NOT NULL AND p.visa_status <> 'Citizen'
    RETURN p.name as employee_name,
           p.department as department,
           p.office as office,
           p.visa_status as visa_type,
           p.hire_date as hire_date,
           p.email as email
    ORDER BY p.hire_date DESC
    LIMIT 50
    """
    
    visa_data = await execute_query_with_cache("dashboard:visas", query)
    
    # Process visa data and simulate expiry dates
    current_date = datetime.utcnow()
    expiring_30_days = []
    expiring_90_days = []
    expiring_180_days = []
    expired = []
    
    for idx, person in enumerate(visa_data):
        # Simulate visa expiry based on hire date + 2-4 years
        hire_date = datetime.fromisoformat(person["hire_date"].replace('Z', '+00:00'))
        visa_duration_days = 730 + (idx * 30)  # 2 years + incremental days
        expiry_date = hire_date + timedelta(days=visa_duration_days)
        days_until_expiry = (expiry_date - current_date).days
        
        visa_info = {
            "employee_name": person["employee_name"],
            "department": person["department"],
            "office": person["office"],
            "visa_type": person["visa_type"],
            "email": person["email"],
            "expiry_date": expiry_date.isoformat(),
            "days_until_expiry": days_until_expiry
        }
        
        if days_until_expiry < 0:
            expired.append(visa_info)
        elif days_until_expiry <= 30:
            expiring_30_days.append(visa_info)
        elif days_until_expiry <= 90:
            expiring_90_days.append(visa_info)
        elif days_until_expiry <= 180:
            expiring_180_days.append(visa_info)
    
    return {
        "summary": {
            "expired": len(expired),
            "expiring_30_days": len(expiring_30_days),
            "expiring_90_days": len(expiring_90_days),
            "expiring_180_days": len(expiring_180_days),
            "total_visa_holders": len(visa_data)
        },
        "timeline": {
            "expired": expired[:5],  # Top 5 for dashboard
            "expiring_30_days": expiring_30_days[:5],
            "expiring_90_days": expiring_90_days[:5],
            "expiring_180_days": expiring_180_days[:5]
        },
        "by_visa_type": {}  # Could add breakdown by visa type
    }