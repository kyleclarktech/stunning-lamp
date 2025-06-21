"""Organizational entity generators (Teams, Groups, Offices)."""

import random
from typing import List, Dict, Any
from datetime import datetime, timedelta
from ..base import BaseGenerator, generate_date_range
from ..config import TEAMS_COUNT, GROUPS_COUNT, OFFICES_COUNT, REGIONS


class TeamsGenerator(BaseGenerator):
    """Generator for Team entities."""
    
    def generate(self) -> List[Dict[str, Any]]:
        """Generate team data for a B2B data analytics platform."""
        teams = [
            # Data Platform Engineering Teams
            {"id": "team_1", "name": "Data Ingestion", "department": "Data Platform Engineering", 
             "focus": "Real-time and batch data ingestion pipelines"},
            {"id": "team_2", "name": "Data Processing", "department": "Data Platform Engineering", 
             "focus": "Distributed data processing and transformation systems"},
            {"id": "team_3", "name": "Storage & Query", "department": "Data Platform Engineering", 
             "focus": "Data lake, warehouse, and query optimization"},
            {"id": "team_4", "name": "Streaming Platform", "department": "Data Platform Engineering", 
             "focus": "Real-time streaming infrastructure and event processing"},
            {"id": "team_5", "name": "Data Quality", "department": "Data Platform Engineering", 
             "focus": "Data validation, quality monitoring, and lineage tracking"},
            
            # Analytics Engineering Teams
            {"id": "team_6", "name": "Analytics Platform", "department": "Analytics Engineering", 
             "focus": "Self-service analytics platform and tools"},
            {"id": "team_7", "name": "Data Modeling", "department": "Analytics Engineering", 
             "focus": "Semantic layer, metrics definitions, and data models"},
            {"id": "team_8", "name": "BI Tools", "department": "Analytics Engineering", 
             "focus": "Business intelligence tools and visualization platforms"},
            
            # Engineering Teams
            {"id": "team_9", "name": "API Platform", "department": "Engineering", 
             "focus": "REST and GraphQL APIs for data access"},
            {"id": "team_10", "name": "Frontend Applications", "department": "Engineering", 
             "focus": "Web applications and user interfaces"},
            {"id": "team_11", "name": "Authentication & Access", "department": "Engineering", 
             "focus": "Identity management, SSO, and access control"},
            {"id": "team_12", "name": "Developer Experience", "department": "Engineering", 
             "focus": "SDKs, documentation, and developer tools"},
            
            # Data Science Teams
            {"id": "team_13", "name": "ML Infrastructure", "department": "Data Science", 
             "focus": "Machine learning platform and model serving"},
            {"id": "team_14", "name": "Advanced Analytics", "department": "Data Science", 
             "focus": "Predictive analytics and AI-powered insights"},
            {"id": "team_15", "name": "Data Science Tools", "department": "Data Science", 
             "focus": "Notebooks, experimentation, and ML workflows"},
            
            # Product Teams
            {"id": "team_16", "name": "Platform Product", "department": "Product", 
             "focus": "Core data platform capabilities and roadmap"},
            {"id": "team_17", "name": "Analytics Product", "department": "Product", 
             "focus": "Analytics features and visualization tools"},
            {"id": "team_18", "name": "Enterprise Product", "department": "Product", 
             "focus": "Enterprise features, governance, and compliance"},
            {"id": "team_19", "name": "Integration Product", "department": "Product", 
             "focus": "Connectors, integrations, and data sources"},
            
            # Infrastructure & DevOps Teams
            {"id": "team_20", "name": "Cloud Infrastructure", "department": "Infrastructure & DevOps", 
             "focus": "Multi-cloud infrastructure and Kubernetes"},
            {"id": "team_21", "name": "Site Reliability", "department": "Infrastructure & DevOps", 
             "focus": "System reliability, monitoring, and incident response"},
            {"id": "team_22", "name": "Database Operations", "department": "Infrastructure & DevOps", 
             "focus": "Database management and optimization"},
            
            # Security & Compliance Teams
            {"id": "team_23", "name": "Data Security", "department": "Security & Compliance", 
             "focus": "Data encryption, access control, and security"},
            {"id": "team_24", "name": "Compliance & Privacy", "department": "Security & Compliance", 
             "focus": "GDPR, CCPA, SOC2, and regulatory compliance"},
            {"id": "team_25", "name": "Security Operations", "department": "Security & Compliance", 
             "focus": "Security monitoring and incident response"},
            
            # Customer Success Teams
            {"id": "team_26", "name": "Enterprise Success", "department": "Customer Success", 
             "focus": "Strategic account management and success"},
            {"id": "team_27", "name": "Technical Success", "department": "Customer Success", 
             "focus": "Technical implementation and support"},
            {"id": "team_28", "name": "Customer Education", "department": "Customer Success", 
             "focus": "Training, certification, and documentation"},
            
            # Professional Services Teams
            {"id": "team_29", "name": "Implementation Services", "department": "Professional Services", 
             "focus": "Customer implementations and migrations"},
            {"id": "team_30", "name": "Data Architecture", "department": "Professional Services", 
             "focus": "Data architecture consulting and best practices"},
            {"id": "team_31", "name": "Analytics Consulting", "department": "Professional Services", 
             "focus": "Analytics strategy and use case development"},
            
            # Sales Teams
            {"id": "team_32", "name": "Enterprise Sales", "department": "Sales", 
             "focus": "Fortune 500 and large enterprise accounts"},
            {"id": "team_33", "name": "Mid-Market Sales", "department": "Sales", 
             "focus": "Mid-market and growth company accounts"},
            {"id": "team_34", "name": "Partner Sales", "department": "Sales", 
             "focus": "Channel partners and technology alliances"},
            
            # Solutions Architecture Teams
            {"id": "team_35", "name": "Enterprise Architecture", "department": "Solutions Architecture", 
             "focus": "Enterprise data architecture and strategy"},
            {"id": "team_36", "name": "Technical Solutions", "department": "Solutions Architecture", 
             "focus": "Technical demonstrations and proof of concepts"},
            {"id": "team_37", "name": "Integration Architecture", "department": "Solutions Architecture", 
             "focus": "Integration patterns and best practices"}
        ]
        
        return teams


class GroupsGenerator(BaseGenerator):
    """Generator for Group entities."""
    
    def generate(self) -> List[Dict[str, Any]]:
        """Generate cross-functional groups."""
        groups = [
            # Executive groups
            {"id": "group_1", "name": "Executive Leadership Team", "type": "governance", 
             "description": "C-suite and VP-level leadership", "lead_department": "Executive"},
            {"id": "group_2", "name": "Product Council", "type": "governance", 
             "description": "Product strategy and roadmap decisions", "lead_department": "Product"},
            
            # Technical groups
            {"id": "group_3", "name": "Architecture Review Board", "type": "technical", 
             "description": "Technical architecture decisions and standards", "lead_department": "Engineering"},
            {"id": "group_4", "name": "Data Governance Council", "type": "governance", 
             "description": "Data quality, privacy, and governance policies", "lead_department": "Data Platform Engineering"},
            {"id": "group_5", "name": "Security Champions", "type": "technical", 
             "description": "Security best practices and vulnerability management", "lead_department": "Security & Compliance"},
            
            # Operational groups
            {"id": "group_6", "name": "Change Advisory Board", "type": "operational", 
             "description": "Production change management and approvals", "lead_department": "Infrastructure & DevOps"},
            {"id": "group_7", "name": "Incident Response Team", "type": "operational", 
             "description": "Major incident response and coordination", "lead_department": "Infrastructure & DevOps"},
            {"id": "group_8", "name": "Customer Advisory Board", "type": "governance", 
             "description": "Strategic customer feedback and direction", "lead_department": "Customer Success"},
            
            # Culture and people groups
            {"id": "group_9", "name": "Diversity & Inclusion Council", "type": "culture", 
             "description": "Promoting diversity and inclusive practices", "lead_department": "People Operations"},
            {"id": "group_10", "name": "Learning & Development Committee", "type": "culture", 
             "description": "Employee growth and training programs", "lead_department": "People Operations"},
            
            # Process improvement groups
            {"id": "group_11", "name": "DevOps Guild", "type": "technical", 
             "description": "DevOps practices and tooling standards", "lead_department": "Infrastructure & DevOps"},
            {"id": "group_12", "name": "Agile Center of Excellence", "type": "operational", 
             "description": "Agile methodology and process improvement", "lead_department": "Engineering"},
            
            # Strategic groups
            {"id": "group_13", "name": "Innovation Lab", "type": "technical", 
             "description": "Emerging technologies and proof of concepts", "lead_department": "Data Science"},
            {"id": "group_14", "name": "Partner Alliance Council", "type": "governance", 
             "description": "Strategic partnerships and integrations", "lead_department": "Sales"},
            {"id": "group_15", "name": "SLA & Performance Committee", "type": "operational", 
             "description": "Service level agreements and performance metrics", "lead_department": "Customer Success"}
        ]
        
        return groups


class OfficesGenerator(BaseGenerator):
    """Generator for Office entities."""
    
    def generate(self) -> List[Dict[str, Any]]:
        """Generate office locations with global coverage."""
        offices = [
            {
                "id": "office_1",
                "name": "San Francisco HQ",
                "city": "San Francisco",
                "country": "United States",
                "country_code": "US",
                "region": "AMERICAS",
                "timezone": "America/Los_Angeles",
                "timezone_offset": -8,
                "business_hours_start": "09:00",
                "business_hours_end": "18:00",
                "business_hours_start_utc": "17:00",  # 9 AM PST = 5 PM UTC
                "business_hours_end_utc": "02:00",    # 6 PM PST = 2 AM UTC next day
                "languages": ["English"],
                "currency": "USD",
                "data_residency_zone": "US",
                "is_headquarters": True,
                "established_date": "2020-01-15"
            },
            {
                "id": "office_2",
                "name": "New York",
                "city": "New York",
                "country": "United States",
                "country_code": "US",
                "region": "AMERICAS",
                "timezone": "America/New_York",
                "timezone_offset": -5,
                "business_hours_start": "09:00",
                "business_hours_end": "18:00",
                "business_hours_start_utc": "14:00",  # 9 AM EST = 2 PM UTC
                "business_hours_end_utc": "23:00",    # 6 PM EST = 11 PM UTC
                "languages": ["English", "Spanish"],
                "currency": "USD",
                "data_residency_zone": "US",
                "is_headquarters": False,
                "established_date": "2021-03-01"
            },
            {
                "id": "office_3",
                "name": "London",
                "city": "London",
                "country": "United Kingdom",
                "country_code": "GB",
                "region": "EMEA",
                "timezone": "Europe/London",
                "timezone_offset": 0,
                "business_hours_start": "09:00",
                "business_hours_end": "18:00",
                "business_hours_start_utc": "09:00",  # GMT = UTC
                "business_hours_end_utc": "18:00",
                "languages": ["English"],
                "currency": "GBP",
                "data_residency_zone": "EU",
                "is_headquarters": False,
                "established_date": "2021-06-15"
            },
            {
                "id": "office_4",
                "name": "Berlin",
                "city": "Berlin",
                "country": "Germany",
                "country_code": "DE",
                "region": "EMEA",
                "timezone": "Europe/Berlin",
                "timezone_offset": 1,
                "business_hours_start": "09:00",
                "business_hours_end": "18:00",
                "business_hours_start_utc": "08:00",  # 9 AM CET = 8 AM UTC
                "business_hours_end_utc": "17:00",    # 6 PM CET = 5 PM UTC
                "languages": ["German", "English"],
                "currency": "EUR",
                "data_residency_zone": "EU",
                "is_headquarters": False,
                "established_date": "2022-01-10"
            },
            {
                "id": "office_5",
                "name": "Singapore",
                "city": "Singapore",
                "country": "Singapore",
                "country_code": "SG",
                "region": "APAC",
                "timezone": "Asia/Singapore",
                "timezone_offset": 8,
                "business_hours_start": "09:00",
                "business_hours_end": "18:00",
                "business_hours_start_utc": "01:00",  # 9 AM SGT = 1 AM UTC
                "business_hours_end_utc": "10:00",    # 6 PM SGT = 10 AM UTC
                "languages": ["English", "Mandarin", "Malay"],
                "currency": "SGD",
                "data_residency_zone": "APAC",
                "is_headquarters": False,
                "established_date": "2021-09-01"
            },
            {
                "id": "office_6",
                "name": "Tokyo",
                "city": "Tokyo",
                "country": "Japan",
                "country_code": "JP",
                "region": "APAC",
                "timezone": "Asia/Tokyo",
                "timezone_offset": 9,
                "business_hours_start": "09:00",
                "business_hours_end": "18:00",
                "business_hours_start_utc": "00:00",  # 9 AM JST = 12 AM UTC
                "business_hours_end_utc": "09:00",    # 6 PM JST = 9 AM UTC
                "languages": ["Japanese", "English"],
                "currency": "JPY",
                "data_residency_zone": "APAC",
                "is_headquarters": False,
                "established_date": "2022-04-01"
            },
            {
                "id": "office_7",
                "name": "Sydney",
                "city": "Sydney",
                "country": "Australia",
                "country_code": "AU",
                "region": "APAC",
                "timezone": "Australia/Sydney",
                "timezone_offset": 11,  # AEDT
                "business_hours_start": "09:00",
                "business_hours_end": "18:00",
                "business_hours_start_utc": "22:00",  # 9 AM AEDT = 10 PM UTC previous day
                "business_hours_end_utc": "07:00",    # 6 PM AEDT = 7 AM UTC
                "languages": ["English"],
                "currency": "AUD",
                "data_residency_zone": "APAC",
                "is_headquarters": False,
                "established_date": "2022-07-01"
            },
            {
                "id": "office_8",
                "name": "Toronto",
                "city": "Toronto",
                "country": "Canada",
                "country_code": "CA",
                "region": "AMERICAS",
                "timezone": "America/Toronto",
                "timezone_offset": -5,
                "business_hours_start": "09:00",
                "business_hours_end": "18:00",
                "business_hours_start_utc": "14:00",  # 9 AM EST = 2 PM UTC
                "business_hours_end_utc": "23:00",    # 6 PM EST = 11 PM UTC
                "languages": ["English", "French"],
                "currency": "CAD",
                "data_residency_zone": "CA",
                "is_headquarters": False,
                "established_date": "2022-10-15"
            }
        ]
        
        return offices