import json
import falkordb
from faker import Faker
import random
from datetime import datetime, timedelta
import os
import sys

# Add parent directory to path to access environment variables
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

fake = Faker()

def generate_skills_data():
    """Generate technical skills and competencies"""
    skills = [
        # Programming Languages
        {"id": "skill_1", "name": "Python", "category": "programming", "type": "language"},
        {"id": "skill_2", "name": "Java", "category": "programming", "type": "language"},
        {"id": "skill_3", "name": "Go", "category": "programming", "type": "language"},
        {"id": "skill_4", "name": "JavaScript", "category": "programming", "type": "language"},
        {"id": "skill_5", "name": "TypeScript", "category": "programming", "type": "language"},
        {"id": "skill_6", "name": "SQL", "category": "programming", "type": "language"},
        {"id": "skill_7", "name": "Scala", "category": "programming", "type": "language"},
        {"id": "skill_8", "name": "Rust", "category": "programming", "type": "language"},
        
        # Cloud Platforms
        {"id": "skill_9", "name": "AWS", "category": "cloud", "type": "platform"},
        {"id": "skill_10", "name": "GCP", "category": "cloud", "type": "platform"},
        {"id": "skill_11", "name": "Azure", "category": "cloud", "type": "platform"},
        
        # Data Technologies
        {"id": "skill_12", "name": "Apache Spark", "category": "data", "type": "framework"},
        {"id": "skill_13", "name": "Apache Kafka", "category": "data", "type": "framework"},
        {"id": "skill_14", "name": "Apache Airflow", "category": "data", "type": "framework"},
        {"id": "skill_15", "name": "Snowflake", "category": "data", "type": "database"},
        {"id": "skill_16", "name": "BigQuery", "category": "data", "type": "database"},
        {"id": "skill_17", "name": "Databricks", "category": "data", "type": "platform"},
        {"id": "skill_18", "name": "dbt", "category": "data", "type": "tool"},
        {"id": "skill_19", "name": "Apache Flink", "category": "data", "type": "framework"},
        {"id": "skill_20", "name": "Elasticsearch", "category": "data", "type": "database"},
        
        # Machine Learning
        {"id": "skill_21", "name": "TensorFlow", "category": "ml", "type": "framework"},
        {"id": "skill_22", "name": "PyTorch", "category": "ml", "type": "framework"},
        {"id": "skill_23", "name": "Scikit-learn", "category": "ml", "type": "framework"},
        {"id": "skill_24", "name": "MLflow", "category": "ml", "type": "platform"},
        {"id": "skill_25", "name": "Kubeflow", "category": "ml", "type": "platform"},
        
        # DevOps & Infrastructure
        {"id": "skill_26", "name": "Kubernetes", "category": "devops", "type": "platform"},
        {"id": "skill_27", "name": "Docker", "category": "devops", "type": "platform"},
        {"id": "skill_28", "name": "Terraform", "category": "devops", "type": "tool"},
        {"id": "skill_29", "name": "Helm", "category": "devops", "type": "tool"},
        {"id": "skill_30", "name": "Jenkins", "category": "devops", "type": "tool"},
        {"id": "skill_31", "name": "GitLab CI", "category": "devops", "type": "tool"},
        {"id": "skill_32", "name": "Prometheus", "category": "devops", "type": "monitoring"},
        {"id": "skill_33", "name": "Grafana", "category": "devops", "type": "monitoring"},
        
        # Databases
        {"id": "skill_34", "name": "PostgreSQL", "category": "database", "type": "relational"},
        {"id": "skill_35", "name": "MySQL", "category": "database", "type": "relational"},
        {"id": "skill_36", "name": "MongoDB", "category": "database", "type": "nosql"},
        {"id": "skill_37", "name": "Redis", "category": "database", "type": "nosql"},
        {"id": "skill_38", "name": "Cassandra", "category": "database", "type": "nosql"},
        
        # Domain Expertise
        {"id": "skill_39", "name": "Data Architecture", "category": "domain", "type": "expertise"},
        {"id": "skill_40", "name": "Data Governance", "category": "domain", "type": "expertise"},
        {"id": "skill_41", "name": "Data Modeling", "category": "domain", "type": "expertise"},
        {"id": "skill_42", "name": "ETL/ELT", "category": "domain", "type": "expertise"},
        {"id": "skill_43", "name": "Real-time Processing", "category": "domain", "type": "expertise"},
        {"id": "skill_44", "name": "Data Quality", "category": "domain", "type": "expertise"},
        {"id": "skill_45", "name": "Analytics Engineering", "category": "domain", "type": "expertise"},
        {"id": "skill_46", "name": "Security & Compliance", "category": "domain", "type": "expertise"},
        {"id": "skill_47", "name": "Performance Optimization", "category": "domain", "type": "expertise"},
        {"id": "skill_48", "name": "Distributed Systems", "category": "domain", "type": "expertise"},
        
        # Certifications
        {"id": "skill_49", "name": "AWS Certified Solutions Architect", "category": "certification", "type": "aws"},
        {"id": "skill_50", "name": "GCP Professional Data Engineer", "category": "certification", "type": "gcp"},
        {"id": "skill_51", "name": "Certified Kubernetes Administrator", "category": "certification", "type": "cncf"},
        {"id": "skill_52", "name": "Databricks Certified Data Engineer", "category": "certification", "type": "databricks"}
    ]
    return skills

def generate_projects_data():
    """Generate project data"""
    projects = []
    project_names = [
        {"name": "Data Lake Modernization", "type": "infrastructure", "client_id": "client_1"},  # Financial Services
        {"name": "Real-time Analytics Platform", "type": "platform", "client_id": "client_2"},  # Retail
        {"name": "ML Pipeline Implementation", "type": "ml", "client_id": "client_3"},  # Healthcare
        {"name": "Customer 360 Data Platform", "type": "analytics", "client_id": "client_4"},  # Manufacturing
        {"name": "Cost Optimization Initiative", "type": "optimization", "client_id": "client_5"},  # Telecom
        {"name": "Data Governance Framework", "type": "governance", "client_id": "client_6"},  # E-commerce
        {"name": "Multi-Cloud Migration", "type": "infrastructure", "client_id": "client_7"},  # Media
        {"name": "Streaming Data Pipeline", "type": "platform", "client_id": "client_8"},  # Energy
        {"name": "Self-Service Analytics Portal", "type": "analytics", "client_id": "client_9"},  # Pharmaceutical
        {"name": "API Platform v2.0", "type": "platform", "client_id": "client_10"},  # Logistics
        {"name": "Security Compliance Audit", "type": "governance", "client_id": "client_11"},  # Insurance
        {"name": "Performance Optimization Sprint", "type": "optimization", "client_id": "client_12"},  # Education
        {"name": "Predictive Maintenance System", "type": "ml", "client_id": "client_13"},  # Government
        {"name": "Cloud-Native Data Platform", "type": "platform", "client_id": "client_14"},  # Technology
        {"name": "Risk Analytics Engine", "type": "analytics", "client_id": "client_15"},  # Banking (Financial)
        {"name": "Patient Data Integration", "type": "platform", "client_id": "client_16"},  # Healthcare
        {"name": "Supply Chain Analytics", "type": "analytics", "client_id": "client_17"},  # Manufacturing
        {"name": "Recommendation Engine", "type": "ml", "client_id": "client_18"},  # E-commerce
        {"name": "Content Analytics Platform", "type": "analytics", "client_id": "client_19"},  # Media
        {"name": "Grid Optimization System", "type": "optimization", "client_id": "client_20"}  # Energy
    ]
    
    for i, proj in enumerate(project_names):
        start_date = fake.date_between(start_date='-6m', end_date='+3m')
        duration_weeks = random.randint(8, 26)
        end_date = start_date + timedelta(weeks=duration_weeks)
        
        project = {
            "id": f"project_{i+1}",
            "name": proj["name"],
            "type": proj["type"],
            "status": random.choice(["planning", "active", "on_hold", "completed"]),
            "start_date": start_date.isoformat(),
            "end_date": end_date.isoformat(),
            "budget": random.randint(100000, 2000000),
            "priority": random.choice(["high", "medium", "low"]),
            "client_id": proj["client_id"],
            "description": f"Implementation of {proj['name']} for enterprise client"
        }
        projects.append(project)
    
    return projects

def generate_clients_data():
    """Generate client data with at least one client per industry"""
    clients = []
    
    # Define all industries we want represented
    all_industries = [
        "Financial Services", "Retail", "Healthcare", "Manufacturing", "Telecom", 
        "E-commerce", "Media", "Energy", "Pharmaceutical", "Logistics", 
        "Insurance", "Education", "Government", "Technology"
    ]
    
    # Create specific clients for each industry to ensure representation
    industry_clients = [
        {"name": "Acme Financial Services", "industry": "Financial Services"},
        {"name": "Global Retail Corp", "industry": "Retail"},
        {"name": "HealthTech Solutions", "industry": "Healthcare"},
        {"name": "Manufacturing Industries", "industry": "Manufacturing"},
        {"name": "Telecomm Giant", "industry": "Telecom"},
        {"name": "E-commerce Leader", "industry": "E-commerce"},
        {"name": "Media Conglomerate", "industry": "Media"},
        {"name": "Energy Corporation", "industry": "Energy"},
        {"name": "Pharma Innovations", "industry": "Pharmaceutical"},
        {"name": "Logistics Network", "industry": "Logistics"},
        {"name": "Insurance Group", "industry": "Insurance"},
        {"name": "EduTech Platform", "industry": "Education"},
        {"name": "Federal Agency Systems", "industry": "Government"},
        {"name": "TechCorp Solutions", "industry": "Technology"},
        # Additional clients for variety
        {"name": "Banking Consortium", "industry": "Financial Services"},
        {"name": "Regional Health Network", "industry": "Healthcare"},
        {"name": "Smart Manufacturing Co", "industry": "Manufacturing"},
        {"name": "Digital Commerce Inc", "industry": "E-commerce"},
        {"name": "Streaming Media Services", "industry": "Media"},
        {"name": "Renewable Energy Partners", "industry": "Energy"}
    ]
    
    for i, client_info in enumerate(industry_clients):
        # Tier assignment based on industry and position
        if client_info["industry"] in ["Financial Services", "Healthcare", "Government"]:
            tier = random.choice(["enterprise", "strategic"])  # Higher tier for regulated industries
        elif i < len(all_industries):  # First client of each industry
            tier = "enterprise"  # Ensure at least one enterprise client per industry
        else:
            tier = random.choice(["enterprise", "mid-market", "strategic"])
        
        annual_value = random.randint(500000, 5000000) if tier == "mid-market" else random.randint(1000000, 10000000)
        
        # Define region and time zone mappings
        region_timezone_map = {
            "AMERICAS": ["America/New_York", "America/Chicago", "America/Los_Angeles", "America/Toronto"],
            "EMEA": ["Europe/London", "Europe/Paris", "Europe/Berlin", "Africa/Johannesburg"],
            "APAC": ["Asia/Tokyo", "Asia/Singapore", "Asia/Sydney", "Asia/Mumbai"]
        }
        
        # Assign primary region based on industry and randomization
        if client_info["industry"] == "Government" and "Federal" in client_info["name"]:
            primary_region = "AMERICAS"
        else:
            primary_region = random.choice(["AMERICAS", "EMEA", "APAC"])
        
        # Set support tier based on client tier
        support_tier_map = {
            "mid-market": random.choice(["Basic", "Professional"]),
            "enterprise": random.choice(["Professional", "Enterprise"]),
            "strategic": "Strategic"
        }
        
        client = {
            "id": f"client_{i+1}",
            "name": client_info["name"],
            "industry": client_info["industry"],
            "tier": tier,
            "annual_value": annual_value,
            "mrr": round(annual_value / 12, 2),
            "data_volume_gb": random.randint(100, 50000),
            "active_users": random.randint(10, 5000),
            "support_tier": support_tier_map[tier],
            "primary_region": primary_region,
            "time_zone_preferences": random.sample(region_timezone_map[primary_region], k=random.randint(1, 3)),
            "relationship_start": fake.date_between(start_date='-3y', end_date='-6m').isoformat()
        }
        clients.append(client)
    
    return clients

def generate_sprints_data():
    """Generate sprint data for projects"""
    sprints = []
    sprint_id = 1
    projects = generate_projects_data()
    
    for project in projects:
        if project["status"] in ["active", "completed"]:
            # Generate 2-6 sprints per project
            num_sprints = random.randint(2, 6)
            start_date = datetime.fromisoformat(project["start_date"])
            
            for i in range(num_sprints):
                sprint_start = start_date + timedelta(weeks=i*2)
                sprint_end = sprint_start + timedelta(weeks=2)
                
                sprint = {
                    "id": f"sprint_{sprint_id}",
                    "name": f"{project['name']} - Sprint {i+1}",
                    "project_id": project["id"],
                    "sprint_number": i + 1,
                    "start_date": sprint_start.isoformat(),
                    "end_date": sprint_end.isoformat(),
                    "status": "completed" if sprint_end < datetime.now() else "active" if sprint_start <= datetime.now() else "planned",
                    "velocity": random.randint(20, 60) if sprint_end < datetime.now() else None
                }
                sprints.append(sprint)
                sprint_id += 1
    
    return sprints

def generate_offices_data():
    """Generate global office data for 24/7 operations"""
    offices = [
        {
            "id": "office_sf",
            "name": "San Francisco HQ",
            "city": "San Francisco",
            "country": "United States",
            "country_code": "US",
            "region": "AMERICAS",
            "timezone": "US/Pacific",
            "timezone_offset": -8,
            "business_hours_start": "09:00",
            "business_hours_end": "18:00",
            "business_hours_start_utc": "17:00",  # 9am PST = 5pm UTC
            "business_hours_end_utc": "02:00",     # 6pm PST = 2am UTC next day
            "languages": ["en"],
            "currency": "USD",
            "data_residency_zone": "US",
            "is_headquarters": True,
            "established_date": "2018-03-15"
        },
        {
            "id": "office_ny",
            "name": "New York",
            "city": "New York",
            "country": "United States",
            "country_code": "US",
            "region": "AMERICAS",
            "timezone": "US/Eastern",
            "timezone_offset": -5,
            "business_hours_start": "09:00",
            "business_hours_end": "18:00",
            "business_hours_start_utc": "14:00",  # 9am EST = 2pm UTC
            "business_hours_end_utc": "23:00",     # 6pm EST = 11pm UTC
            "languages": ["en"],
            "currency": "USD",
            "data_residency_zone": "US",
            "is_headquarters": False,
            "established_date": "2019-06-01"
        },
        {
            "id": "office_london",
            "name": "London",
            "city": "London",
            "country": "United Kingdom",
            "country_code": "GB",
            "region": "EMEA",
            "timezone": "Europe/London",
            "timezone_offset": 0,
            "business_hours_start": "09:00",
            "business_hours_end": "18:00",
            "business_hours_start_utc": "09:00",  # 9am GMT = 9am UTC
            "business_hours_end_utc": "18:00",     # 6pm GMT = 6pm UTC
            "languages": ["en"],
            "currency": "GBP",
            "data_residency_zone": "EU",
            "is_headquarters": False,
            "established_date": "2020-02-15"
        },
        {
            "id": "office_frankfurt",
            "name": "Frankfurt",
            "city": "Frankfurt",
            "country": "Germany",
            "country_code": "DE",
            "region": "EMEA",
            "timezone": "Europe/Berlin",
            "timezone_offset": 1,
            "business_hours_start": "09:00",
            "business_hours_end": "18:00",
            "business_hours_start_utc": "08:00",  # 9am CET = 8am UTC
            "business_hours_end_utc": "17:00",     # 6pm CET = 5pm UTC
            "languages": ["de", "en"],
            "currency": "EUR",
            "data_residency_zone": "EU",
            "is_headquarters": False,
            "established_date": "2020-09-01"
        },
        {
            "id": "office_paris",
            "name": "Paris",
            "city": "Paris",
            "country": "France",
            "country_code": "FR",
            "region": "EMEA",
            "timezone": "Europe/Paris",
            "timezone_offset": 1,
            "business_hours_start": "09:00",
            "business_hours_end": "18:00",
            "business_hours_start_utc": "08:00",  # 9am CET = 8am UTC
            "business_hours_end_utc": "17:00",     # 6pm CET = 5pm UTC
            "languages": ["fr", "en"],
            "currency": "EUR",
            "data_residency_zone": "EU",
            "is_headquarters": False,
            "established_date": "2021-04-01"
        },
        {
            "id": "office_tokyo",
            "name": "Tokyo",
            "city": "Tokyo",
            "country": "Japan",
            "country_code": "JP",
            "region": "APAC",
            "timezone": "Asia/Tokyo",
            "timezone_offset": 9,
            "business_hours_start": "09:00",
            "business_hours_end": "18:00",
            "business_hours_start_utc": "00:00",  # 9am JST = 12am UTC
            "business_hours_end_utc": "09:00",     # 6pm JST = 9am UTC
            "languages": ["ja", "en"],
            "currency": "JPY",
            "data_residency_zone": "APAC",
            "is_headquarters": False,
            "established_date": "2021-10-01"
        },
        {
            "id": "office_hk",
            "name": "Hong Kong",
            "city": "Hong Kong",
            "country": "Hong Kong",
            "country_code": "HK",
            "region": "APAC",
            "timezone": "Asia/Hong_Kong",
            "timezone_offset": 8,
            "business_hours_start": "09:00",
            "business_hours_end": "18:00",
            "business_hours_start_utc": "01:00",  # 9am HKT = 1am UTC
            "business_hours_end_utc": "10:00",     # 6pm HKT = 10am UTC
            "languages": ["zh", "en"],
            "currency": "HKD",
            "data_residency_zone": "APAC",
            "is_headquarters": False,
            "established_date": "2022-01-15"
        },
        {
            "id": "office_sydney",
            "name": "Sydney",
            "city": "Sydney",
            "country": "Australia",
            "country_code": "AU",
            "region": "APAC",
            "timezone": "Australia/Sydney",
            "timezone_offset": 10,
            "business_hours_start": "09:00",
            "business_hours_end": "18:00",
            "business_hours_start_utc": "23:00",  # 9am AEDT = 11pm UTC previous day
            "business_hours_end_utc": "08:00",     # 6pm AEDT = 8am UTC
            "languages": ["en"],
            "currency": "AUD",
            "data_residency_zone": "APAC",
            "is_headquarters": False,
            "established_date": "2022-07-01"
        }
    ]
    return offices

def generate_languages_data():
    """Generate language data with ISO codes"""
    languages = [
        {"id": "lang_en", "code": "en", "name": "English", "native_name": "English", "script": "Latin", "direction": "ltr", "is_business_language": True},
        {"id": "lang_de", "code": "de", "name": "German", "native_name": "Deutsch", "script": "Latin", "direction": "ltr", "is_business_language": True},
        {"id": "lang_fr", "code": "fr", "name": "French", "native_name": "Français", "script": "Latin", "direction": "ltr", "is_business_language": True},
        {"id": "lang_es", "code": "es", "name": "Spanish", "native_name": "Español", "script": "Latin", "direction": "ltr", "is_business_language": True},
        {"id": "lang_ja", "code": "ja", "name": "Japanese", "native_name": "日本語", "script": "Japanese", "direction": "ltr", "is_business_language": True},
        {"id": "lang_zh", "code": "zh", "name": "Chinese", "native_name": "中文", "script": "Chinese", "direction": "ltr", "is_business_language": True},
        {"id": "lang_ko", "code": "ko", "name": "Korean", "native_name": "한국어", "script": "Korean", "direction": "ltr", "is_business_language": False},
        {"id": "lang_pt", "code": "pt", "name": "Portuguese", "native_name": "Português", "script": "Latin", "direction": "ltr", "is_business_language": False},
        {"id": "lang_it", "code": "it", "name": "Italian", "native_name": "Italiano", "script": "Latin", "direction": "ltr", "is_business_language": False},
        {"id": "lang_ru", "code": "ru", "name": "Russian", "native_name": "Русский", "script": "Cyrillic", "direction": "ltr", "is_business_language": False},
        {"id": "lang_ar", "code": "ar", "name": "Arabic", "native_name": "العربية", "script": "Arabic", "direction": "rtl", "is_business_language": False},
        {"id": "lang_hi", "code": "hi", "name": "Hindi", "native_name": "हिन्दी", "script": "Devanagari", "direction": "ltr", "is_business_language": False}
    ]
    return languages

def generate_holidays_data():
    """Generate holiday data for 2024-2025"""
    holidays = []
    
    # US holidays
    us_holidays_2024 = [
        {"name": "New Year's Day", "date": "2024-01-01", "offices": ["office_sf", "office_ny"]},
        {"name": "Martin Luther King Jr. Day", "date": "2024-01-15", "offices": ["office_sf", "office_ny"]},
        {"name": "Presidents Day", "date": "2024-02-19", "offices": ["office_sf", "office_ny"]},
        {"name": "Memorial Day", "date": "2024-05-27", "offices": ["office_sf", "office_ny"]},
        {"name": "Independence Day", "date": "2024-07-04", "offices": ["office_sf", "office_ny"]},
        {"name": "Labor Day", "date": "2024-09-02", "offices": ["office_sf", "office_ny"]},
        {"name": "Thanksgiving", "date": "2024-11-28", "offices": ["office_sf", "office_ny"]},
        {"name": "Day after Thanksgiving", "date": "2024-11-29", "offices": ["office_sf", "office_ny"]},
        {"name": "Christmas Day", "date": "2024-12-25", "offices": ["office_sf", "office_ny"]}
    ]
    
    # UK holidays
    uk_holidays_2024 = [
        {"name": "New Year's Day", "date": "2024-01-01", "offices": ["office_london"]},
        {"name": "Good Friday", "date": "2024-03-29", "offices": ["office_london"]},
        {"name": "Easter Monday", "date": "2024-04-01", "offices": ["office_london"]},
        {"name": "Early May Bank Holiday", "date": "2024-05-06", "offices": ["office_london"]},
        {"name": "Spring Bank Holiday", "date": "2024-05-27", "offices": ["office_london"]},
        {"name": "Summer Bank Holiday", "date": "2024-08-26", "offices": ["office_london"]},
        {"name": "Christmas Day", "date": "2024-12-25", "offices": ["office_london"]},
        {"name": "Boxing Day", "date": "2024-12-26", "offices": ["office_london"]}
    ]
    
    # German holidays
    de_holidays_2024 = [
        {"name": "New Year's Day", "date": "2024-01-01", "offices": ["office_frankfurt"]},
        {"name": "Good Friday", "date": "2024-03-29", "offices": ["office_frankfurt"]},
        {"name": "Easter Monday", "date": "2024-04-01", "offices": ["office_frankfurt"]},
        {"name": "Labour Day", "date": "2024-05-01", "offices": ["office_frankfurt"]},
        {"name": "Ascension Day", "date": "2024-05-09", "offices": ["office_frankfurt"]},
        {"name": "Whit Monday", "date": "2024-05-20", "offices": ["office_frankfurt"]},
        {"name": "German Unity Day", "date": "2024-10-03", "offices": ["office_frankfurt"]},
        {"name": "Christmas Day", "date": "2024-12-25", "offices": ["office_frankfurt"]},
        {"name": "Boxing Day", "date": "2024-12-26", "offices": ["office_frankfurt"]}
    ]
    
    # French holidays
    fr_holidays_2024 = [
        {"name": "New Year's Day", "date": "2024-01-01", "offices": ["office_paris"]},
        {"name": "Easter Monday", "date": "2024-04-01", "offices": ["office_paris"]},
        {"name": "Labour Day", "date": "2024-05-01", "offices": ["office_paris"]},
        {"name": "Victory in Europe Day", "date": "2024-05-08", "offices": ["office_paris"]},
        {"name": "Ascension Day", "date": "2024-05-09", "offices": ["office_paris"]},
        {"name": "Whit Monday", "date": "2024-05-20", "offices": ["office_paris"]},
        {"name": "Bastille Day", "date": "2024-07-14", "offices": ["office_paris"]},
        {"name": "Assumption Day", "date": "2024-08-15", "offices": ["office_paris"]},
        {"name": "All Saints' Day", "date": "2024-11-01", "offices": ["office_paris"]},
        {"name": "Armistice Day", "date": "2024-11-11", "offices": ["office_paris"]},
        {"name": "Christmas Day", "date": "2024-12-25", "offices": ["office_paris"]}
    ]
    
    # Japanese holidays
    jp_holidays_2024 = [
        {"name": "New Year's Day", "date": "2024-01-01", "offices": ["office_tokyo"]},
        {"name": "Coming of Age Day", "date": "2024-01-08", "offices": ["office_tokyo"]},
        {"name": "National Foundation Day", "date": "2024-02-11", "offices": ["office_tokyo"]},
        {"name": "Emperor's Birthday", "date": "2024-02-23", "offices": ["office_tokyo"]},
        {"name": "Vernal Equinox Day", "date": "2024-03-20", "offices": ["office_tokyo"]},
        {"name": "Showa Day", "date": "2024-04-29", "offices": ["office_tokyo"]},
        {"name": "Constitution Memorial Day", "date": "2024-05-03", "offices": ["office_tokyo"]},
        {"name": "Greenery Day", "date": "2024-05-04", "offices": ["office_tokyo"]},
        {"name": "Children's Day", "date": "2024-05-05", "offices": ["office_tokyo"]},
        {"name": "Marine Day", "date": "2024-07-15", "offices": ["office_tokyo"]},
        {"name": "Mountain Day", "date": "2024-08-11", "offices": ["office_tokyo"]},
        {"name": "Respect for the Aged Day", "date": "2024-09-16", "offices": ["office_tokyo"]},
        {"name": "Autumnal Equinox Day", "date": "2024-09-22", "offices": ["office_tokyo"]},
        {"name": "Health and Sports Day", "date": "2024-10-14", "offices": ["office_tokyo"]},
        {"name": "Culture Day", "date": "2024-11-03", "offices": ["office_tokyo"]},
        {"name": "Labour Thanksgiving Day", "date": "2024-11-23", "offices": ["office_tokyo"]}
    ]
    
    # Hong Kong holidays
    hk_holidays_2024 = [
        {"name": "New Year's Day", "date": "2024-01-01", "offices": ["office_hk"]},
        {"name": "Lunar New Year's Day", "date": "2024-02-10", "offices": ["office_hk"]},
        {"name": "Second Day of Lunar New Year", "date": "2024-02-12", "offices": ["office_hk"]},
        {"name": "Third Day of Lunar New Year", "date": "2024-02-13", "offices": ["office_hk"]},
        {"name": "Ching Ming Festival", "date": "2024-04-04", "offices": ["office_hk"]},
        {"name": "Good Friday", "date": "2024-03-29", "offices": ["office_hk"]},
        {"name": "Easter Monday", "date": "2024-04-01", "offices": ["office_hk"]},
        {"name": "Labour Day", "date": "2024-05-01", "offices": ["office_hk"]},
        {"name": "Buddha's Birthday", "date": "2024-05-15", "offices": ["office_hk"]},
        {"name": "Dragon Boat Festival", "date": "2024-06-10", "offices": ["office_hk"]},
        {"name": "Hong Kong SAR Establishment Day", "date": "2024-07-01", "offices": ["office_hk"]},
        {"name": "Mid-Autumn Festival", "date": "2024-09-18", "offices": ["office_hk"]},
        {"name": "National Day", "date": "2024-10-01", "offices": ["office_hk"]},
        {"name": "Chung Yeung Festival", "date": "2024-10-11", "offices": ["office_hk"]},
        {"name": "Christmas Day", "date": "2024-12-25", "offices": ["office_hk"]},
        {"name": "Boxing Day", "date": "2024-12-26", "offices": ["office_hk"]}
    ]
    
    # Australian holidays
    au_holidays_2024 = [
        {"name": "New Year's Day", "date": "2024-01-01", "offices": ["office_sydney"]},
        {"name": "Australia Day", "date": "2024-01-26", "offices": ["office_sydney"]},
        {"name": "Good Friday", "date": "2024-03-29", "offices": ["office_sydney"]},
        {"name": "Easter Saturday", "date": "2024-03-30", "offices": ["office_sydney"]},
        {"name": "Easter Monday", "date": "2024-04-01", "offices": ["office_sydney"]},
        {"name": "Anzac Day", "date": "2024-04-25", "offices": ["office_sydney"]},
        {"name": "Queen's Birthday", "date": "2024-06-10", "offices": ["office_sydney"]},
        {"name": "Bank Holiday", "date": "2024-08-05", "offices": ["office_sydney"]},
        {"name": "Labour Day", "date": "2024-10-07", "offices": ["office_sydney"]},
        {"name": "Christmas Day", "date": "2024-12-25", "offices": ["office_sydney"]},
        {"name": "Boxing Day", "date": "2024-12-26", "offices": ["office_sydney"]}
    ]
    
    # Company-wide holidays
    company_holidays_2024 = [
        {"name": "Company Summer Break", "date": "2024-07-01", "offices": ["office_sf", "office_ny", "office_london", "office_frankfurt", "office_paris", "office_tokyo", "office_hk", "office_sydney"]},
        {"name": "Company Winter Break", "date": "2024-12-24", "offices": ["office_sf", "office_ny", "office_london", "office_frankfurt", "office_paris", "office_tokyo", "office_hk", "office_sydney"]},
        {"name": "Company Winter Break", "date": "2024-12-31", "offices": ["office_sf", "office_ny", "office_london", "office_frankfurt", "office_paris", "office_tokyo", "office_hk", "office_sydney"]}
    ]
    
    # Combine all holidays
    all_holidays = (us_holidays_2024 + uk_holidays_2024 + de_holidays_2024 + 
                   fr_holidays_2024 + jp_holidays_2024 + hk_holidays_2024 + 
                   au_holidays_2024 + company_holidays_2024)
    
    # Generate holiday entities
    for i, holiday_data in enumerate(all_holidays):
        holiday = {
            "id": f"holiday_{i+1}",
            "name": holiday_data["name"],
            "date": holiday_data["date"],
            "type": "company" if "Company" in holiday_data["name"] else "public",
            "recurring": True,
            "offices": holiday_data["offices"],
            "impact": "closure",
            "coverage_required": False if "Company" in holiday_data["name"] else True
        }
        holidays.append(holiday)
    
    return holidays

def generate_compliance_data():
    """Generate compliance framework data for global operations"""
    compliance_frameworks = [
        # Data Privacy
        {
            "id": "comp_gdpr",
            "framework": "GDPR",
            "version": "2018",
            "jurisdiction": "European Union",
            "geographic_scope": ["EU", "EEA", "UK"],
            "type": "data_privacy",
            "requirements": {
                "data_subject_rights": ["access", "rectification", "erasure", "portability"],
                "lawful_basis": ["consent", "contract", "legal_obligation", "vital_interests", "public_task", "legitimate_interests"],
                "breach_notification": "72 hours",
                "dpo_required": True,
                "privacy_by_design": True,
                "impact_assessments": True
            },
            "penalties": {
                "max_fine_percentage": 4,
                "max_fine_amount": "20M EUR",
                "enforcement_body": "Data Protection Authorities"
            },
            "effective_date": "2018-05-25",
            "last_updated": "2023-06-01",
            "status": "active"
        },
        {
            "id": "comp_ccpa",
            "framework": "CCPA",
            "version": "2020",
            "jurisdiction": "California, USA",
            "geographic_scope": ["US-CA"],
            "type": "data_privacy",
            "requirements": {
                "consumer_rights": ["know", "delete", "opt-out", "non-discrimination"],
                "revenue_threshold": 25000000,
                "consumer_threshold": 50000,
                "data_categories": ["personal", "commercial", "biometric", "internet_activity", "geolocation"],
                "breach_notification": "without unreasonable delay",
                "privacy_policy_required": True
            },
            "penalties": {
                "per_violation": 2500,
                "per_intentional_violation": 7500,
                "enforcement_body": "California Attorney General"
            },
            "effective_date": "2020-01-01",
            "last_updated": "2023-01-01",
            "status": "active"
        },
        # Security Standards
        {
            "id": "comp_soc2",
            "framework": "SOC2",
            "version": "Type II",
            "jurisdiction": "United States",
            "geographic_scope": ["US", "Global"],
            "type": "security",
            "requirements": {
                "trust_principles": ["security", "availability", "processing_integrity", "confidentiality", "privacy"],
                "audit_frequency": "annual",
                "continuous_monitoring": True,
                "vendor_management": True,
                "incident_response": True,
                "access_controls": True
            },
            "penalties": {
                "certification_loss": True,
                "client_contract_breach": True,
                "reputational_damage": "high"
            },
            "effective_date": "2017-05-01",
            "last_updated": "2023-04-15",
            "status": "active"
        },
        # Industry Specific
        {
            "id": "comp_hipaa",
            "framework": "HIPAA",
            "version": "2013 Omnibus",
            "jurisdiction": "United States",
            "geographic_scope": ["US"],
            "type": "data_privacy",
            "requirements": {
                "safeguards": ["administrative", "physical", "technical"],
                "phi_handling": True,
                "business_associate_agreements": True,
                "breach_notification": "60 days",
                "risk_assessments": "annual",
                "employee_training": True
            },
            "penalties": {
                "tier1_min": 100,
                "tier1_max": 50000,
                "tier4_min": 1500000,
                "tier4_max": 1500000,
                "enforcement_body": "OCR/HHS"
            },
            "effective_date": "2013-09-23",
            "last_updated": "2022-10-20",
            "status": "active"
        },
        {
            "id": "comp_pci_dss",
            "framework": "PCI-DSS",
            "version": "4.0",
            "jurisdiction": "Global",
            "geographic_scope": ["Global"],
            "type": "financial",
            "requirements": {
                "network_security": True,
                "cardholder_data_protection": True,
                "vulnerability_management": True,
                "access_control": True,
                "monitoring_testing": True,
                "security_policy": True,
                "customized_approach": True
            },
            "penalties": {
                "monthly_fines": "5000-100000",
                "card_brand_fines": True,
                "processing_suspension": True
            },
            "effective_date": "2022-03-31",
            "last_updated": "2024-01-01",
            "status": "active"
        },
        # Regional Regulations
        {
            "id": "comp_lgpd",
            "framework": "LGPD",
            "version": "2020",
            "jurisdiction": "Brazil",
            "geographic_scope": ["BR"],
            "type": "data_privacy",
            "requirements": {
                "legal_basis": ["consent", "legal_obligation", "public_policy", "research", "contract", "legitimate_interest"],
                "data_subject_rights": ["access", "correction", "deletion", "portability", "information"],
                "dpo_required": True,
                "impact_assessment": True
            },
            "penalties": {
                "max_fine_percentage": 2,
                "max_fine_amount": "50M BRL",
                "enforcement_body": "ANPD"
            },
            "effective_date": "2020-09-18",
            "last_updated": "2023-07-01",
            "status": "active"
        },
        {
            "id": "comp_pipeda",
            "framework": "PIPEDA",
            "version": "2019",
            "jurisdiction": "Canada",
            "geographic_scope": ["CA"],
            "type": "data_privacy",
            "requirements": {
                "privacy_principles": ["accountability", "consent", "limiting_collection", "limiting_use", "accuracy", "safeguards", "openness", "access", "challenging_compliance"],
                "breach_notification": "without unreasonable delay",
                "privacy_policy": True
            },
            "penalties": {
                "max_fine": 100000,
                "currency": "CAD",
                "enforcement_body": "Privacy Commissioner"
            },
            "effective_date": "2019-11-01",
            "last_updated": "2023-03-15",
            "status": "active"
        },
        {
            "id": "comp_appi",
            "framework": "APPI",
            "version": "2022",
            "jurisdiction": "Japan",
            "geographic_scope": ["JP"],
            "type": "data_privacy",
            "requirements": {
                "purpose_limitation": True,
                "data_minimization": True,
                "consent_requirements": "opt-in",
                "cross_border_transfer": "adequacy or consent",
                "security_measures": True,
                "breach_notification": True
            },
            "penalties": {
                "corporate_fine": 100000000,
                "individual_fine": 1000000,
                "currency": "JPY",
                "enforcement_body": "PPC"
            },
            "effective_date": "2022-04-01",
            "last_updated": "2023-06-01",
            "status": "active"
        }
    ]
    
    return compliance_frameworks

def generate_data_residency_data():
    """Generate data residency zone information"""
    data_residency_zones = [
        {
            "id": "dr_us",
            "zone": "US",
            "countries": ["United States", "Canada", "Mexico"],
            "regulations": ["CCPA", "PIPEDA", "COPPA", "FERPA"],
            "storage_locations": ["us-east-1", "us-west-2", "us-central1", "ca-central-1"],
            "transfer_restrictions": {
                "to_eu": "standard_contractual_clauses",
                "to_apac": "consent_required",
                "to_other": "case_by_case"
            },
            "encryption_required": True
        },
        {
            "id": "dr_eu",
            "zone": "EU",
            "countries": ["Germany", "France", "Netherlands", "Belgium", "Italy", "Spain", "Poland", "Ireland", "Sweden", "Denmark"],
            "regulations": ["GDPR", "ePrivacy", "NIS2", "DMA", "DSA"],
            "storage_locations": ["eu-west-1", "eu-central-1", "eu-north-1", "europe-west1", "europe-west4"],
            "transfer_restrictions": {
                "to_us": "adequacy_decision_or_scc",
                "to_apac": "adequacy_or_appropriate_safeguards",
                "to_other": "gdpr_compliant_only"
            },
            "encryption_required": True
        },
        {
            "id": "dr_uk",
            "zone": "UK",
            "countries": ["United Kingdom"],
            "regulations": ["UK-GDPR", "DPA-2018"],
            "storage_locations": ["eu-west-2", "europe-west2"],
            "transfer_restrictions": {
                "to_eu": "adequacy_decision",
                "to_us": "appropriate_safeguards",
                "to_apac": "case_by_case"
            },
            "encryption_required": True
        },
        {
            "id": "dr_apac",
            "zone": "APAC",
            "countries": ["Japan", "Singapore", "Australia", "New Zealand", "Hong Kong", "South Korea"],
            "regulations": ["APPI", "PDPA", "Privacy Act", "PIPA"],
            "storage_locations": ["ap-northeast-1", "ap-southeast-1", "ap-southeast-2", "asia-northeast1", "asia-southeast1"],
            "transfer_restrictions": {
                "to_us": "consent_or_contract",
                "to_eu": "appropriate_safeguards",
                "within_apac": "country_specific"
            },
            "encryption_required": True
        },
        {
            "id": "dr_china",
            "zone": "China",
            "countries": ["China"],
            "regulations": ["PIPL", "CSL", "DSL"],
            "storage_locations": ["cn-north-1", "cn-northwest-1"],
            "transfer_restrictions": {
                "to_any": "security_assessment_required",
                "data_export": "government_approval",
                "critical_data": "localization_required"
            },
            "encryption_required": True
        },
        {
            "id": "dr_india",
            "zone": "India",
            "countries": ["India"],
            "regulations": ["DPDP", "IT Act"],
            "storage_locations": ["ap-south-1", "asia-south1"],
            "transfer_restrictions": {
                "to_us": "contract_required",
                "to_eu": "consent_required",
                "sensitive_data": "localization_required"
            },
            "encryption_required": True
        },
        {
            "id": "dr_latam",
            "zone": "LATAM",
            "countries": ["Brazil", "Argentina", "Chile", "Colombia"],
            "regulations": ["LGPD", "LPDP"],
            "storage_locations": ["sa-east-1", "southamerica-east1"],
            "transfer_restrictions": {
                "to_us": "standard_clauses",
                "to_eu": "adequacy_or_clauses",
                "within_latam": "minimal_restrictions"
            },
            "encryption_required": True
        }
    ]
    
    return data_residency_zones

def generate_schedules_data():
    """Generate 24/7 on-call schedule data for global operations"""
    schedules = []
    schedule_id = 1
    
    # Define schedule types and patterns
    schedule_types = [
        {"type": "on_call", "coverage_type": "primary", "recurring_pattern": "weekly"},
        {"type": "on_call", "coverage_type": "backup", "recurring_pattern": "weekly"},
        {"type": "on_call", "coverage_type": "escalation", "recurring_pattern": "weekly"},
        {"type": "maintenance", "coverage_type": "primary", "recurring_pattern": "weekly"},
        {"type": "coverage", "coverage_type": "primary", "recurring_pattern": "daily"}
    ]
    
    # Get offices for timezone-based scheduling
    offices = generate_offices_data()
    
    # Generate schedules for each office and type
    base_date = datetime(2024, 1, 1)
    
    for office in offices:
        for schedule_type in schedule_types:
            # Create 12 weeks of schedules for each type (3 months)
            for week in range(12):
                start_date = base_date + timedelta(weeks=week)
                
                # On-call schedules are weekly rotations
                if schedule_type["recurring_pattern"] == "weekly":
                    end_date = start_date + timedelta(days=7)
                else:  # Daily coverage schedules
                    # Create daily schedules for the week
                    for day in range(7):
                        day_start = start_date + timedelta(days=day)
                        schedules.append({
                            "id": f"schedule_{schedule_id}",
                            "type": schedule_type["type"],
                            "timezone": office["timezone"],
                            "start_datetime": day_start.isoformat(),
                            "end_datetime": (day_start + timedelta(days=1)).isoformat(),
                            "recurring_pattern": schedule_type["recurring_pattern"],
                            "coverage_type": schedule_type["coverage_type"],
                            "office_id": office["id"],
                            "region": office["region"]
                        })
                        schedule_id += 1
                    continue
                
                schedules.append({
                    "id": f"schedule_{schedule_id}",
                    "type": schedule_type["type"],
                    "timezone": office["timezone"],
                    "start_datetime": start_date.isoformat(),
                    "end_datetime": end_date.isoformat(),
                    "recurring_pattern": schedule_type["recurring_pattern"],
                    "coverage_type": schedule_type["coverage_type"],
                    "office_id": office["id"],
                    "region": office["region"]
                })
                schedule_id += 1
    
    # Add special schedules for P0 incident coverage (24/7)
    for region in ["AMERICAS", "EMEA", "APAC"]:
        # Create P0 escalation schedules with 4-hour shifts for follow-the-sun coverage
        for week in range(12):
            week_start = base_date + timedelta(weeks=week)
            for day in range(7):
                day_start = week_start + timedelta(days=day)
                # 6 shifts per day (4 hours each)
                for shift in range(6):
                    shift_start = day_start + timedelta(hours=shift*4)
                    schedules.append({
                        "id": f"schedule_{schedule_id}",
                        "type": "on_call",
                        "timezone": "UTC",  # P0 schedules in UTC for global coordination
                        "start_datetime": shift_start.isoformat(),
                        "end_datetime": (shift_start + timedelta(hours=4)).isoformat(),
                        "recurring_pattern": "daily",
                        "coverage_type": "p0_escalation",
                        "office_id": None,  # Cross-office coverage
                        "region": region,
                        "severity_focus": "P0"
                    })
                    schedule_id += 1
    
    return schedules

def generate_incidents_data():
    """Generate historical incident data with P0-P3 severities"""
    incidents = []
    incident_id = 1
    
    # Incident templates by severity
    incident_types = {
        "P0": [
            {"desc": "Complete platform outage", "services": ["api", "database", "web"], "mttr_range": (30, 120)},
            {"desc": "Data pipeline failure affecting all customers", "services": ["data_pipeline", "etl"], "mttr_range": (45, 180)},
            {"desc": "Authentication service down", "services": ["auth", "sso"], "mttr_range": (15, 90)},
            {"desc": "Critical data corruption detected", "services": ["database", "storage"], "mttr_range": (60, 240)},
            {"desc": "Security breach detected", "services": ["security", "monitoring"], "mttr_range": (30, 360)}
        ],
        "P1": [
            {"desc": "API degradation affecting 30% of requests", "services": ["api"], "mttr_range": (20, 90)},
            {"desc": "Significant query performance degradation", "services": ["database", "analytics"], "mttr_range": (30, 120)},
            {"desc": "Partial data pipeline failure", "services": ["data_pipeline"], "mttr_range": (25, 100)},
            {"desc": "Customer dashboard loading issues", "services": ["web", "frontend"], "mttr_range": (15, 60)},
            {"desc": "Real-time analytics delay >5 minutes", "services": ["streaming", "analytics"], "mttr_range": (20, 80)}
        ],
        "P2": [
            {"desc": "Non-critical feature unavailable", "services": ["web"], "mttr_range": (60, 480)},
            {"desc": "Scheduled job failures", "services": ["scheduler", "jobs"], "mttr_range": (45, 240)},
            {"desc": "Reporting dashboard slow response", "services": ["reporting", "analytics"], "mttr_range": (30, 180)},
            {"desc": "Email notifications delayed", "services": ["notifications", "email"], "mttr_range": (60, 360)},
            {"desc": "Documentation site intermittent errors", "services": ["docs", "web"], "mttr_range": (120, 720)}
        ],
        "P3": [
            {"desc": "UI cosmetic issues", "services": ["frontend"], "mttr_range": (240, 2880)},
            {"desc": "Non-critical monitoring alerts", "services": ["monitoring"], "mttr_range": (180, 1440)},
            {"desc": "Legacy API deprecation warnings", "services": ["api"], "mttr_range": (360, 2880)},
            {"desc": "Minor documentation errors", "services": ["docs"], "mttr_range": (480, 4320)},
            {"desc": "Low-priority feature requests", "services": ["product"], "mttr_range": (720, 10080)}
        ]
    }
    
    # Regional distribution for incidents
    regions = [
        {"region": "AMERICAS", "offices": ["office_sf", "office_ny"], "weight": 0.4},
        {"region": "EMEA", "offices": ["office_london", "office_frankfurt"], "weight": 0.35},
        {"region": "APAC", "offices": ["office_singapore", "office_tokyo", "office_sydney", "office_bangalore"], "weight": 0.25}
    ]
    
    # Generate incidents over the past 90 days
    base_date = datetime.now() - timedelta(days=90)
    
    # Severity distribution: P0: 5%, P1: 15%, P2: 35%, P3: 45%
    severity_distribution = [
        ("P0", 5, 0.05),
        ("P1", 15, 0.15),
        ("P2", 35, 0.35),
        ("P3", 45, 0.45)
    ]
    
    # Generate ~100 incidents over 90 days
    for _ in range(100):
        # Select severity based on distribution
        severity = random.choices(
            [s[0] for s in severity_distribution],
            weights=[s[2] for s in severity_distribution]
        )[0]
        
        # Select incident type
        incident_template = random.choice(incident_types[severity])
        
        # Select affected regions (P0 often affects multiple regions)
        if severity == "P0" and random.random() < 0.6:
            # 60% chance P0 affects multiple regions
            num_regions = random.randint(2, 3)
            affected_regions = random.sample([r["region"] for r in regions], num_regions)
        else:
            # Other severities usually affect single region
            region = random.choices(regions, weights=[r["weight"] for r in regions])[0]
            affected_regions = [region["region"]]
        
        # Generate random timestamp within the past 90 days
        days_ago = random.uniform(0, 90)
        hours_offset = random.uniform(0, 24)
        created_at = base_date + timedelta(days=days_ago, hours=hours_offset)
        
        # Calculate MTTR based on severity
        mttr_minutes = random.randint(*incident_template["mttr_range"])
        resolved_at = created_at + timedelta(minutes=mttr_minutes)
        
        # Add some unresolved recent incidents
        if days_ago < 2 and severity in ["P2", "P3"] and random.random() < 0.2:
            resolved_at = None
            status = "open"
            mttr_minutes = None
        else:
            status = "resolved"
        
        incidents.append({
            "id": f"incident_{incident_id}",
            "severity": severity,
            "status": status,
            "description": incident_template["desc"],
            "affected_regions": affected_regions,
            "affected_services": incident_template["services"],
            "created_at": created_at.isoformat(),
            "resolved_at": resolved_at.isoformat() if resolved_at else None,
            "mttr_minutes": mttr_minutes,
            "root_cause": random.choice([
                "Configuration change",
                "Infrastructure failure", 
                "Code deployment",
                "Third-party service outage",
                "Capacity exceeded",
                "Network issues",
                "Human error",
                "Unknown"
            ]) if status == "resolved" else None
        })
        incident_id += 1
    
    # Sort incidents by created_at for realistic ordering
    incidents.sort(key=lambda x: x["created_at"])
    
    return incidents

def generate_visas_data():
    """Generate visa and work authorization data for global workforce"""
    visas = []
    visa_id = 1
    
    # Common visa types by country
    visa_types = {
        "United States": [
            {"type": "H-1B", "name": "Specialty Occupation Work Visa", "max_duration_years": 6},
            {"type": "L-1A", "name": "Intracompany Transferee Executive", "max_duration_years": 7},
            {"type": "L-1B", "name": "Intracompany Transferee Specialized Knowledge", "max_duration_years": 5},
            {"type": "O-1", "name": "Extraordinary Ability Work Visa", "max_duration_years": 3},
            {"type": "TN", "name": "NAFTA Professional Work Visa", "max_duration_years": 3},
            {"type": "Green Card", "name": "Permanent Resident Card", "max_duration_years": 10}
        ],
        "United Kingdom": [
            {"type": "Skilled Worker", "name": "Skilled Worker Visa", "max_duration_years": 5},
            {"type": "ICT", "name": "Intra-company Transfer Visa", "max_duration_years": 5},
            {"type": "Global Talent", "name": "Global Talent Visa", "max_duration_years": 5},
            {"type": "ILR", "name": "Indefinite Leave to Remain", "max_duration_years": 0}  # Permanent
        ],
        "Germany": [
            {"type": "EU Blue Card", "name": "EU Blue Card", "max_duration_years": 4},
            {"type": "ICT Card", "name": "Intra-Corporate Transfer Card", "max_duration_years": 3},
            {"type": "Employment Visa", "name": "Employment Visa", "max_duration_years": 3},
            {"type": "Permanent Residence", "name": "Niederlassungserlaubnis", "max_duration_years": 0}
        ],
        "France": [
            {"type": "Passeport Talent", "name": "Talent Passport", "max_duration_years": 4},
            {"type": "ICT Permit", "name": "Intra-Company Transfer Permit", "max_duration_years": 3},
            {"type": "EU Blue Card", "name": "EU Blue Card France", "max_duration_years": 4}
        ],
        "Japan": [
            {"type": "Engineer/Specialist", "name": "Engineer/Specialist in Humanities", "max_duration_years": 5},
            {"type": "Highly Skilled Professional", "name": "Highly Skilled Professional Visa", "max_duration_years": 5},
            {"type": "Intra-company Transferee", "name": "Intra-company Transferee", "max_duration_years": 5},
            {"type": "Permanent Resident", "name": "Permanent Resident", "max_duration_years": 0}
        ],
        "Australia": [
            {"type": "TSS 482", "name": "Temporary Skill Shortage Visa", "max_duration_years": 4},
            {"type": "186 ENS", "name": "Employer Nomination Scheme", "max_duration_years": 0},  # Permanent
            {"type": "189", "name": "Skilled Independent Visa", "max_duration_years": 0},
            {"type": "494", "name": "Skilled Employer Sponsored Regional", "max_duration_years": 5}
        ],
        "Hong Kong": [
            {"type": "Employment Visa", "name": "General Employment Policy", "max_duration_years": 3},
            {"type": "QMAS", "name": "Quality Migrant Admission Scheme", "max_duration_years": 8},
            {"type": "Right of Abode", "name": "Right of Abode", "max_duration_years": 0}
        ]
    }
    
    # Generate visas for different scenarios
    now = datetime.now()
    
    # US H-1B visas (common for tech workers)
    for i in range(50):
        issued_date = now - timedelta(days=random.randint(30, 1095))  # 1 month to 3 years ago
        visa_type_info = random.choice(visa_types["United States"][:3])  # Work visas only
        
        visas.append({
            "id": f"visa_{visa_id}",
            "type": visa_type_info["type"],
            "name": visa_type_info["name"],
            "country": "United States",
            "issued_date": issued_date.strftime("%Y-%m-%d"),
            "expiry_date": (issued_date + timedelta(days=365 * 3)).strftime("%Y-%m-%d"),  # 3 year validity
            "restrictions": ["Single employer", "Requires sponsorship"],
            "allows_client_site": True,
            "max_duration_years": visa_type_info["max_duration_years"],
            "renewable": True
        })
        visa_id += 1
    
    # UK Skilled Worker visas
    for i in range(30):
        issued_date = now - timedelta(days=random.randint(30, 730))
        visa_type_info = visa_types["United Kingdom"][0]
        
        visas.append({
            "id": f"visa_{visa_id}",
            "type": visa_type_info["type"],
            "name": visa_type_info["name"],
            "country": "United Kingdom",
            "issued_date": issued_date.strftime("%Y-%m-%d"),
            "expiry_date": (issued_date + timedelta(days=365 * 5)).strftime("%Y-%m-%d"),
            "restrictions": ["Tied to sponsor", "Minimum salary requirement"],
            "allows_client_site": True,
            "max_duration_years": visa_type_info["max_duration_years"],
            "renewable": True
        })
        visa_id += 1
    
    # EU Blue Cards (Germany, France)
    for country in ["Germany", "France"]:
        for i in range(20):
            issued_date = now - timedelta(days=random.randint(30, 730))
            visa_type_info = next(v for v in visa_types[country] if "Blue Card" in v["name"])
            
            visas.append({
                "id": f"visa_{visa_id}",
                "type": visa_type_info["type"],
                "name": visa_type_info["name"],
                "country": country,
                "issued_date": issued_date.strftime("%Y-%m-%d"),
                "expiry_date": (issued_date + timedelta(days=365 * 4)).strftime("%Y-%m-%d"),
                "restrictions": ["Highly qualified employment", "Minimum salary threshold"],
                "allows_client_site": True,
                "max_duration_years": visa_type_info["max_duration_years"],
                "renewable": True
            })
            visa_id += 1
    
    # APAC visas (Japan, Australia, Hong Kong)
    for country in ["Japan", "Australia", "Hong Kong"]:
        for i in range(15):
            issued_date = now - timedelta(days=random.randint(30, 730))
            visa_type_info = random.choice(visa_types[country][:2])
            
            duration_years = 3 if visa_type_info["max_duration_years"] > 0 else 10
            restrictions = []
            if country == "Japan":
                restrictions = ["Company sponsorship required", "Residence card required"]
            elif country == "Australia":
                restrictions = ["Employer nomination required", "Skills assessment required"]
            else:
                restrictions = ["Local sponsor required"]
            
            visas.append({
                "id": f"visa_{visa_id}",
                "type": visa_type_info["type"],
                "name": visa_type_info["name"],
                "country": country,
                "issued_date": issued_date.strftime("%Y-%m-%d"),
                "expiry_date": (issued_date + timedelta(days=365 * duration_years)).strftime("%Y-%m-%d"),
                "restrictions": restrictions,
                "allows_client_site": True,
                "max_duration_years": visa_type_info["max_duration_years"],
                "renewable": True
            })
            visa_id += 1
    
    # Some business visit visas
    business_visa_countries = ["United States", "China", "India", "Brazil", "Russia"]
    for country in business_visa_countries:
        for i in range(10):
            issued_date = now - timedelta(days=random.randint(30, 365))
            
            visas.append({
                "id": f"visa_{visa_id}",
                "type": "Business",
                "name": "Business Visitor Visa",
                "country": country,
                "issued_date": issued_date.strftime("%Y-%m-%d"),
                "expiry_date": (issued_date + timedelta(days=365 * 5)).strftime("%Y-%m-%d"),  # 5 year validity
                "restrictions": ["No employment allowed", "Max 90 days per visit"],
                "allows_client_site": True,
                "max_duration_years": 0,  # Visit only
                "renewable": False
            })
            visa_id += 1
    
    # Some permanent residencies
    pr_countries = ["United States", "United Kingdom", "Germany", "Australia", "Japan"]
    for country in pr_countries:
        for i in range(5):
            issued_date = now - timedelta(days=random.randint(365, 1825))  # 1-5 years ago
            
            # Find the permanent visa type for this country
            pr_type = next((v for v in visa_types.get(country, []) if v["max_duration_years"] == 0), None)
            if pr_type:
                visas.append({
                    "id": f"visa_{visa_id}",
                    "type": pr_type["type"],
                    "name": pr_type["name"],
                    "country": country,
                    "issued_date": issued_date.strftime("%Y-%m-%d"),
                    "expiry_date": (issued_date + timedelta(days=365 * 10)).strftime("%Y-%m-%d"),  # 10 year card
                    "restrictions": [],
                    "allows_client_site": True,
                    "max_duration_years": 0,
                    "renewable": True
                })
                visa_id += 1
    
    return visas

def generate_metrics_data():
    """Generate performance metrics data for services across regions"""
    metrics = []
    metric_id = 1
    
    # Services we track
    services = [
        "api-gateway",
        "data-pipeline",
        "analytics-engine", 
        "ml-inference",
        "query-service",
        "streaming-processor",
        "batch-scheduler",
        "metadata-service",
        "auth-service",
        "notification-service"
    ]
    
    # Regions (aligned with offices)
    regions = ["AMERICAS", "EMEA", "APAC"]
    
    # Metric types and their typical values
    metric_configs = [
        {
            "type": "availability",
            "unit": "percentage",
            "percentiles": [99],  # We track availability as a single value
            "base_value": 99.5,
            "variance": 0.5
        },
        {
            "type": "response_time",
            "unit": "milliseconds", 
            "percentiles": [50, 95, 99],
            "base_values": {"50": 50, "95": 200, "99": 500},
            "variance": 0.3
        },
        {
            "type": "throughput",
            "unit": "requests_per_second",
            "percentiles": [50],  # Average throughput
            "base_value": 1000,
            "variance": 0.4
        },
        {
            "type": "error_rate",
            "unit": "percentage",
            "percentiles": [50],
            "base_value": 0.1,
            "variance": 0.5
        },
        {
            "type": "cpu_utilization",
            "unit": "percentage",
            "percentiles": [50, 95],
            "base_values": {"50": 40, "95": 70},
            "variance": 0.3
        },
        {
            "type": "memory_utilization",
            "unit": "percentage",
            "percentiles": [50, 95],
            "base_values": {"50": 50, "95": 80},
            "variance": 0.2
        }
    ]
    
    # Generate metrics for the last 30 days
    now = datetime.now()
    
    for days_ago in range(30):
        timestamp = now - timedelta(days=days_ago)
        
        # Generate metrics for each service, region, and metric type
        for service in services:
            for region in regions:
                for config in metric_configs:
                    # Add some variance based on region and service
                    region_multiplier = {"AMERICAS": 1.0, "EMEA": 1.1, "APAC": 0.9}[region]
                    service_multiplier = 1.0
                    if "ml" in service or "analytics" in service:
                        service_multiplier = 1.2  # ML services are slower
                    elif "auth" in service or "gateway" in service:
                        service_multiplier = 0.8  # Auth/gateway are faster
                    
                    if config["type"] in ["availability", "throughput", "error_rate"]:
                        # Single percentile metrics
                        base = config["base_value"]
                        # Add daily variance
                        daily_variance = random.uniform(-config["variance"], config["variance"])
                        # Add hourly spikes for some hours
                        hour = timestamp.hour
                        hourly_spike = 0
                        if hour in [9, 10, 14, 15]:  # Business hours spikes
                            if config["type"] == "throughput":
                                hourly_spike = 0.5
                            elif config["type"] == "error_rate":
                                hourly_spike = 0.2
                        
                        value = base * region_multiplier * service_multiplier * (1 + daily_variance + hourly_spike)
                        
                        # Ensure reasonable bounds
                        if config["type"] == "availability":
                            value = min(100, max(95, value))
                        elif config["type"] == "error_rate":
                            value = max(0, min(5, value))
                        
                        metrics.append({
                            "id": f"metric_{metric_id}",
                            "type": config["type"],
                            "service": service,
                            "region": region,
                            "value": round(value, 2),
                            "unit": config["unit"],
                            "timestamp": timestamp.isoformat(),
                            "percentile": config["percentiles"][0]
                        })
                        metric_id += 1
                    
                    else:
                        # Multiple percentile metrics (response_time, cpu, memory)
                        for percentile in config["percentiles"]:
                            base = config["base_values"][str(percentile)]
                            daily_variance = random.uniform(-config["variance"], config["variance"])
                            
                            value = base * region_multiplier * service_multiplier * (1 + daily_variance)
                            
                            # Add some anomalies
                            if random.random() < 0.02:  # 2% chance of anomaly
                                value *= random.uniform(2, 5)
                            
                            metrics.append({
                                "id": f"metric_{metric_id}",
                                "type": config["type"],
                                "service": service,
                                "region": region,
                                "value": round(value, 2),
                                "unit": config["unit"],
                                "timestamp": timestamp.isoformat(),
                                "percentile": percentile
                            })
                            metric_id += 1
    
    # Add some SLA metrics (monthly aggregates)
    sla_metrics = []
    for service in services:
        for region in regions:
            # Monthly SLA achievement
            sla_achieved = random.uniform(99.0, 99.99)
            metrics.append({
                "id": f"metric_{metric_id}",
                "type": "sla_achievement",
                "service": service,
                "region": region,
                "value": round(sla_achieved, 2),
                "unit": "percentage",
                "timestamp": now.replace(day=1).isoformat(),  # First of month
                "percentile": 0  # Not applicable for SLA
            })
            metric_id += 1
    
    return metrics

def generate_people_data():
    """Generate realistic people data for a B2B data analytics platform company"""
    people = []
    departments = [
        "Data Platform Engineering", "Analytics Engineering", "Product", "Data Science", 
        "Infrastructure & DevOps", "Security & Compliance", "Customer Success", 
        "Professional Services", "Sales", "Marketing", "Finance", "Legal", 
        "People Operations", "Engineering", "Solutions Architecture"
    ]
    
    seniority_levels = ["Junior", "Mid", "Senior", "Staff", "Principal"]
    timezones = ["US/Pacific", "US/Mountain", "US/Central", "US/Eastern", "Europe/London", "Europe/Berlin", "Asia/Singapore", "Australia/Sydney"]
    
    roles = {
        "Data Platform Engineering": [
            "Data Platform Engineer", "Senior Data Platform Engineer", "Staff Data Platform Engineer",
            "Principal Data Platform Engineer", "Data Infrastructure Engineer", "Senior Data Infrastructure Engineer",
            "Streaming Data Engineer", "Data Pipeline Engineer", "Platform Engineering Manager",
            "Director of Data Platform", "VP of Data Engineering", "Data Platform Architect"
        ],
        "Analytics Engineering": [
            "Analytics Engineer", "Senior Analytics Engineer", "Lead Analytics Engineer",
            "Analytics Engineering Manager", "BI Developer", "Senior BI Developer",
            "Data Modeling Engineer", "Metrics Engineer", "Analytics Platform Engineer"
        ],
        "Engineering": [
            "Backend Engineer", "Senior Backend Engineer", "Staff Backend Engineer", 
            "Frontend Engineer", "Senior Frontend Engineer", "Full Stack Engineer",
            "API Engineer", "Senior API Engineer", "Engineering Manager", "Director of Engineering"
        ],
        "Product": [
            "Product Manager - Analytics", "Senior Product Manager - Data Platform", 
            "Principal Product Manager", "Group Product Manager - Enterprise", "Product Director", 
            "VP of Product", "Technical Product Manager - APIs", "Product Manager - Data Governance",
            "Product Manager - Visualization", "Product Manager - Data Integration"
        ],
        "Data Science": [
            "Data Scientist", "Senior Data Scientist", "Staff Data Scientist", "Principal Data Scientist",
            "ML Engineer", "Senior ML Engineer", "Applied Scientist", "Research Data Scientist",
            "Data Science Manager", "Director of Data Science", "VP of Data Science",
            "Algorithm Engineer", "ML Platform Engineer"
        ],
        "Infrastructure & DevOps": [
            "DevOps Engineer", "Senior DevOps Engineer", "Staff DevOps Engineer",
            "Site Reliability Engineer", "Senior SRE", "Infrastructure Engineer",
            "Cloud Architect", "Kubernetes Engineer", "DevOps Manager", 
            "Director of Infrastructure", "Database Administrator", "Performance Engineer"
        ],
        "Security & Compliance": [
            "Security Engineer", "Senior Security Engineer", "Staff Security Engineer",
            "Security Architect", "Compliance Manager", "Data Privacy Officer",
            "GRC Analyst", "Senior GRC Analyst", "Security Operations Engineer",
            "Director of Security", "CISO", "Compliance Engineer"
        ],
        "Customer Success": [
            "Customer Success Manager", "Senior Customer Success Manager", "Enterprise CSM",
            "Technical Account Manager", "Senior TAM", "Customer Success Engineer",
            "Implementation Specialist", "Customer Success Director", "VP of Customer Success",
            "Onboarding Specialist", "Customer Success Operations Manager"
        ],
        "Professional Services": [
            "Data Consultant", "Senior Data Consultant", "Lead Data Consultant",
            "Solutions Consultant", "Implementation Engineer", "Senior Implementation Engineer",
            "Professional Services Manager", "Engagement Manager", "Director of Professional Services",
            "Data Architect - Consulting", "Analytics Consultant"
        ],
        "Sales": [
            "Sales Development Representative", "Account Executive - Mid Market", "Enterprise Account Executive",
            "Senior Enterprise AE", "Sales Engineer", "Senior Sales Engineer", 
            "Sales Manager", "Regional Sales Director", "VP of Sales", "Chief Revenue Officer",
            "Channel Partner Manager", "Strategic Account Manager"
        ],
        "Marketing": [
            "Product Marketing Manager", "Senior Product Marketing Manager", "Content Marketing Manager",
            "Demand Generation Manager", "Marketing Operations Manager", "Developer Relations Manager",
            "Marketing Director", "VP of Marketing", "Technical Writer", "Marketing Analyst",
            "Event Marketing Manager", "Partner Marketing Manager"
        ],
        "Finance": [
            "Financial Analyst", "Senior Financial Analyst", "Revenue Analyst", 
            "FP&A Manager", "Finance Manager", "Accounting Manager", "Controller",
            "Finance Director", "VP of Finance", "CFO", "Billing Specialist",
            "Revenue Operations Analyst"
        ],
        "Legal": [
            "Legal Counsel", "Senior Legal Counsel", "Data Privacy Counsel", 
            "Commercial Counsel", "General Counsel", "Contract Manager", 
            "Compliance Counsel", "Paralegal"
        ],
        "People Operations": [
            "People Operations Specialist", "HR Business Partner", "Senior HRBP",
            "Talent Acquisition Manager", "Senior Recruiter", "Technical Recruiter",
            "People Operations Manager", "Director of People", "VP of People", 
            "Learning & Development Manager", "Total Rewards Manager"
        ],
        "Solutions Architecture": [
            "Solutions Architect", "Senior Solutions Architect", "Principal Solutions Architect",
            "Data Solutions Architect", "Enterprise Architect", "Technical Solutions Manager",
            "Integration Architect", "Solutions Engineering Manager", "Director of Solutions Architecture",
            "Pre-Sales Engineer", "Customer Solutions Engineer"
        ],
        # Note: Removed QA, Research, and BD as separate departments - these roles are integrated into other teams
    }
    
    for i in range(500):
        dept = random.choice(departments)
        # Generate a name first
        full_name = fake.name()
        # Create email from the name
        first_name = full_name.split()[0].lower()
        last_name = full_name.split()[-1].lower()
        # Remove any apostrophes or special characters from names
        first_name = first_name.replace("'", "").replace("-", "")
        last_name = last_name.replace("'", "").replace("-", "")
        email = f"{first_name}.{last_name}@company.com"
        
        role = random.choice(roles[dept])
        hire_date = fake.date_between(start_date='-3y', end_date='today')
        years_exp = random.randint(1, 15)
        
        # Determine seniority based on role
        if "Principal" in role or "VP" in role or "Director" in role:
            seniority = "Principal"
            base_rate = random.randint(200, 350)
        elif "Staff" in role or "Lead" in role or "Senior" in role:
            seniority = "Senior"
            base_rate = random.randint(150, 250)
        elif "Manager" in role:
            seniority = "Staff"
            base_rate = random.randint(175, 275)
        else:
            seniority = random.choice(["Junior", "Mid", "Senior"])
            base_rate = random.randint(100, 200)
        
        location = random.choice([
            "San Francisco", "New York", "Austin", "Remote", "Seattle", "Boston", 
            "Chicago", "Los Angeles", "Denver", "Atlanta", "Portland", "Miami",
            "Toronto", "London", "Berlin", "Singapore", "Sydney"
        ])
        
        # Map location to timezone
        timezone_map = {
            "San Francisco": "US/Pacific", "Seattle": "US/Pacific", "Los Angeles": "US/Pacific", "Portland": "US/Pacific",
            "Denver": "US/Mountain", "Austin": "US/Central", "Chicago": "US/Central",
            "New York": "US/Eastern", "Boston": "US/Eastern", "Atlanta": "US/Eastern", "Miami": "US/Eastern",
            "Toronto": "US/Eastern", "London": "Europe/London", "Berlin": "Europe/Berlin",
            "Singapore": "Asia/Singapore", "Sydney": "Australia/Sydney", "Remote": random.choice(timezones)
        }
        
        person = {
            "id": f"person_{i+1}",
            "name": full_name,
            "email": email,
            "department": dept,
            "role": role,
            "seniority": seniority,
            "hire_date": hire_date.isoformat(),
            "location": location,
            "timezone": timezone_map.get(location, "US/Pacific"),
            "capacity_hours_per_week": 40,
            "current_utilization": random.randint(60, 100),  # percentage
            "billing_rate": base_rate,
            "years_experience": years_exp,
            "manager_id": None  # Will be set later
        }
        people.append(person)
    
    # Set managers (roughly 1 manager per 6-8 people)
    managers = random.sample(people, k=20)
    for manager in managers:
        manager["role"] = manager["role"].replace("Senior ", "").replace("Staff ", "") + " Manager"
    
    # Assign managers to people
    for person in people:
        if person not in managers:
            # Find a manager in the same department if possible
            dept_managers = [m for m in managers if m["department"] == person["department"]]
            if dept_managers:
                person["manager_id"] = random.choice(dept_managers)["id"]
            else:
                person["manager_id"] = random.choice(managers)["id"]
    
    return people

def generate_teams_data():
    """Generate team data for a B2B data analytics platform"""
    teams = [
        # Data Platform Engineering Teams
        {"id": "team_1", "name": "Data Ingestion", "department": "Data Platform Engineering", "focus": "Real-time and batch data ingestion pipelines"},
        {"id": "team_2", "name": "Data Processing", "department": "Data Platform Engineering", "focus": "Distributed data processing and transformation systems"},
        {"id": "team_3", "name": "Storage & Query", "department": "Data Platform Engineering", "focus": "Data lake, warehouse, and query optimization"},
        {"id": "team_4", "name": "Streaming Platform", "department": "Data Platform Engineering", "focus": "Real-time streaming infrastructure and event processing"},
        {"id": "team_5", "name": "Data Quality", "department": "Data Platform Engineering", "focus": "Data validation, quality monitoring, and lineage tracking"},
        
        # Analytics Engineering Teams
        {"id": "team_6", "name": "Analytics Platform", "department": "Analytics Engineering", "focus": "Self-service analytics platform and tools"},
        {"id": "team_7", "name": "Data Modeling", "department": "Analytics Engineering", "focus": "Semantic layer, metrics definitions, and data models"},
        {"id": "team_8", "name": "BI Tools", "department": "Analytics Engineering", "focus": "Business intelligence tools and visualization platforms"},
        
        # Engineering Teams
        {"id": "team_9", "name": "API Platform", "department": "Engineering", "focus": "REST and GraphQL APIs for data access"},
        {"id": "team_10", "name": "Frontend Applications", "department": "Engineering", "focus": "Web applications and user interfaces"},
        {"id": "team_11", "name": "Authentication & Access", "department": "Engineering", "focus": "Identity management, SSO, and access control"},
        {"id": "team_12", "name": "Developer Experience", "department": "Engineering", "focus": "SDKs, documentation, and developer tools"},
        
        # Data Science Teams
        {"id": "team_13", "name": "ML Infrastructure", "department": "Data Science", "focus": "Machine learning platform and model serving"},
        {"id": "team_14", "name": "Advanced Analytics", "department": "Data Science", "focus": "Predictive analytics and AI-powered insights"},
        {"id": "team_15", "name": "Data Science Tools", "department": "Data Science", "focus": "Notebooks, experimentation, and ML workflows"},
        
        # Product Teams
        {"id": "team_16", "name": "Platform Product", "department": "Product", "focus": "Core data platform capabilities and roadmap"},
        {"id": "team_17", "name": "Analytics Product", "department": "Product", "focus": "Analytics features and visualization tools"},
        {"id": "team_18", "name": "Enterprise Product", "department": "Product", "focus": "Enterprise features, governance, and compliance"},
        {"id": "team_19", "name": "Integration Product", "department": "Product", "focus": "Connectors, integrations, and data sources"},
        
        # Infrastructure & DevOps Teams
        {"id": "team_20", "name": "Cloud Infrastructure", "department": "Infrastructure & DevOps", "focus": "Multi-cloud infrastructure and Kubernetes"},
        {"id": "team_21", "name": "Site Reliability", "department": "Infrastructure & DevOps", "focus": "System reliability, monitoring, and incident response"},
        {"id": "team_22", "name": "Database Operations", "department": "Infrastructure & DevOps", "focus": "Database management and optimization"},
        
        # Security & Compliance Teams
        {"id": "team_23", "name": "Data Security", "department": "Security & Compliance", "focus": "Data encryption, access control, and security"},
        {"id": "team_24", "name": "Compliance & Privacy", "department": "Security & Compliance", "focus": "GDPR, CCPA, SOC2, and regulatory compliance"},
        {"id": "team_25", "name": "Security Operations", "department": "Security & Compliance", "focus": "Security monitoring and incident response"},
        
        # Customer Success Teams
        {"id": "team_26", "name": "Enterprise Success", "department": "Customer Success", "focus": "Strategic account management and success"},
        {"id": "team_27", "name": "Technical Success", "department": "Customer Success", "focus": "Technical implementation and support"},
        {"id": "team_28", "name": "Customer Education", "department": "Customer Success", "focus": "Training, certification, and documentation"},
        
        # Professional Services Teams
        {"id": "team_29", "name": "Implementation Services", "department": "Professional Services", "focus": "Customer implementations and migrations"},
        {"id": "team_30", "name": "Data Architecture", "department": "Professional Services", "focus": "Data architecture consulting and best practices"},
        {"id": "team_31", "name": "Analytics Consulting", "department": "Professional Services", "focus": "Analytics strategy and use case development"},
        
        # Sales Teams
        {"id": "team_32", "name": "Enterprise Sales", "department": "Sales", "focus": "Fortune 500 and large enterprise accounts"},
        {"id": "team_33", "name": "Mid-Market Sales", "department": "Sales", "focus": "Mid-market and growth company accounts"},
        {"id": "team_34", "name": "Partner Sales", "department": "Sales", "focus": "Channel partners and technology alliances"},
        
        # Solutions Architecture Teams
        {"id": "team_35", "name": "Enterprise Architecture", "department": "Solutions Architecture", "focus": "Enterprise data architecture and strategy"},
        {"id": "team_36", "name": "Technical Solutions", "department": "Solutions Architecture", "focus": "Technical demonstrations and proof of concepts"},
        {"id": "team_37", "name": "Integration Architecture", "department": "Solutions Architecture", "focus": "Integration patterns and best practices"}
    ]
    
    return teams

def generate_groups_data():
    """Generate cross-functional groups for data analytics platform governance"""
    groups = [
        {
            "id": "group_1",
            "name": "Data Governance Council",
            "description": "Cross-functional data governance, privacy, quality standards, and compliance oversight",
            "type": "governance",
            "lead_department": "Security"
        },
        {
            "id": "group_2", 
            "name": "Security & Privacy Board",
            "description": "Data security, encryption standards, access control, and privacy compliance",
            "type": "governance",
            "lead_department": "Security & Compliance"
        },
        {
            "id": "group_3",
            "name": "Data Architecture Board",
            "description": "Data architecture standards, technology stack decisions, and integration patterns",
            "type": "technical",
            "lead_department": "Data Platform Engineering"
        },
        {
            "id": "group_4",
            "name": "Customer Data Council",
            "description": "Customer data handling, retention policies, and data ethics guidelines",
            "type": "governance",
            "lead_department": "Security & Compliance"
        },
        {
            "id": "group_5",
            "name": "Platform Reliability Team",
            "description": "24/7 platform monitoring, incident response, and reliability engineering",
            "type": "operational",
            "lead_department": "Infrastructure & DevOps"
        },
        {
            "id": "group_6",
            "name": "Regulatory Compliance Committee",
            "description": "SOC2, GDPR, CCPA, HIPAA, and industry-specific compliance requirements",
            "type": "compliance",
            "lead_department": "Security & Compliance"
        },
        {
            "id": "group_7",
            "name": "API Governance Board",
            "description": "API standards, versioning, rate limiting, and developer experience",
            "type": "technical",
            "lead_department": "Engineering"
        },
        {
            "id": "group_8",
            "name": "Data Quality Committee",
            "description": "Data quality standards, validation rules, and monitoring processes",
            "type": "technical",
            "lead_department": "Data Platform Engineering"
        },
        {
            "id": "group_9",
            "name": "ML/AI Ethics Committee",
            "description": "Ethical AI guidelines, bias detection, and responsible ML practices",
            "type": "governance",
            "lead_department": "Data Science"
        },
        {
            "id": "group_10",
            "name": "Enterprise Customer Advisory",
            "description": "Enterprise customer feedback, feature prioritization, and strategic partnerships",
            "type": "strategic",
            "lead_department": "Customer Success"
        },
        {
            "id": "group_11",
            "name": "SLA & Performance Committee",
            "description": "SLA definitions, performance benchmarks, and customer commitment standards",
            "type": "operational",
            "lead_department": "Infrastructure & DevOps"
        },
        {
            "id": "group_12",
            "name": "Data Connectors Alliance",
            "description": "Integration partnerships, connector development, and ecosystem expansion",
            "type": "technical",
            "lead_department": "Solutions Architecture"
        },
        {
            "id": "group_13",
            "name": "Cost Optimization Board",
            "description": "Cloud cost management, resource optimization, and pricing strategy",
            "type": "operational",
            "lead_department": "Infrastructure & DevOps"
        },
        {
            "id": "group_14",
            "name": "Partner Ecosystem Council",
            "description": "Technology partnerships, channel strategy, and ecosystem development",
            "type": "strategic",
            "lead_department": "Sales"
        },
        {
            "id": "group_15",
            "name": "Innovation Lab",
            "description": "Emerging technologies, R&D initiatives, and competitive analysis",
            "type": "strategic",
            "lead_department": "Data Science"
        }
    ]
    
    return groups

def generate_policies_data():
    """Generate comprehensive policies for B2B data analytics platform"""
    policies = [
        {
            "id": "policy_1",
            "name": "Customer Data Processing Policy",
            "description": "All customer data processing must comply with data processing agreements (DPAs). Data must be processed only for agreed purposes with explicit consent. Data minimization principles apply - collect only necessary data. Customer data segregation must be maintained with encryption at rest and in transit. Processing logs retained for audit purposes.",
            "category": "data_governance",
            "severity": "critical",
            "responsible_type": "group",
            "compliance_frameworks": ["GDPR", "CCPA", "SOC2"]
        },
        {
            "id": "policy_2", 
            "name": "Data Classification Policy",
            "description": "All data must be classified as Public, Internal, Confidential, or Restricted. Classification determines handling requirements including encryption, access controls, and retention periods. Restricted data requires additional security controls and audit logging. Automated classification tools must scan and tag data. Quarterly classification reviews required.",
            "category": "data_governance",
            "severity": "high",
            "responsible_type": "team",
            "compliance_frameworks": ["SOC2", "ISO27001", "NIST"]
        },
        {
            "id": "policy_3",
            "name": "Data Quality Standards Policy", 
            "description": "Data quality metrics must be defined and monitored for all datasets. Quality thresholds: completeness >95%, accuracy >99%, consistency >98%. Automated quality checks required for all data pipelines. Quality issues must be remediated within SLA timeframes. Data quality scorecards published monthly.",
            "category": "data_governance",
            "severity": "high",
            "responsible_type": "team",
            "compliance_frameworks": ["SOC2", "Internal"]
        },
        {
            "id": "policy_4",
            "name": "Data Lineage and Metadata Policy",
            "description": "Complete data lineage must be maintained for all datasets showing origin, transformations, and dependencies. Metadata cataloging required including schema, ownership, quality metrics, and usage. Lineage must be queryable and auditable. Updates to lineage tracking within 24 hours of pipeline changes.",
            "category": "data_governance",
            "severity": "medium", 
            "responsible_type": "team",
            "compliance_frameworks": ["SOC2", "Internal"]
        },
        {
            "id": "policy_5",
            "name": "Encryption Policy",
            "description": "All data must be encrypted at rest (AES-256) and in transit (TLS 1.2+). Encryption keys managed via HSM with annual rotation. Customer data requires envelope encryption with customer-managed keys option. Key escrow and recovery procedures required. Encryption status monitored continuously.",
            "category": "security",
            "severity": "critical",
            "responsible_type": "team",
            "compliance_frameworks": ["SOC2", "ISO27001", "FIPS"]
        },
        {
            "id": "policy_6",
            "name": "Access Control Policy",
            "description": "Role-based access control (RBAC) required for all systems. Just-in-time access for privileged operations. Access reviews quarterly for admins, semi-annually for users. Break-glass procedures for emergency access with full audit trail. Customer data access restricted to authorized personnel only.",
            "category": "security",
            "severity": "critical",
            "responsible_type": "group",
            "compliance_frameworks": ["SOC2", "ISO27001", "NIST"]
        },
        {
            "id": "policy_7",
            "name": "Audit Logging Policy",
            "description": "All data access, modifications, and administrative actions must be logged. Logs retained for 2 years minimum, 7 years for compliance data. Log integrity protection via write-once storage. Real-time anomaly detection on audit logs. Customer audit logs available via API.",
            "category": "security",
            "severity": "high",
            "responsible_type": "team",
            "compliance_frameworks": ["SOC2", "GDPR", "HIPAA"]
        },
        {
            "id": "policy_8",
            "name": "API Rate Limiting Policy",
            "description": "All APIs must implement rate limiting based on customer tier. Default limits: 1000 requests/hour for standard, 10000/hour for premium, custom for enterprise. Burst allowances up to 2x limit for 5 minutes. Clear error messages and retry headers required. Rate limit monitoring and alerting.",
            "category": "platform",
            "severity": "high",
            "responsible_type": "team",
            "compliance_frameworks": ["SOC2", "Internal"]
        },
        {
            "id": "policy_9",
            "name": "SLA and Uptime Policy",
            "description": "Platform SLA: 99.9% uptime for standard, 99.95% for premium, 99.99% for enterprise. Planned maintenance windows excluded. SLA credits issued automatically for breaches. Real-time status page required with incident history. Performance SLAs for query response times.",
            "category": "platform",
            "severity": "critical",
            "responsible_type": "group",
            "compliance_frameworks": ["SOC2", "Internal"]
        },
        {
            "id": "policy_10",
            "name": "Multi-tenancy Isolation Policy",
            "description": "Complete logical isolation between customer tenants. Resource quotas enforced per tenant. No shared compute or storage resources. Network isolation via VPC/namespace separation. Regular isolation testing required. Data leakage prevention controls mandatory.",
            "category": "platform",
            "severity": "critical",
            "responsible_type": "team",
            "compliance_frameworks": ["SOC2", "ISO27001", "FedRAMP"]
        },
        {
            "id": "policy_11",
            "name": "Data Export Policy",
            "description": "Customers must be able to export all their data within 30 days of request. Standard formats: CSV, JSON, Parquet. Bulk export via secure channels. Export includes all data, metadata, and configurations. Automated export capabilities required. Data portability compliance.",
            "category": "platform",
            "severity": "high",
            "responsible_type": "team",
            "compliance_frameworks": ["GDPR", "CCPA", "Internal"]
        },
        {
            "id": "policy_12",
            "name": "Data Processing Agreement Policy", 
            "description": "Signed DPAs required for all customers before data processing. DPAs must specify purposes, retention, sub-processors, and security measures. Annual review and updates required. Template DPAs for standard offerings, custom for enterprise. Sub-processor list maintained publicly.",
            "category": "legal",
            "severity": "critical",
            "responsible_type": "group",
            "compliance_frameworks": ["GDPR", "CCPA", "SOC2"]
        },
        {
            "id": "policy_13",
            "name": "Right to Erasure Policy",
            "description": "Customer data deletion requests must be fulfilled within 30 days. Deletion includes all copies, backups (after retention period), and derived data. Deletion certificate provided. Some data retained for legal/compliance as documented. Automated deletion workflows required.",
            "category": "data_privacy",
            "severity": "critical",
            "responsible_type": "group",
            "compliance_frameworks": ["GDPR", "CCPA", "PIPEDA"]
        },
        {
            "id": "policy_14",
            "name": "Data Breach Notification Policy",
            "description": "Confirmed breaches notified to affected customers within 72 hours. Notifications include scope, impact, remediation steps, and recommendations. Regulatory notifications as required by jurisdiction. Public disclosure for significant breaches. Breach response team activation procedures.",
            "category": "security",
            "severity": "critical",
            "responsible_type": "group",
            "compliance_frameworks": ["GDPR", "CCPA", "SOC2"]
        },
        {
            "id": "policy_15",
            "name": "Third-party Data Processor Policy",
            "description": "All third-party processors vetted for security and compliance. Contracts require equivalent data protection. Annual audits of critical processors. Processor list maintained and available to customers. Change notifications 30 days in advance. Data localization requirements respected.",
            "category": "vendor_management",
            "severity": "high",
            "responsible_type": "group",
            "compliance_frameworks": ["GDPR", "SOC2", "ISO27001"]
        },
        {
            "id": "policy_16",
            "name": "CI/CD Security Policy",
            "description": "All code deployments via automated CI/CD pipelines. Security scanning (SAST/DAST) required before production. No direct production access - all changes via pipeline. Deployment approvals for critical systems. Rollback capabilities required. Container scanning for vulnerabilities.",
            "category": "development",
            "severity": "high",
            "responsible_type": "team",
            "compliance_frameworks": ["SOC2", "ISO27001", "NIST"]
        },
        {
            "id": "policy_17",
            "name": "Disaster Recovery Policy",
            "description": "RPO: 1 hour for critical data, 4 hours for standard. RTO: 4 hours for critical systems, 24 hours for standard. DR testing quarterly with full failover annually. Geo-redundant backups in 3+ regions. Automated failover for critical services. Customer data recovery guarantees.",
            "category": "operations",
            "severity": "critical",
            "responsible_type": "group",
            "compliance_frameworks": ["SOC2", "ISO22301", "Internal"]
        },
        {
            "id": "policy_18",
            "name": "Change Management Policy",
            "description": "All production changes require approval based on risk level. High-risk changes need CAB approval and rollback plan. Change freeze during peak periods. Post-implementation reviews for major changes. Emergency change procedures defined. Customer notification for impacting changes.",
            "category": "operations",
            "severity": "high",
            "responsible_type": "group",
            "compliance_frameworks": ["SOC2", "ITIL", "Internal"]
        },
        {
            "id": "policy_19",
            "name": "Performance Monitoring Policy",
            "description": "All services monitored for availability, latency, and error rates. SLIs/SLOs defined per service. Alerting thresholds at 80% of SLO. Performance baselines established and anomaly detection enabled. Monthly performance reviews and optimization. Customer-facing performance metrics published.",
            "category": "operations",
            "severity": "medium",
            "responsible_type": "team",
            "compliance_frameworks": ["SOC2", "Internal"]
        },
        {
            "id": "policy_20",
            "name": "Data Retention and Deletion Policy",
            "description": "Customer data retained per contractual agreements. Default retention: operational data 90 days, analytical results 1 year, audit logs 2 years. Automated deletion workflows with verification. Legal hold procedures for investigations. Data destruction certificates provided on request.",
            "category": "data_governance",
            "severity": "high",
            "responsible_type": "group",
            "compliance_frameworks": ["GDPR", "CCPA", "SOC2"]
        }
    ]
    
    return policies

def generate_cloud_regions_data():
    """Generate cloud region data for multi-cloud deployments"""
    regions = []
    
    # Define cloud regions for major providers
    cloud_regions = [
        # AWS Regions
        {"provider": "AWS", "region_code": "us-east-1", "region_name": "US East (N. Virginia)", "availability_zones": 6, "data_residency_zone": "US"},
        {"provider": "AWS", "region_code": "us-west-2", "region_name": "US West (Oregon)", "availability_zones": 4, "data_residency_zone": "US"},
        {"provider": "AWS", "region_code": "eu-west-1", "region_name": "EU (Ireland)", "availability_zones": 3, "data_residency_zone": "EU"},
        {"provider": "AWS", "region_code": "eu-central-1", "region_name": "EU (Frankfurt)", "availability_zones": 3, "data_residency_zone": "EU"},
        {"provider": "AWS", "region_code": "ap-southeast-1", "region_name": "Asia Pacific (Singapore)", "availability_zones": 3, "data_residency_zone": "APAC"},
        {"provider": "AWS", "region_code": "ap-northeast-1", "region_name": "Asia Pacific (Tokyo)", "availability_zones": 4, "data_residency_zone": "APAC"},
        
        # GCP Regions
        {"provider": "GCP", "region_code": "us-central1", "region_name": "Iowa", "availability_zones": 4, "data_residency_zone": "US"},
        {"provider": "GCP", "region_code": "us-east1", "region_name": "South Carolina", "availability_zones": 3, "data_residency_zone": "US"},
        {"provider": "GCP", "region_code": "europe-west1", "region_name": "Belgium", "availability_zones": 3, "data_residency_zone": "EU"},
        {"provider": "GCP", "region_code": "europe-west4", "region_name": "Netherlands", "availability_zones": 3, "data_residency_zone": "EU"},
        {"provider": "GCP", "region_code": "asia-southeast1", "region_name": "Singapore", "availability_zones": 3, "data_residency_zone": "APAC"},
        {"provider": "GCP", "region_code": "asia-northeast1", "region_name": "Tokyo", "availability_zones": 3, "data_residency_zone": "APAC"},
        
        # Azure Regions
        {"provider": "Azure", "region_code": "eastus", "region_name": "East US", "availability_zones": 3, "data_residency_zone": "US"},
        {"provider": "Azure", "region_code": "westus2", "region_name": "West US 2", "availability_zones": 3, "data_residency_zone": "US"},
        {"provider": "Azure", "region_code": "northeurope", "region_name": "North Europe", "availability_zones": 3, "data_residency_zone": "EU"},
        {"provider": "Azure", "region_code": "westeurope", "region_name": "West Europe", "availability_zones": 3, "data_residency_zone": "EU"},
        {"provider": "Azure", "region_code": "southeastasia", "region_name": "Southeast Asia", "availability_zones": 3, "data_residency_zone": "APAC"},
        {"provider": "Azure", "region_code": "japaneast", "region_name": "Japan East", "availability_zones": 3, "data_residency_zone": "APAC"}
    ]
    
    for i, region in enumerate(cloud_regions):
        regions.append({
            "id": f"region_{i+1}",
            "provider": region["provider"],
            "region_code": region["region_code"],
            "region_name": region["region_name"],
            "availability_zones": region["availability_zones"],
            "data_residency_zone": region["data_residency_zone"]
        })
    
    return regions

def generate_platform_components_data():
    """Generate platform component data for expertise mapping"""
    components = []
    
    # Define platform components with their properties
    platform_components = [
        # Core Services
        {"name": "API Gateway", "type": "service", "tier": "core", "owner_team_id": "team_14", "documentation_url": "https://docs.company.com/api-gateway"},
        {"name": "Authentication Service", "type": "service", "tier": "core", "owner_team_id": "team_6", "documentation_url": "https://docs.company.com/auth-service"},
        {"name": "Data Ingestion Pipeline", "type": "pipeline", "tier": "core", "owner_team_id": "team_1", "documentation_url": "https://docs.company.com/data-ingestion"},
        {"name": "Stream Processing Engine", "type": "pipeline", "tier": "core", "owner_team_id": "team_1", "documentation_url": "https://docs.company.com/stream-processing"},
        {"name": "Batch Processing Framework", "type": "pipeline", "tier": "core", "owner_team_id": "team_1", "documentation_url": "https://docs.company.com/batch-processing"},
        
        # Data Storage
        {"name": "Data Lake Storage", "type": "database", "tier": "core", "owner_team_id": "team_5", "documentation_url": "https://docs.company.com/data-lake"},
        {"name": "Time Series Database", "type": "database", "tier": "core", "owner_team_id": "team_5", "documentation_url": "https://docs.company.com/tsdb"},
        {"name": "Metadata Store", "type": "database", "tier": "supporting", "owner_team_id": "team_5", "documentation_url": "https://docs.company.com/metadata-store"},
        {"name": "Feature Store", "type": "database", "tier": "core", "owner_team_id": "team_4", "documentation_url": "https://docs.company.com/feature-store"},
        
        # Analytics & ML
        {"name": "Analytics Engine", "type": "service", "tier": "core", "owner_team_id": "team_2", "documentation_url": "https://docs.company.com/analytics-engine"},
        {"name": "ML Inference Service", "type": "service", "tier": "core", "owner_team_id": "team_4", "documentation_url": "https://docs.company.com/ml-inference"},
        {"name": "Model Training Pipeline", "type": "pipeline", "tier": "supporting", "owner_team_id": "team_4", "documentation_url": "https://docs.company.com/model-training"},
        {"name": "Data Visualization Service", "type": "service", "tier": "core", "owner_team_id": "team_2", "documentation_url": "https://docs.company.com/visualization"},
        
        # Customer-Facing
        {"name": "Customer Portal", "type": "service", "tier": "core", "owner_team_id": "team_14", "documentation_url": "https://docs.company.com/customer-portal"},
        {"name": "Admin Dashboard", "type": "service", "tier": "supporting", "owner_team_id": "team_14", "documentation_url": "https://docs.company.com/admin-dashboard"},
        {"name": "Reporting Service", "type": "service", "tier": "core", "owner_team_id": "team_2", "documentation_url": "https://docs.company.com/reporting"},
        
        # Infrastructure & Monitoring
        {"name": "Monitoring & Alerting", "type": "service", "tier": "supporting", "owner_team_id": "team_5", "documentation_url": "https://docs.company.com/monitoring"},
        {"name": "Log Aggregation Service", "type": "service", "tier": "supporting", "owner_team_id": "team_5", "documentation_url": "https://docs.company.com/logging"},
        {"name": "CI/CD Pipeline", "type": "pipeline", "tier": "supporting", "owner_team_id": "team_5", "documentation_url": "https://docs.company.com/cicd"},
        {"name": "Service Mesh", "type": "service", "tier": "supporting", "owner_team_id": "team_5", "documentation_url": "https://docs.company.com/service-mesh"}
    ]
    
    for i, component in enumerate(platform_components):
        components.append({
            "id": f"component_{i+1}",
            "name": component["name"],
            "type": component["type"],
            "tier": component["tier"],
            "owner_team_id": component["owner_team_id"],
            "documentation_url": component["documentation_url"]
        })
    
    return components

def generate_relationships():
    """Generate relationships between entities"""
    people = generate_people_data()
    teams = generate_teams_data()
    groups = generate_groups_data()
    policies = generate_policies_data()
    skills = generate_skills_data()
    projects = generate_projects_data()
    clients = generate_clients_data()
    sprints = generate_sprints_data()
    offices = generate_offices_data()
    languages = generate_languages_data()
    holidays = generate_holidays_data()
    compliance_frameworks = generate_compliance_data()
    data_residency_zones = generate_data_residency_data()
    schedules = generate_schedules_data()
    incidents = generate_incidents_data()
    visas = generate_visas_data()
    metrics = generate_metrics_data()
    cloud_regions = generate_cloud_regions_data()
    platform_components = generate_platform_components_data()
    
    relationships = {
        "person_team_memberships": [],
        "person_group_memberships": [],
        "team_policy_responsibilities": [],
        "group_policy_responsibilities": [],
        "person_skills": [],
        "person_project_allocations": [],
        "project_skill_requirements": [],
        "team_project_delivery": [],
        "person_mentorships": [],
        "person_backups": [],
        "person_specializations": [],
        "person_office_assignments": [],
        "person_languages": [],
        "office_collaborations": [],
        "office_compliance": [],
        "client_compliance": [],
        "office_data_residency": [],
        "project_data_residency": [],
        "person_on_call": [],
        "person_incident_response": [],
        "team_handoffs": [],
        "person_visas": [],
        "team_supports_region": [],
        "component_deployed_in": [],
        "client_uses_component": [],
        "person_expert_in": []
    }
    
    # Assign people to teams (each person belongs to 1 primary team)
    for person in people:
        # Find teams in the same department
        dept_teams = [t for t in teams if t["department"] == person["department"]]
        if dept_teams:
            team = random.choice(dept_teams)
        else:
            team = random.choice(teams)
        
        relationships["person_team_memberships"].append({
            "person_id": person["id"],
            "team_id": team["id"],
            "role": person["role"],
            "is_lead": random.random() < 0.15  # 15% chance of being team lead
        })
    
    # Assign people to groups (cross-functional, 3-8 people per group)
    for group in groups:
        # Get people from relevant departments
        if group["lead_department"] == "Security & Compliance":
            relevant_people = [p for p in people if p["department"] in ["Security & Compliance", "Engineering", "Infrastructure & DevOps"]]
        elif group["lead_department"] == "Data Science":
            relevant_people = [p for p in people if p["department"] in ["Data Science", "Analytics Engineering", "Product"]]
        elif group["lead_department"] == "Engineering":
            relevant_people = [p for p in people if p["department"] in ["Engineering", "Infrastructure & DevOps", "Security & Compliance"]]
        elif group["lead_department"] == "Data Platform Engineering":
            relevant_people = [p for p in people if p["department"] in ["Data Platform Engineering", "Analytics Engineering", "Infrastructure & DevOps"]]
        elif group["lead_department"] == "Product":
            relevant_people = [p for p in people if p["department"] in ["Product", "Engineering", "Data Science"]]
        elif group["lead_department"] == "Customer Success":
            relevant_people = [p for p in people if p["department"] in ["Customer Success", "Professional Services", "Solutions Architecture"]]
        elif group["lead_department"] == "Infrastructure & DevOps":
            relevant_people = [p for p in people if p["department"] in ["Infrastructure & DevOps", "Engineering", "Security & Compliance"]]
        elif group["lead_department"] == "Solutions Architecture":
            relevant_people = [p for p in people if p["department"] in ["Solutions Architecture", "Professional Services", "Engineering"]]
        elif group["lead_department"] == "Sales":
            relevant_people = [p for p in people if p["department"] in ["Sales", "Marketing", "Customer Success"]]
        else:
            relevant_people = people
        
        # Select 3-8 people for this group
        group_size = random.randint(3, min(8, len(relevant_people)))
        group_members = random.sample(relevant_people, group_size)
        
        for i, person in enumerate(group_members):
            relationships["person_group_memberships"].append({
                "person_id": person["id"],
                "group_id": group["id"],
                "role": "Lead" if i == 0 else "Member",
                "joined_date": fake.date_between(start_date='-2y', end_date='today').isoformat()
            })
    
    # Assign policies to teams or groups based on responsible_type
    for policy in policies:
        if policy["responsible_type"] == "team":
            # Assign to relevant teams based on policy category
            if policy["category"] == "data_governance":
                eligible_teams = [t for t in teams if t["department"] in ["Data Platform Engineering", "Analytics Engineering", "Data Science"]]
            elif policy["category"] == "platform":
                eligible_teams = [t for t in teams if t["department"] in ["Engineering", "Data Platform Engineering", "Infrastructure & DevOps"]]
            elif policy["category"] == "security":
                eligible_teams = [t for t in teams if t["department"] in ["Security & Compliance", "Engineering", "Infrastructure & DevOps"]]
            elif policy["category"] in ["development", "operations"]:
                eligible_teams = [t for t in teams if t["department"] in ["Engineering", "Infrastructure & DevOps", "Data Platform Engineering"]]
            else:
                eligible_teams = teams
            
            # Assign to 1-3 teams
            responsible_teams = random.sample(eligible_teams, random.randint(1, min(3, len(eligible_teams))))
            for team in responsible_teams:
                relationships["team_policy_responsibilities"].append({
                    "team_id": team["id"],
                    "policy_id": policy["id"],
                    "responsibility_type": random.choice(["owner", "contributor", "reviewer"]),
                    "assigned_date": fake.date_between(start_date='-1y', end_date='today').isoformat()
                })
        
        else:  # responsible_type == "group"
            # Assign to relevant groups
            if policy["category"] == "data_governance":
                eligible_groups = [g for g in groups if "Data Governance" in g["name"] or "Data Quality" in g["name"]]
            elif policy["category"] == "security":
                eligible_groups = [g for g in groups if "Security" in g["name"] or "Compliance" in g["name"]]
            elif policy["category"] == "data_privacy":
                eligible_groups = [g for g in groups if "Data" in g["name"] or "Compliance" in g["name"] or "Privacy" in g["name"]]
            elif policy["category"] == "platform":
                eligible_groups = [g for g in groups if "API" in g["name"] or "SLA" in g["name"] or "Architecture" in g["name"]]
            elif policy["category"] == "development":
                eligible_groups = [g for g in groups if "Architecture" in g["name"] or "API" in g["name"]]
            else:
                eligible_groups = groups
            
            if eligible_groups:
                responsible_group = random.choice(eligible_groups)
                relationships["group_policy_responsibilities"].append({
                    "group_id": responsible_group["id"],
                    "policy_id": policy["id"],
                    "responsibility_type": "owner",
                    "assigned_date": fake.date_between(start_date='-1y', end_date='today').isoformat()
                })
    
    # Assign skills to people based on their role and department
    for person in people:
        num_skills = random.randint(3, 8)
        person_skills = []
        
        # Core skills based on department
        if person["department"] in ["Data Platform Engineering", "Analytics Engineering"]:
            core_skills = ["skill_1", "skill_6", "skill_12", "skill_13", "skill_14", "skill_15", "skill_16", "skill_17", "skill_18"]
        elif person["department"] == "Data Science":
            core_skills = ["skill_1", "skill_6", "skill_21", "skill_22", "skill_23", "skill_24", "skill_25"]
        elif person["department"] in ["Engineering", "Infrastructure & DevOps"]:
            core_skills = ["skill_1", "skill_2", "skill_3", "skill_4", "skill_5", "skill_26", "skill_27", "skill_28"]
        else:
            core_skills = ["skill_1", "skill_6", "skill_39", "skill_40", "skill_41"]
        
        # Add cloud skills for technical roles
        if person["department"] in ["Data Platform Engineering", "Engineering", "Infrastructure & DevOps", "Data Science"]:
            core_skills.extend(["skill_9", "skill_10", "skill_11"])
        
        selected_skills = random.sample(core_skills, min(num_skills, len(core_skills)))
        
        for skill_id in selected_skills:
            proficiency = random.choice(["beginner", "intermediate", "advanced", "expert"])
            years_exp = random.randint(1, min(10, person["years_experience"]))
            
            relationships["person_skills"].append({
                "person_id": person["id"],
                "skill_id": skill_id,
                "proficiency_level": proficiency,
                "years_experience": years_exp,
                "last_used": fake.date_between(start_date='-6m', end_date='today').isoformat()
            })
    
    # Assign people to projects
    active_projects = [p for p in projects if p["status"] in ["active", "planning"]]
    for project in active_projects:
        # Allocate 3-12 people per project
        num_people = random.randint(3, 12)
        allocated_people = random.sample(people, num_people)
        
        for person in allocated_people:
            allocation = random.randint(20, 100)  # percentage
            relationships["person_project_allocations"].append({
                "person_id": person["id"],
                "project_id": project["id"],
                "allocation_percentage": allocation,
                "start_date": project["start_date"],
                "end_date": project["end_date"],
                "role_on_project": random.choice(["lead", "contributor", "advisor", "reviewer"])
            })
    
    # Define project skill requirements
    for project in projects:
        # Each project requires 2-5 skills
        num_required_skills = random.randint(2, 5)
        
        if project["type"] == "ml":
            relevant_skills = ["skill_1", "skill_21", "skill_22", "skill_23", "skill_24", "skill_25"]
        elif project["type"] == "infrastructure":
            relevant_skills = ["skill_26", "skill_27", "skill_28", "skill_9", "skill_10", "skill_11"]
        elif project["type"] == "platform":
            relevant_skills = ["skill_1", "skill_2", "skill_3", "skill_12", "skill_13", "skill_14"]
        elif project["type"] == "analytics":
            relevant_skills = ["skill_1", "skill_6", "skill_15", "skill_16", "skill_17", "skill_18"]
        else:
            relevant_skills = list(range(1, 53))
            relevant_skills = [f"skill_{i}" for i in relevant_skills]
        
        selected_skills = random.sample(relevant_skills, min(num_required_skills, len(relevant_skills)))
        
        for skill_id in selected_skills:
            relationships["project_skill_requirements"].append({
                "project_id": project["id"],
                "skill_id": skill_id,
                "priority": random.choice(["critical", "high", "medium", "low"]),
                "min_proficiency_level": random.choice(["intermediate", "advanced", "expert"]),
                "headcount_needed": random.randint(1, 3)
            })
    
    # Assign teams to deliver projects
    for project in projects:
        # 1-3 teams per project
        num_teams = random.randint(1, 3)
        selected_teams = random.sample(teams, num_teams)
        
        for team in selected_teams:
            relationships["team_project_delivery"].append({
                "team_id": team["id"],
                "project_id": project["id"],
                "responsibility": random.choice(["primary", "supporting", "consulting"]),
                "committed_capacity": random.randint(20, 80)  # percentage of team capacity
            })
    
    # Create mentorship relationships
    senior_people = [p for p in people if p["seniority"] in ["Senior", "Staff", "Principal"]]
    junior_people = [p for p in people if p["seniority"] in ["Junior", "Mid"]]
    
    for mentor in random.sample(senior_people, min(30, len(senior_people))):
        # Each mentor has 1-3 mentees
        num_mentees = random.randint(1, 3)
        potential_mentees = [p for p in junior_people if p["department"] == mentor["department"]]
        
        if potential_mentees:
            mentees = random.sample(potential_mentees, min(num_mentees, len(potential_mentees)))
            for mentee in mentees:
                relationships["person_mentorships"].append({
                    "mentor_id": mentor["id"],
                    "mentee_id": mentee["id"],
                    "start_date": fake.date_between(start_date='-1y', end_date='today').isoformat(),
                    "focus_area": random.choice(["technical skills", "career development", "domain expertise", "leadership"])
                })
    
    # Create backup relationships for critical roles
    critical_people = [p for p in people if "Lead" in p["role"] or "Manager" in p["role"] or "Principal" in p["role"]]
    
    for person in critical_people:
        # Find potential backups in same department
        potential_backups = [p for p in people if p["department"] == person["department"] and p["id"] != person["id"]]
        
        if potential_backups:
            backup = random.choice(potential_backups)
            relationships["person_backups"].append({
                "primary_person_id": person["id"],
                "backup_person_id": backup["id"],
                "coverage_type": random.choice(["full", "partial", "emergency"]),
                "readiness_level": random.choice(["ready", "in_training", "identified"])
            })
    
    # Create specialization relationships
    for person in people:
        # 20% of people have specializations
        if random.random() < 0.2:
            if person["department"] in ["Data Platform Engineering", "Analytics Engineering"]:
                specializations = ["Real-time Processing", "Data Governance", "Performance Optimization", "Data Modeling"]
            elif person["department"] == "Data Science":
                specializations = ["Computer Vision", "NLP", "Time Series", "Recommender Systems", "MLOps"]
            elif person["department"] == "Engineering":
                specializations = ["API Design", "Microservices", "Frontend Architecture", "Security"]
            else:
                specializations = ["Process Improvement", "Strategic Planning", "Cross-functional Leadership"]
            
            spec = random.choice(specializations)
            relationships["person_specializations"].append({
                "person_id": person["id"],
                "specialization": spec,
                "expertise_level": random.choice(["recognized", "expert", "thought_leader"]),
                "years_in_specialty": random.randint(2, 8)
            })
    
    # Assign people to offices based on their location
    office_mapping = {
        "San Francisco": "office_sf",
        "Los Angeles": "office_sf",
        "Seattle": "office_sf",
        "Portland": "office_sf",
        "New York": "office_ny",
        "Boston": "office_ny",
        "Miami": "office_ny",
        "Atlanta": "office_ny",
        "Chicago": "office_ny",
        "Austin": "office_ny",
        "Denver": "office_sf",  # Mountain time but closer to SF office
        "Toronto": "office_ny",
        "London": "office_london",
        "Berlin": "office_frankfurt",
        "Paris": "office_paris",
        "Tokyo": "office_tokyo",
        "Singapore": "office_hk",  # No Singapore office, assign to HK
        "Sydney": "office_sydney",
        "Hong Kong": "office_hk",
        "Remote": None  # Will be assigned based on timezone
    }
    
    for person in people:
        office_id = office_mapping.get(person["location"])
        
        # For remote workers, assign based on timezone
        if office_id is None:
            timezone_office_map = {
                "US/Pacific": "office_sf",
                "US/Mountain": "office_sf",
                "US/Central": "office_ny",
                "US/Eastern": "office_ny",
                "Europe/London": "office_london",
                "Europe/Berlin": "office_frankfurt",
                "Europe/Paris": "office_paris",
                "Asia/Tokyo": "office_tokyo",
                "Asia/Hong_Kong": "office_hk",
                "Asia/Singapore": "office_hk",
                "Australia/Sydney": "office_sydney"
            }
            office_id = timezone_office_map.get(person["timezone"], "office_sf")
        
        relationships["person_office_assignments"].append({
            "person_id": person["id"],
            "office_id": office_id,
            "start_date": person["hire_date"],
            "is_remote": person["location"] == "Remote",
            "desk_location": f"Floor {random.randint(1, 5)}, Section {random.choice(['A', 'B', 'C', 'D'])}" if person["location"] != "Remote" else None
        })
    
    # Assign languages to people
    # Language mapping based on office/location
    office_language_map = {
        "office_sf": ["lang_en", "lang_es"],  # English + Spanish common in California
        "office_ny": ["lang_en", "lang_es"],   # English + Spanish common in NY
        "office_london": ["lang_en"],
        "office_frankfurt": ["lang_de", "lang_en"],
        "office_paris": ["lang_fr", "lang_en"],
        "office_tokyo": ["lang_ja", "lang_en"],
        "office_hk": ["lang_zh", "lang_en"],
        "office_sydney": ["lang_en"]
    }
    
    for person_office in relationships["person_office_assignments"]:
        person_id = person_office["person_id"]
        office_id = person_office["office_id"]
        office_languages = office_language_map.get(office_id, ["lang_en"])
        
        # Everyone speaks at least one language
        primary_lang = office_languages[0]
        relationships["person_languages"].append({
            "person_id": person_id,
            "language_id": primary_lang,
            "proficiency": "native" if primary_lang != "lang_en" else random.choice(["native", "fluent"]),
            "is_primary": True,
            "certified": False,
            "certification_date": None
        })
        
        # English as secondary language for non-English primary speakers
        if primary_lang != "lang_en":
            relationships["person_languages"].append({
                "person_id": person_id,
                "language_id": "lang_en",
                "proficiency": random.choice(["fluent", "professional", "professional"]),  # Most are professional
                "is_primary": False,
                "certified": random.random() < 0.3,  # 30% have certification
                "certification_date": fake.date_between(start_date='-5y', end_date='today').isoformat() if random.random() < 0.3 else None
            })
        
        # 20% of people speak an additional language
        if random.random() < 0.2:
            additional_langs = ["lang_es", "lang_fr", "lang_de", "lang_zh", "lang_ja", "lang_ko", "lang_pt", "lang_it", "lang_ru", "lang_ar", "lang_hi"]
            # Remove languages they already speak
            existing_langs = [rel["language_id"] for rel in relationships["person_languages"] if rel["person_id"] == person_id]
            available_langs = [lang for lang in additional_langs if lang not in existing_langs]
            
            if available_langs:
                additional_lang = random.choice(available_langs)
                relationships["person_languages"].append({
                    "person_id": person_id,
                    "language_id": additional_lang,
                    "proficiency": random.choice(["basic", "professional", "fluent"]),
                    "is_primary": False,
                    "certified": False,
                    "certification_date": None
                })
    
    # Create office collaboration relationships based on timezone overlap
    office_pairs = [
        ("office_sf", "office_ny", 3),      # 3 hours overlap
        ("office_ny", "office_london", 4),   # 4 hours overlap
        ("office_london", "office_frankfurt", 8),  # Full overlap
        ("office_london", "office_paris", 8),      # Full overlap
        ("office_frankfurt", "office_paris", 8),   # Full overlap
        ("office_tokyo", "office_hk", 7),    # 7 hours overlap
        ("office_hk", "office_sydney", 5),   # 5 hours overlap
        ("office_sf", "office_sydney", 2),   # 2 hours overlap (across date line)
        ("office_london", "office_hk", 1),   # 1 hour overlap
    ]
    
    for office1_id, office2_id, overlap_hours in office_pairs:
        # Bidirectional relationships
        relationships["office_collaborations"].append({
            "office1_id": office1_id,
            "office2_id": office2_id,
            "overlap_hours": overlap_hours,
            "preferred_meeting_times": [f"{10+i}:00" for i in range(overlap_hours)]  # Starting from 10am
        })
        relationships["office_collaborations"].append({
            "office1_id": office2_id,
            "office2_id": office1_id,
            "overlap_hours": overlap_hours,
            "preferred_meeting_times": [f"{10+i}:00" for i in range(overlap_hours)]
        })
    
    # Office-Compliance relationships
    # Map offices to their applicable compliance frameworks based on region
    for office in offices:
        applicable_frameworks = []
        
        # GDPR for EU offices
        if office["region"] == "EMEA" and office["country"] in ["United Kingdom", "Germany", "France"]:
            applicable_frameworks.append("comp_gdpr")
        
        # UK offices get GDPR (UK follows EU GDPR)
        # if office["country"] == "United Kingdom":
        #     applicable_frameworks.append("comp_gdpr")  # UK follows EU GDPR
        
        # CCPA for California
        if office["id"] == "office_sf" or office["id"] == "office_la":
            applicable_frameworks.append("comp_ccpa")
        
        # SOC2 for all offices (company-wide)
        applicable_frameworks.append("comp_soc2")
        
        # APPI for Japan
        if office["country"] == "Japan":
            applicable_frameworks.append("comp_appi")
        
        # PIPEDA for Canada (if we had Canadian offices)
        # LGPD for Brazil (if we had Brazilian offices)
        
        for framework_id in applicable_frameworks:
            relationships["office_compliance"].append({
                "office_id": office["id"],
                "compliance_id": framework_id,
                "since": "2022-01-01",
                "attestation_date": "2023-12-15",
                "next_audit": "2024-12-15"
            })
    
    # Client-Compliance requirements
    # Different clients require different compliance based on their industry
    for client in clients:
        required_frameworks = []
        
        # Healthcare clients need HIPAA
        if client["industry"] == "Healthcare":
            required_frameworks.append({
                "framework_id": "comp_hipaa",
                "contractual": True,
                "sla_impact": "critical"
            })
        
        # Pharmaceutical clients also need HIPAA for patient data
        if client["industry"] == "Pharmaceutical":
            required_frameworks.append({
                "framework_id": "comp_hipaa",
                "contractual": True,
                "sla_impact": "high"
            })
        
        # Financial services need PCI-DSS and SOC2
        if client["industry"] in ["Financial Services", "Insurance"]:
            required_frameworks.extend([
                {"framework_id": "comp_pci_dss", "contractual": True, "sla_impact": "high"},
                {"framework_id": "comp_soc2", "contractual": True, "sla_impact": "critical"}
            ])
        
        # Government clients need strict compliance
        if client["industry"] == "Government":
            required_frameworks.extend([
                {"framework_id": "comp_soc2", "contractual": True, "sla_impact": "critical"},
                {"framework_id": "comp_gdpr", "contractual": False, "sla_impact": "medium"}  # For citizen data
            ])
        
        # Education clients handling student data
        if client["industry"] == "Education":
            required_frameworks.append({
                "framework_id": "comp_soc2",
                "contractual": True,
                "sla_impact": "high"
            })
        
        # EU-based clients need GDPR
        # For this example, randomly assign some clients as EU-based
        if random.choice([True, False]) and client["tier"] in ["enterprise", "strategic"]:
            if not any(f["framework_id"] == "comp_gdpr" for f in required_frameworks):
                required_frameworks.append({
                    "framework_id": "comp_gdpr",
                    "contractual": True,
                    "sla_impact": "critical"
                })
        
        # All enterprise clients require SOC2
        if client["tier"] == "enterprise":
            if not any(f["framework_id"] == "comp_soc2" for f in required_frameworks):
                required_frameworks.append({
                    "framework_id": "comp_soc2",
                    "contractual": True,
                    "sla_impact": "high"
                })
        
        for req in required_frameworks:
            relationships["client_compliance"].append({
                "client_id": client["id"],
                "compliance_id": req["framework_id"],
                "contractual": req["contractual"],
                "sla_impact": req["sla_impact"]
            })
    
    # Office-DataResidency enforcement
    # Map offices to their data residency zones
    office_to_dr_zone = {
        "office_sf": "dr_us",
        "office_ny": "dr_us",
        "office_london": "dr_uk",
        "office_frankfurt": "dr_eu",
        "office_paris": "dr_eu",
        "office_tokyo": "dr_apac",
        "office_hk": "dr_apac",
        "office_sydney": "dr_apac"
    }
    
    for office_id, dr_zone_id in office_to_dr_zone.items():
        relationships["office_data_residency"].append({
            "office_id": office_id,
            "data_residency_id": dr_zone_id
        })
    
    # Project-DataResidency assignments
    # Projects store data based on their primary client's requirements
    for project in projects:
        # Find the client for this project
        client = next((c for c in clients if c["id"] == project["client_id"]), None)
        if client:
            # Determine data residency based on client and project type
            dr_zone_id = "dr_us"  # Default
            
            # If client requires GDPR, use EU data residency
            client_compliance = [r for r in relationships["client_compliance"] if r["client_id"] == client["id"]]
            if any(cc["compliance_id"] == "comp_gdpr" for cc in client_compliance):
                dr_zone_id = "dr_eu"
            # Healthcare projects might need specific US regions
            elif "health" in client["industry"].lower():
                dr_zone_id = "dr_us"
            # Financial projects in APAC
            elif "financial" in client["industry"].lower() and project["id"] in ["project_7", "project_8"]:
                dr_zone_id = "dr_apac"
            
            relationships["project_data_residency"].append({
                "project_id": project["id"],
                "data_residency_id": dr_zone_id
            })
    
    # Create ON_CALL relationships between people and schedules
    # Get people by office and expertise for realistic assignments
    people_by_office = {}
    for person_office in relationships["person_office_assignments"]:
        office_id = person_office["office_id"]
        if office_id not in people_by_office:
            people_by_office[office_id] = []
        people_by_office[office_id].append(person_office["person_id"])
    
    # Assign people to schedules based on office and schedule type
    for schedule in schedules:
        if schedule["office_id"] and schedule["office_id"] in people_by_office:
            # Get people from this office
            office_people = people_by_office[schedule["office_id"]]
            
            # Filter by seniority for different coverage types
            available_people = []
            for person_id in office_people:
                person = next((p for p in people if p["id"] == person_id), None)
                if person:
                    # Senior people for escalation, mix for primary/backup
                    if schedule["coverage_type"] == "escalation" and person["seniority"] in ["Senior", "Staff", "Principal"]:
                        available_people.append(person_id)
                    elif schedule["coverage_type"] in ["primary", "backup"]:
                        available_people.append(person_id)
            
            # Assign 1-2 people per schedule
            if available_people:
                num_assignments = 1 if schedule["coverage_type"] == "primary" else min(2, len(available_people))
                assigned = random.sample(available_people, min(num_assignments, len(available_people)))
                
                for person_id in assigned:
                    reachable_via = random.choice(["phone", "slack", "pagerduty"])
                    relationships["person_on_call"].append({
                        "person_id": person_id,
                        "schedule_id": schedule["id"],
                        "role": schedule["coverage_type"],
                        "reachable_via": reachable_via
                    })
        
        # Handle P0 escalation schedules (cross-office)
        elif schedule.get("severity_focus") == "P0":
            # Get senior engineers from the region
            region_offices = [o for o in offices if o["region"] == schedule["region"]]
            region_people = []
            for office in region_offices:
                if office["id"] in people_by_office:
                    for person_id in people_by_office[office["id"]]:
                        person = next((p for p in people if p["id"] == person_id), None)
                        if person and person["seniority"] in ["Senior", "Staff", "Principal"]:
                            region_people.append(person_id)
            
            # Assign 2-3 people for P0 coverage
            if region_people:
                assigned = random.sample(region_people, min(3, len(region_people)))
                for person_id in assigned:
                    relationships["person_on_call"].append({
                        "person_id": person_id,
                        "schedule_id": schedule["id"],
                        "role": "p0_escalation",
                        "reachable_via": "pagerduty"
                    })
    
    # Create RESPONDED_TO relationships between people and incidents
    for incident in incidents:
        if incident["status"] == "resolved":
            # Get people from affected regions who could respond
            responders = []
            for region in incident["affected_regions"]:
                region_offices = [o for o in offices if o["region"] == region]
                for office in region_offices:
                    if office["id"] in people_by_office:
                        office_people = people_by_office[office["id"]]
                        # For P0/P1, prefer senior people; for P2/P3, anyone can respond
                        for person_id in office_people:
                            person = next((p for p in people if p["id"] == person_id), None)
                            if person:
                                if incident["severity"] in ["P0", "P1"]:
                                    if person["seniority"] in ["Senior", "Staff", "Principal"]:
                                        responders.append((person_id, person["seniority"]))
                                else:
                                    responders.append((person_id, person["seniority"]))
            
            # Select 1-3 responders based on severity
            num_responders = 3 if incident["severity"] == "P0" else 2 if incident["severity"] == "P1" else 1
            if responders:
                selected_responders = random.sample(responders, min(num_responders, len(responders)))
                
                for idx, (person_id, seniority) in enumerate(selected_responders):
                    # First responder has shortest response time
                    if idx == 0:
                        # Response time based on severity: P0: 5-15 min, P1: 10-30 min, P2: 20-60 min, P3: 30-120 min
                        if incident["severity"] == "P0":
                            response_time = random.randint(5, 15)
                        elif incident["severity"] == "P1":
                            response_time = random.randint(10, 30)
                        elif incident["severity"] == "P2":
                            response_time = random.randint(20, 60)
                        else:
                            response_time = random.randint(30, 120)
                        role = "primary_responder"
                    else:
                        # Secondary responders join later
                        response_time = random.randint(15, 45) if incident["severity"] in ["P0", "P1"] else random.randint(30, 90)
                        role = "secondary_responder"
                    
                    relationships["person_incident_response"].append({
                        "person_id": person_id,
                        "incident_id": incident["id"],
                        "response_time_minutes": response_time,
                        "role": role
                    })
    
    # Create HANDS_OFF_TO relationships between teams for 24/7 coverage
    # Map teams to their primary office timezone
    team_timezones = {}
    for team in teams:
        # Find the most common office among team members
        team_offices = {}
        for membership in relationships["person_team_memberships"]:
            if membership["team_id"] == team["id"]:
                person_id = membership["person_id"]
                # Find person's office
                for office_assignment in relationships["person_office_assignments"]:
                    if office_assignment["person_id"] == person_id:
                        office_id = office_assignment["office_id"]
                        team_offices[office_id] = team_offices.get(office_id, 0) + 1
                        break
        
        # Assign team to most common office
        if team_offices:
            primary_office_id = max(team_offices, key=team_offices.get)
            office = next((o for o in offices if o["id"] == primary_office_id), None)
            if office:
                team_timezones[team["id"]] = {
                    "timezone": office["timezone"],
                    "offset": office["timezone_offset"],
                    "region": office["region"]
                }
    
    # Create handoff relationships based on timezone progression
    # Define handoff patterns (who hands off to whom based on timezone)
    handoff_patterns = [
        # Americas to EMEA
        {"from_region": "AMERICAS", "to_region": "EMEA", "handoff_time": "17:00", "handoff_type": "end_of_day"},
        # EMEA to APAC
        {"from_region": "EMEA", "to_region": "APAC", "handoff_time": "17:00", "handoff_type": "end_of_day"},
        # APAC to Americas
        {"from_region": "APAC", "to_region": "AMERICAS", "handoff_time": "17:00", "handoff_type": "end_of_day"},
        # Within regions for critical services
        {"from_region": "AMERICAS", "to_region": "AMERICAS", "handoff_time": "09:00", "handoff_type": "morning_sync"},
        {"from_region": "EMEA", "to_region": "EMEA", "handoff_time": "09:00", "handoff_type": "morning_sync"},
        {"from_region": "APAC", "to_region": "APAC", "handoff_time": "09:00", "handoff_type": "morning_sync"}
    ]
    
    # Create handoffs between teams in similar functions but different regions
    for pattern in handoff_patterns:
        from_teams = [t for t in teams if t["id"] in team_timezones and team_timezones[t["id"]]["region"] == pattern["from_region"]]
        to_teams = [t for t in teams if t["id"] in team_timezones and team_timezones[t["id"]]["region"] == pattern["to_region"]]
        
        # Match teams by department/focus area
        for from_team in from_teams:
            matching_to_teams = [t for t in to_teams if t["department"] == from_team["department"] or t["focus"] == from_team["focus"]]
            if matching_to_teams and from_team["id"] != matching_to_teams[0]["id"]:
                to_team = matching_to_teams[0]
                relationships["team_handoffs"].append({
                    "from_team_id": from_team["id"],
                    "to_team_id": to_team["id"],
                    "handoff_time": pattern["handoff_time"],
                    "handoff_type": pattern["handoff_type"]
                })
    
    # Create person-visa relationships
    # Assign visas to people based on their office location
    for person in people:
        # Find person's office
        person_office_rel = next((rel for rel in relationships["person_office_assignments"] if rel["person_id"] == person["id"]), None)
        if person_office_rel:
            office = next((o for o in offices if o["id"] == person_office_rel["office_id"]), None)
            if office:
                # Determine if person needs visa based on office location
                # Assume some people are locals, some need visas
                needs_visa = random.random() < 0.3  # 30% of people need visas
                
                if needs_visa:
                    # Find appropriate visas for the office country
                    country_visas = [v for v in visas if v["country"] == office["country"] and v["type"] != "Business"]
                    
                    if country_visas:
                        # Choose a visa based on seniority and role
                        if person["seniority"] in ["Principal", "Staff", "Senior"]:
                            # Senior people more likely to have permanent/longer visas
                            perm_visas = [v for v in country_visas if v["max_duration_years"] == 0 or v["max_duration_years"] >= 5]
                            visa = random.choice(perm_visas) if perm_visas else random.choice(country_visas)
                        else:
                            # Junior people get regular work visas
                            work_visas = [v for v in country_visas if v["max_duration_years"] > 0 and v["type"] not in ["Permanent Resident", "ILR", "Green Card"]]
                            visa = random.choice(work_visas) if work_visas else random.choice(country_visas)
                        
                        # Determine visa status
                        issued_date = datetime.strptime(visa["issued_date"], "%Y-%m-%d")
                        expiry_date = datetime.strptime(visa["expiry_date"], "%Y-%m-%d")
                        now = datetime.now()
                        
                        if expiry_date < now:
                            status = "expired"
                        elif (expiry_date - now).days < 90:
                            status = "expiring_soon"
                        else:
                            status = "active"
                        
                        # Sponsor is the company
                        sponsor = "GlobalDataCorp"
                        
                        relationships["person_visas"].append({
                            "person_id": person["id"],
                            "visa_id": visa["id"],
                            "status": status,
                            "sponsor": sponsor
                        })
    
    # Add some people with multiple visas (e.g., business visas for travel)
    senior_people = [p for p in people if p["seniority"] in ["Principal", "Staff", "Senior"]]
    for person in random.sample(senior_people, min(20, len(senior_people))):
        # Add business visas for frequent travelers
        business_visas = [v for v in visas if v["type"] == "Business"]
        if business_visas:
            for _ in range(random.randint(1, 3)):  # 1-3 business visas
                visa = random.choice(business_visas)
                # Check if person already has this visa
                existing = any(rel["person_id"] == person["id"] and rel["visa_id"] == visa["id"] 
                              for rel in relationships["person_visas"])
                if not existing:
                    relationships["person_visas"].append({
                        "person_id": person["id"],
                        "visa_id": visa["id"],
                        "status": "active",
                        "sponsor": "Self"
                    })
    
    # Generate SUPPORTS_REGION relationships (Team -> Client)
    # Customer Success and Professional Services teams support clients based on regions
    support_teams = [t for t in teams if t["department"] in ["Customer Success", "Professional Services", "Solutions Architecture"]]
    for team in support_teams:
        # Each support team covers specific regions
        if "APAC" in team["name"]:
            supported_regions = ["APAC"]
        elif "EMEA" in team["name"]:
            supported_regions = ["EMEA"]
        elif "Americas" in team["name"]:
            supported_regions = ["AMERICAS"]
        else:
            # General teams support all regions but with varying coverage
            supported_regions = ["AMERICAS", "EMEA", "APAC"]
        
        # Create relationships for clients in supported regions
        for client in clients:
            if client["primary_region"] in supported_regions:
                coverage_hours = {
                    "AMERICAS": "8:00-20:00 EST",
                    "EMEA": "8:00-20:00 GMT",
                    "APAC": "8:00-20:00 JST"
                }.get(client["primary_region"], "24/7")
                
                relationships["team_supports_region"].append({
                    "team_id": team["id"],
                    "client_id": client["id"],
                    "coverage_hours": coverage_hours
                })
    
    # Generate DEPLOYED_IN relationships (PlatformComponent -> CloudRegion)
    # Deploy components across multiple regions for redundancy
    for component in platform_components:
        # Core components deployed in all major regions
        if component["tier"] == "core":
            num_regions = random.randint(6, 12)
        else:
            num_regions = random.randint(2, 6)
        
        deployed_regions = random.sample(cloud_regions, num_regions)
        for region in deployed_regions:
            relationships["component_deployed_in"].append({
                "component_id": component["id"],
                "region_id": region["id"]
            })
    
    # Generate USES_COMPONENT relationships (Client -> PlatformComponent)
    for client in clients:
        # All clients use core components
        core_components = [c for c in platform_components if c["tier"] == "core"]
        for component in core_components:
            usage_level = "high" if client["tier"] == "strategic" else random.choice(["low", "medium", "high"])
            relationships["client_uses_component"].append({
                "client_id": client["id"],
                "component_id": component["id"],
                "usage_level": usage_level
            })
        
        # Strategic and enterprise clients use additional components
        if client["tier"] in ["strategic", "enterprise"]:
            supporting_components = [c for c in platform_components if c["tier"] == "supporting"]
            num_supporting = random.randint(2, len(supporting_components))
            for component in random.sample(supporting_components, num_supporting):
                relationships["client_uses_component"].append({
                    "client_id": client["id"],
                    "component_id": component["id"],
                    "usage_level": random.choice(["low", "medium"])
                })
    
    # Generate EXPERT_IN relationships (Person -> PlatformComponent)
    # Engineers and architects have expertise in specific components
    technical_people = [p for p in people if any(role in p["role"] for role in 
                       ["Engineer", "Architect", "Developer", "Scientist", "DevOps", "SRE"])]
    
    for person in technical_people:
        # Number of components they're expert in depends on seniority
        if "Principal" in person["role"] or "Staff" in person["role"]:
            num_expertises = random.randint(3, 6)
        elif "Senior" in person["role"]:
            num_expertises = random.randint(2, 4)
        else:
            num_expertises = random.randint(1, 2)
        
        # Select components based on their role/department
        if "Data" in person["department"]:
            relevant_components = [c for c in platform_components if 
                                 any(word in c["name"] for word in ["Data", "Pipeline", "Lake", "Stream", "Batch"])]
        elif "ML" in person["role"] or "Data Science" in person["department"]:
            relevant_components = [c for c in platform_components if 
                                 any(word in c["name"] for word in ["ML", "Model", "Feature", "Analytics"])]
        elif "Infrastructure" in person["department"] or "DevOps" in person["role"]:
            relevant_components = [c for c in platform_components if 
                                 c["type"] in ["database", "service"] or "Infrastructure" in c["name"]]
        else:
            relevant_components = platform_components
        
        if relevant_components:
            expert_components = random.sample(relevant_components, 
                                           min(num_expertises, len(relevant_components)))
            for component in expert_components:
                # Expertise level based on seniority
                if "Principal" in person["role"] or "Staff" in person["role"]:
                    expertise_level = random.randint(4, 5)
                elif "Senior" in person["role"]:
                    expertise_level = random.randint(3, 4)
                else:
                    expertise_level = random.randint(1, 3)
                
                relationships["person_expert_in"].append({
                    "person_id": person["id"],
                    "component_id": component["id"],
                    "expertise_level": expertise_level
                })
    
    return {
        "people": people,
        "teams": teams,
        "groups": groups,
        "policies": policies,
        "skills": skills,
        "projects": projects,
        "clients": clients,
        "sprints": sprints,
        "offices": offices,
        "languages": languages,
        "holidays": holidays,
        "compliance": compliance_frameworks,
        "data_residency": data_residency_zones,
        "schedules": schedules,
        "incidents": incidents,
        "visas": visas,
        "metrics": metrics,
        "cloud_regions": cloud_regions,
        "platform_components": platform_components,
        "relationships": relationships
    }

def seed_database(falkor_client):
    """Seed the database with test data"""
    print("🌱 Seeding database with test data...")
    
    # Get or create the graph
    db = falkor_client.select_graph("agent_poc")
    
    # Clear existing data
    try:
        db.query("MATCH (n) DETACH DELETE n")
    except:
        pass  # Graph might not exist yet
    
    # Create indexes for better performance
    try:
        db.query("CREATE INDEX ON :Message(timestamp)")
        db.query("CREATE INDEX ON :Person(name)")
        db.query("CREATE INDEX ON :Team(name)")
        db.query("CREATE INDEX ON :Group(name)")
        db.query("CREATE INDEX ON :Policy(name)")
        db.query("CREATE INDEX ON :Skill(name)")
        db.query("CREATE INDEX ON :Project(name)")
        db.query("CREATE INDEX ON :Client(name)")
        db.query("CREATE INDEX ON :Sprint(name)")
        db.query("CREATE INDEX ON :Office(name)")
        db.query("CREATE INDEX ON :Office(region)")
        db.query("CREATE INDEX ON :Office(timezone)")
        db.query("CREATE INDEX ON :Language(code)")
        db.query("CREATE INDEX ON :Language(name)")
        db.query("CREATE INDEX ON :Holiday(date)")
        db.query("CREATE INDEX ON :Holiday(type)")
        db.query("CREATE INDEX ON :Compliance(framework)")
        db.query("CREATE INDEX ON :Compliance(jurisdiction)")
        db.query("CREATE INDEX ON :Compliance(type)")
        db.query("CREATE INDEX ON :Compliance(status)")
        db.query("CREATE INDEX ON :DataResidency(zone)")
        db.query("CREATE INDEX ON :DataResidency(countries)")
        db.query("CREATE INDEX ON :CloudRegion(provider)")
        db.query("CREATE INDEX ON :CloudRegion(region_code)")
        db.query("CREATE INDEX ON :CloudRegion(data_residency_zone)")
        db.query("CREATE INDEX ON :PlatformComponent(name)")
        db.query("CREATE INDEX ON :PlatformComponent(type)")
        db.query("CREATE INDEX ON :PlatformComponent(tier)")
        db.query("CREATE INDEX ON :Schedule(type)")
        db.query("CREATE INDEX ON :Schedule(coverage_type)")
        db.query("CREATE INDEX ON :Schedule(region)")
        db.query("CREATE INDEX ON :Schedule(start_datetime)")
        db.query("CREATE INDEX ON :Incident(severity)")
        db.query("CREATE INDEX ON :Incident(status)")
        db.query("CREATE INDEX ON :Incident(created_at)")
    except:
        pass  # Indexes might already exist
    
    # Generate all data and relationships
    data = generate_relationships()
    
    # Create nodes for people
    for person in data["people"]:
        escaped_name = person['name'].replace("'", "''")
        escaped_role = person['role'].replace("'", "''")
        query = f"""CREATE (p:Person {{
            id: '{person['id']}',
            name: '{escaped_name}',
            email: '{person['email']}',
            department: '{person['department']}',
            role: '{escaped_role}',
            seniority: '{person['seniority']}',
            hire_date: '{person['hire_date']}',
            location: '{person['location']}',
            timezone: '{person['timezone']}',
            capacity_hours_per_week: {person['capacity_hours_per_week']},
            current_utilization: {person['current_utilization']},
            billing_rate: {person['billing_rate']},
            years_experience: {person['years_experience']},
            manager_id: '{person.get('manager_id', '')}'
        }})"""
        db.query(query)
    
    # Create nodes for teams
    for team in data["teams"]:
        escaped_name = team['name'].replace("'", "''")
        escaped_focus = team['focus'].replace("'", "''")
        query = f"""CREATE (t:Team {{
            id: '{team['id']}',
            name: '{escaped_name}',
            department: '{team['department']}',
            focus: '{escaped_focus}'
        }})"""
        db.query(query)
    
    # Create nodes for groups
    for group in data["groups"]:
        escaped_name = group['name'].replace("'", "''")
        escaped_description = group['description'].replace("'", "''")
        query = f"""CREATE (g:Group {{
            id: '{group['id']}',
            name: '{escaped_name}',
            description: '{escaped_description}',
            type: '{group['type']}',
            lead_department: '{group['lead_department']}'
        }})"""
        db.query(query)
    
    # Create nodes for policies
    for policy in data["policies"]:
        frameworks = ','.join(policy['compliance_frameworks'])
        escaped_name = policy['name'].replace("'", "''")
        escaped_description = policy['description'].replace("'", "''")
        query = f"""CREATE (p:Policy {{
            id: '{policy['id']}',
            name: '{escaped_name}',
            description: '{escaped_description}',
            category: '{policy['category']}',
            severity: '{policy['severity']}',
            responsible_type: '{policy['responsible_type']}',
            compliance_frameworks: '{frameworks}'
        }})"""
        db.query(query)
    
    # Create nodes for skills
    for skill in data["skills"]:
        escaped_name = skill['name'].replace("'", "''")
        query = f"""CREATE (s:Skill {{
            id: '{skill['id']}',
            name: '{escaped_name}',
            category: '{skill['category']}',
            type: '{skill['type']}'
        }})"""
        db.query(query)
    
    # Create nodes for clients
    for client in data["clients"]:
        escaped_name = client['name'].replace("'", "''")
        # Convert time_zone_preferences list to string
        time_zones_str = ','.join(client['time_zone_preferences'])
        query = f"""CREATE (c:Client {{
            id: '{client['id']}',
            name: '{escaped_name}',
            industry: '{client['industry']}',
            tier: '{client['tier']}',
            annual_value: {client['annual_value']},
            mrr: {client['mrr']},
            data_volume_gb: {client['data_volume_gb']},
            active_users: {client['active_users']},
            support_tier: '{client['support_tier']}',
            primary_region: '{client['primary_region']}',
            time_zone_preferences: '{time_zones_str}',
            relationship_start: '{client['relationship_start']}'
        }})"""
        db.query(query)
    
    # Create nodes for projects
    for project in data["projects"]:
        escaped_name = project['name'].replace("'", "''")
        escaped_description = project['description'].replace("'", "''")
        query = f"""CREATE (pr:Project {{
            id: '{project['id']}',
            name: '{escaped_name}',
            type: '{project['type']}',
            status: '{project['status']}',
            start_date: '{project['start_date']}',
            end_date: '{project['end_date']}',
            budget: {project['budget']},
            priority: '{project['priority']}',
            client_id: '{project['client_id']}',
            description: '{escaped_description}'
        }})"""
        db.query(query)
    
    # Create nodes for sprints
    for sprint in data["sprints"]:
        escaped_name = sprint['name'].replace("'", "''")
        velocity = sprint['velocity'] if sprint['velocity'] is not None else 0
        query = f"""CREATE (s:Sprint {{
            id: '{sprint['id']}',
            name: '{escaped_name}',
            project_id: '{sprint['project_id']}',
            sprint_number: {sprint['sprint_number']},
            start_date: '{sprint['start_date']}',
            end_date: '{sprint['end_date']}',
            status: '{sprint['status']}',
            velocity: {velocity}
        }})"""
        db.query(query)
    
    # Create nodes for cloud regions
    for region in data["cloud_regions"]:
        escaped_region_name = region['region_name'].replace("'", "''")
        query = f"""CREATE (cr:CloudRegion {{
            id: '{region['id']}',
            provider: '{region['provider']}',
            region_code: '{region['region_code']}',
            region_name: '{escaped_region_name}',
            availability_zones: {region['availability_zones']},
            data_residency_zone: '{region['data_residency_zone']}'
        }})"""
        db.query(query)
    
    # Create nodes for platform components
    for component in data["platform_components"]:
        escaped_name = component['name'].replace("'", "''")
        query = f"""CREATE (pc:PlatformComponent {{
            id: '{component['id']}',
            name: '{escaped_name}',
            type: '{component['type']}',
            tier: '{component['tier']}',
            owner_team_id: '{component['owner_team_id']}',
            documentation_url: '{component['documentation_url']}'
        }})"""
        db.query(query)
    
    # Create nodes for offices
    for office in data["offices"]:
        escaped_name = office['name'].replace("'", "''")
        escaped_city = office['city'].replace("'", "''")
        escaped_country = office['country'].replace("'", "''")
        languages_str = ','.join(office['languages'])
        query = f"""CREATE (o:Office {{
            id: '{office['id']}',
            name: '{escaped_name}',
            city: '{escaped_city}',
            country: '{escaped_country}',
            country_code: '{office['country_code']}',
            region: '{office['region']}',
            timezone: '{office['timezone']}',
            timezone_offset: {office['timezone_offset']},
            business_hours_start: '{office['business_hours_start']}',
            business_hours_end: '{office['business_hours_end']}',
            business_hours_start_utc: '{office['business_hours_start_utc']}',
            business_hours_end_utc: '{office['business_hours_end_utc']}',
            languages: '{languages_str}',
            currency: '{office['currency']}',
            data_residency_zone: '{office['data_residency_zone']}',
            is_headquarters: {str(office['is_headquarters']).lower()},
            established_date: '{office['established_date']}'
        }})"""
        db.query(query)
    
    # Create nodes for languages
    for language in data["languages"]:
        escaped_name = language['name'].replace("'", "''")
        escaped_native_name = language['native_name'].replace("'", "''")
        query = f"""CREATE (l:Language {{
            id: '{language['id']}',
            code: '{language['code']}',
            name: '{escaped_name}',
            native_name: '{escaped_native_name}',
            script: '{language['script']}',
            direction: '{language['direction']}',
            is_business_language: {str(language['is_business_language']).lower()}
        }})"""
        db.query(query)
    
    # Create nodes for holidays
    for holiday in data["holidays"]:
        # Try to escape apostrophes for FalkorDB
        escaped_name = holiday['name'].replace("'", "\\'")
        offices_str = ','.join(holiday['offices'])
        query = f"CREATE (h:Holiday {{"
        query += f"id: '{holiday['id']}', "
        query += f'name: "{escaped_name}", '  # Using double quotes for name
        query += f"date: '{holiday['date']}', "
        query += f"type: '{holiday['type']}', "
        query += f"recurring: {str(holiday['recurring']).lower()}, "
        query += f"offices: '{offices_str}', "
        query += f"impact: '{holiday['impact']}', "
        query += f"coverage_required: {str(holiday['coverage_required']).lower()}"
        query += "})"
        db.query(query)
    
    # Create nodes for compliance frameworks
    for compliance in data["compliance"]:
        escaped_framework = compliance['framework'].replace("'", "''")
        escaped_jurisdiction = compliance['jurisdiction'].replace("'", "''")
        geographic_scope_str = ','.join(compliance['geographic_scope'])
        requirements_json = json.dumps(compliance['requirements']).replace("'", "''")
        penalties_json = json.dumps(compliance['penalties']).replace("'", "''")
        
        query = f"""CREATE (c:Compliance {{
            id: '{compliance['id']}',
            framework: '{escaped_framework}',
            version: '{compliance['version']}',
            jurisdiction: '{escaped_jurisdiction}',
            geographic_scope: '{geographic_scope_str}',
            type: '{compliance['type']}',
            requirements: '{requirements_json}',
            penalties: '{penalties_json}',
            effective_date: '{compliance['effective_date']}',
            last_updated: '{compliance['last_updated']}',
            status: '{compliance['status']}'
        }})"""
        db.query(query)
    
    # Create nodes for data residency zones
    for dr_zone in data["data_residency"]:
        countries_str = ','.join(dr_zone['countries'])
        regulations_str = ','.join(dr_zone['regulations'])
        storage_locations_str = ','.join(dr_zone['storage_locations'])
        transfer_restrictions_json = json.dumps(dr_zone['transfer_restrictions']).replace("'", "''")
        
        query = f"""CREATE (dr:DataResidency {{
            id: '{dr_zone['id']}',
            zone: '{dr_zone['zone']}',
            countries: '{countries_str}',
            regulations: '{regulations_str}',
            storage_locations: '{storage_locations_str}',
            transfer_restrictions: '{transfer_restrictions_json}',
            encryption_required: {str(dr_zone['encryption_required']).lower()}
        }})"""
        db.query(query)
    
    # Create nodes for schedules
    for schedule in data["schedules"]:
        office_id_str = f"'{schedule['office_id']}'" if schedule.get('office_id') else 'null'
        severity_focus_str = f", severity_focus: '{schedule['severity_focus']}'" if schedule.get('severity_focus') else ""
        
        query = f"""CREATE (s:Schedule {{
            id: '{schedule['id']}',
            type: '{schedule['type']}',
            timezone: '{schedule['timezone']}',
            start_datetime: '{schedule['start_datetime']}',
            end_datetime: '{schedule['end_datetime']}',
            recurring_pattern: '{schedule['recurring_pattern']}',
            coverage_type: '{schedule['coverage_type']}',
            office_id: {office_id_str},
            region: '{schedule['region']}'{severity_focus_str}
        }})"""
        db.query(query)
    
    # Create nodes for incidents
    for incident in data["incidents"]:
        regions_str = ','.join(incident['affected_regions'])
        services_str = ','.join(incident['affected_services'])
        escaped_desc = incident['description'].replace("'", "''")
        resolved_at_str = f"'{incident['resolved_at']}'" if incident['resolved_at'] else 'null'
        mttr_str = incident['mttr_minutes'] if incident['mttr_minutes'] else 'null'
        root_cause_str = f", root_cause: '{incident['root_cause']}'" if incident.get('root_cause') else ""
        
        query = f"""CREATE (i:Incident {{
            id: '{incident['id']}',
            severity: '{incident['severity']}',
            status: '{incident['status']}',
            description: '{escaped_desc}',
            affected_regions: '{regions_str}',
            affected_services: '{services_str}',
            created_at: '{incident['created_at']}',
            resolved_at: {resolved_at_str},
            mttr_minutes: {mttr_str}{root_cause_str}
        }})"""
        db.query(query)
    
    # Create nodes for visas
    for visa in data["visas"]:
        escaped_name = visa['name'].replace("'", "''")
        restrictions_str = ','.join(visa['restrictions'])
        
        query = f"""CREATE (v:Visa {{
            id: '{visa['id']}',
            type: '{visa['type']}',
            name: '{escaped_name}',
            country: '{visa['country']}',
            issued_date: '{visa['issued_date']}',
            expiry_date: '{visa['expiry_date']}',
            restrictions: '{restrictions_str}',
            allows_client_site: {str(visa['allows_client_site']).lower()},
            max_duration_years: {visa['max_duration_years']},
            renewable: {str(visa['renewable']).lower()}
        }})"""
        db.query(query)
    
    # Create nodes for metrics
    for metric in data["metrics"]:
        query = f"""CREATE (m:Metric {{
            id: '{metric['id']}',
            type: '{metric['type']}',
            service: '{metric['service']}',
            region: '{metric['region']}',
            value: {metric['value']},
            unit: '{metric['unit']}',
            timestamp: '{metric['timestamp']}',
            percentile: {metric['percentile']}
        }})"""
        db.query(query)
    
    # Create relationships for person-team memberships
    for membership in data["relationships"]["person_team_memberships"]:
        escaped_role = membership['role'].replace("'", "''")
        query = f"""MATCH (p:Person {{id: '{membership['person_id']}'}}), (t:Team {{id: '{membership['team_id']}'}}) 
                   CREATE (p)-[:MEMBER_OF {{role: '{escaped_role}', is_lead: {str(membership['is_lead']).lower()}}}]->(t)"""
        db.query(query)
    
    # Create relationships for person-group memberships
    for membership in data["relationships"]["person_group_memberships"]:
        query = f"""MATCH (p:Person {{id: '{membership['person_id']}'}}), (g:Group {{id: '{membership['group_id']}'}}) 
                   CREATE (p)-[:MEMBER_OF {{role: '{membership['role']}', joined_date: '{membership['joined_date']}'}}
                   ]->(g)"""
        db.query(query)
    
    # Create relationships for team-policy responsibilities
    for responsibility in data["relationships"]["team_policy_responsibilities"]:
        query = f"""MATCH (t:Team {{id: '{responsibility['team_id']}'}}), (p:Policy {{id: '{responsibility['policy_id']}'}}) 
                   CREATE (t)-[:RESPONSIBLE_FOR {{responsibility_type: '{responsibility['responsibility_type']}', assigned_date: '{responsibility['assigned_date']}'}}
                   ]->(p)"""
        db.query(query)
    
    # Create relationships for group-policy responsibilities
    for responsibility in data["relationships"]["group_policy_responsibilities"]:
        query = f"""MATCH (g:Group {{id: '{responsibility['group_id']}'}}), (p:Policy {{id: '{responsibility['policy_id']}'}}) 
                   CREATE (g)-[:RESPONSIBLE_FOR {{responsibility_type: '{responsibility['responsibility_type']}', assigned_date: '{responsibility['assigned_date']}'}}
                   ]->(p)"""
        db.query(query)
    
    # Create manager relationships
    for person in data["people"]:
        if person.get('manager_id'):
            query = f"""MATCH (p:Person {{id: '{person['id']}'}}), (m:Person {{id: '{person['manager_id']}'}}) 
                       CREATE (p)-[:REPORTS_TO]->(m)"""
            db.query(query)
    
    # Create person-skill relationships
    for skill_rel in data["relationships"]["person_skills"]:
        query = f"""MATCH (p:Person {{id: '{skill_rel['person_id']}'}}), (s:Skill {{id: '{skill_rel['skill_id']}'}}) 
                   CREATE (p)-[:HAS_SKILL {{
                       proficiency_level: '{skill_rel['proficiency_level']}',
                       years_experience: {skill_rel['years_experience']},
                       last_used: '{skill_rel['last_used']}'
                   }}]->(s)"""
        db.query(query)
    
    # Create person-project allocations
    for allocation in data["relationships"]["person_project_allocations"]:
        query = f"""MATCH (p:Person {{id: '{allocation['person_id']}'}}), (pr:Project {{id: '{allocation['project_id']}'}}) 
                   CREATE (p)-[:ALLOCATED_TO {{
                       allocation_percentage: {allocation['allocation_percentage']},
                       start_date: '{allocation['start_date']}',
                       end_date: '{allocation['end_date']}',
                       role_on_project: '{allocation['role_on_project']}'
                   }}]->(pr)"""
        db.query(query)
    
    # Create project-skill requirements
    for req in data["relationships"]["project_skill_requirements"]:
        query = f"""MATCH (pr:Project {{id: '{req['project_id']}'}}), (s:Skill {{id: '{req['skill_id']}'}}) 
                   CREATE (pr)-[:REQUIRES_SKILL {{
                       priority: '{req['priority']}',
                       min_proficiency_level: '{req['min_proficiency_level']}',
                       headcount_needed: {req['headcount_needed']}
                   }}]->(s)"""
        db.query(query)
    
    # Create team-project delivery relationships
    for delivery in data["relationships"]["team_project_delivery"]:
        query = f"""MATCH (t:Team {{id: '{delivery['team_id']}'}}), (pr:Project {{id: '{delivery['project_id']}'}}) 
                   CREATE (t)-[:DELIVERS {{
                       responsibility: '{delivery['responsibility']}',
                       committed_capacity: {delivery['committed_capacity']}
                   }}]->(pr)"""
        db.query(query)
    
    # Create mentorship relationships
    for mentorship in data["relationships"]["person_mentorships"]:
        query = f"""MATCH (mentor:Person {{id: '{mentorship['mentor_id']}'}}), (mentee:Person {{id: '{mentorship['mentee_id']}'}}) 
                   CREATE (mentee)-[:MENTORED_BY {{
                       start_date: '{mentorship['start_date']}',
                       focus_area: '{mentorship['focus_area']}'
                   }}]->(mentor)"""
        db.query(query)
    
    # Create backup relationships
    for backup in data["relationships"]["person_backups"]:
        query = f"""MATCH (primary:Person {{id: '{backup['primary_person_id']}'}}), (backup:Person {{id: '{backup['backup_person_id']}'}}) 
                   CREATE (backup)-[:BACKUP_FOR {{
                       coverage_type: '{backup['coverage_type']}',
                       readiness_level: '{backup['readiness_level']}'
                   }}]->(primary)"""
        db.query(query)
    
    # Create specialization relationships  
    for spec in data["relationships"]["person_specializations"]:
        # Create Technology nodes on the fly for specializations
        escaped_spec = spec['specialization'].replace("'", "''")
        query = f"""MERGE (tech:Technology {{name: '{escaped_spec}'}})"""
        db.query(query)
        
        query = f"""MATCH (p:Person {{id: '{spec['person_id']}'}}), (tech:Technology {{name: '{escaped_spec}'}}) 
                   CREATE (p)-[:SPECIALIZES_IN {{
                       expertise_level: '{spec['expertise_level']}',
                       years_in_specialty: {spec['years_in_specialty']}
                   }}]->(tech)"""
        db.query(query)
    
    # Create project-client relationships
    for project in data["projects"]:
        query = f"""MATCH (pr:Project {{id: '{project['id']}'}}), (c:Client {{id: '{project['client_id']}'}}) 
                   CREATE (pr)-[:FOR_CLIENT]->(c)"""
        db.query(query)
    
    # Create sprint-project relationships
    for sprint in data["sprints"]:
        query = f"""MATCH (s:Sprint {{id: '{sprint['id']}'}}), (pr:Project {{id: '{sprint['project_id']}'}}) 
                   CREATE (s)-[:PART_OF]->(pr)"""
        db.query(query)
    
    # Create person-office relationships
    for assignment in data["relationships"]["person_office_assignments"]:
        desk_location = f", desk_location: '{assignment['desk_location']}'" if assignment['desk_location'] else ""
        query = f"""MATCH (p:Person {{id: '{assignment['person_id']}'}}), (o:Office {{id: '{assignment['office_id']}'}}) 
                   CREATE (p)-[:WORKS_AT {{
                       start_date: '{assignment['start_date']}',
                       is_remote: {str(assignment['is_remote']).lower()}{desk_location}
                   }}]->(o)"""
        db.query(query)
    
    # Create person-language relationships
    for lang_rel in data["relationships"]["person_languages"]:
        cert_date = f", certification_date: '{lang_rel['certification_date']}'" if lang_rel['certification_date'] else ""
        query = f"""MATCH (p:Person {{id: '{lang_rel['person_id']}'}}), (l:Language {{id: '{lang_rel['language_id']}'}}) 
                   CREATE (p)-[:SPEAKS {{
                       proficiency: '{lang_rel['proficiency']}',
                       is_primary: {str(lang_rel['is_primary']).lower()},
                       certified: {str(lang_rel['certified']).lower()}{cert_date}
                   }}]->(l)"""
        db.query(query)
    
    # Create holiday-office relationships
    for holiday in data["holidays"]:
        for office_id in holiday["offices"]:
            query = f"""MATCH (h:Holiday {{id: '{holiday['id']}'}}), (o:Office {{id: '{office_id}'}}) 
                       CREATE (h)-[:OBSERVED_BY]->(o)"""
            db.query(query)
    
    # Create office collaboration relationships
    for collab in data["relationships"]["office_collaborations"]:
        meeting_times_str = ','.join(collab['preferred_meeting_times'])
        query = f"""MATCH (o1:Office {{id: '{collab['office1_id']}'}}), (o2:Office {{id: '{collab['office2_id']}'}}) 
                   CREATE (o1)-[:COLLABORATES_WITH {{
                       overlap_hours: {collab['overlap_hours']},
                       preferred_meeting_times: '{meeting_times_str}'
                   }}]->(o2)"""
        db.query(query)
    
    # Create office-compliance relationships
    for office_comp in data["relationships"]["office_compliance"]:
        query = f"""MATCH (o:Office {{id: '{office_comp['office_id']}'}}), (c:Compliance {{id: '{office_comp['compliance_id']}'}}) 
                   CREATE (o)-[:OPERATES_UNDER {{
                       since: '{office_comp['since']}',
                       attestation_date: '{office_comp['attestation_date']}',
                       next_audit: '{office_comp['next_audit']}'
                   }}]->(c)"""
        db.query(query)
    
    # Create client-compliance relationships
    for client_comp in data["relationships"]["client_compliance"]:
        query = f"""MATCH (cl:Client {{id: '{client_comp['client_id']}'}}), (c:Compliance {{id: '{client_comp['compliance_id']}'}}) 
                   CREATE (cl)-[:REQUIRES_COMPLIANCE {{
                       contractual: {str(client_comp['contractual']).lower()},
                       sla_impact: '{client_comp['sla_impact']}'
                   }}]->(c)"""
        db.query(query)
    
    # Create office-data residency relationships
    for office_dr in data["relationships"]["office_data_residency"]:
        query = f"""MATCH (o:Office {{id: '{office_dr['office_id']}'}}), (dr:DataResidency {{id: '{office_dr['data_residency_id']}'}}) 
                   CREATE (o)-[:ENFORCES]->(dr)"""
        db.query(query)
    
    # Create project-data residency relationships
    for proj_dr in data["relationships"]["project_data_residency"]:
        query = f"""MATCH (p:Project {{id: '{proj_dr['project_id']}'}}), (dr:DataResidency {{id: '{proj_dr['data_residency_id']}'}}) 
                   CREATE (p)-[:STORES_DATA_IN]->(dr)"""
        db.query(query)
    
    # Create ON_CALL relationships
    for on_call in data["relationships"]["person_on_call"]:
        query = f"""MATCH (p:Person {{id: '{on_call['person_id']}'}}), (s:Schedule {{id: '{on_call['schedule_id']}'}}) 
                   CREATE (p)-[:ON_CALL {{
                       role: '{on_call['role']}',
                       reachable_via: '{on_call['reachable_via']}'
                   }}]->(s)"""
        db.query(query)
    
    # Create RESPONDED_TO relationships
    for response in data["relationships"]["person_incident_response"]:
        query = f"""MATCH (p:Person {{id: '{response['person_id']}'}}), (i:Incident {{id: '{response['incident_id']}'}}) 
                   CREATE (p)-[:RESPONDED_TO {{
                       response_time_minutes: {response['response_time_minutes']},
                       role: '{response['role']}'
                   }}]->(i)"""
        db.query(query)
    
    # Create HANDS_OFF_TO relationships
    for handoff in data["relationships"]["team_handoffs"]:
        query = f"""MATCH (t1:Team {{id: '{handoff['from_team_id']}'}}), (t2:Team {{id: '{handoff['to_team_id']}'}}) 
                   CREATE (t1)-[:HANDS_OFF_TO {{
                       handoff_time: '{handoff['handoff_time']}',
                       handoff_type: '{handoff['handoff_type']}'
                   }}]->(t2)"""
        db.query(query)
    
    # Create HAS_VISA relationships
    for visa_rel in data["relationships"]["person_visas"]:
        query = f"""MATCH (p:Person {{id: '{visa_rel['person_id']}'}}), (v:Visa {{id: '{visa_rel['visa_id']}'}}) 
                   CREATE (p)-[:HAS_VISA {{
                       status: '{visa_rel['status']}',
                       sponsor: '{visa_rel['sponsor']}'
                   }}]->(v)"""
        db.query(query)
    
    # Create SUPPORTS_REGION relationships (Team -> Client)
    for support_rel in data["relationships"]["team_supports_region"]:
        query = f"""MATCH (t:Team {{id: '{support_rel['team_id']}'}}), (c:Client {{id: '{support_rel['client_id']}'}}) 
                   CREATE (t)-[:SUPPORTS_REGION {{
                       coverage_hours: '{support_rel['coverage_hours']}'
                   }}]->(c)"""
        db.query(query)
    
    # Create DEPLOYED_IN relationships (PlatformComponent -> CloudRegion)
    for deploy_rel in data["relationships"]["component_deployed_in"]:
        query = f"""MATCH (pc:PlatformComponent {{id: '{deploy_rel['component_id']}'}}), (cr:CloudRegion {{id: '{deploy_rel['region_id']}'}}) 
                   CREATE (pc)-[:DEPLOYED_IN]->(cr)"""
        db.query(query)
    
    # Create USES_COMPONENT relationships (Client -> PlatformComponent)
    for uses_rel in data["relationships"]["client_uses_component"]:
        query = f"""MATCH (c:Client {{id: '{uses_rel['client_id']}'}}), (pc:PlatformComponent {{id: '{uses_rel['component_id']}'}}) 
                   CREATE (c)-[:USES_COMPONENT {{
                       usage_level: '{uses_rel['usage_level']}'
                   }}]->(pc)"""
        db.query(query)
    
    # Create EXPERT_IN relationships (Person -> PlatformComponent)
    for expert_rel in data["relationships"]["person_expert_in"]:
        query = f"""MATCH (p:Person {{id: '{expert_rel['person_id']}'}}), (pc:PlatformComponent {{id: '{expert_rel['component_id']}'}}) 
                   CREATE (p)-[:EXPERT_IN {{
                       expertise_level: {expert_rel['expertise_level']}
                   }}]->(pc)"""
        db.query(query)
    
    # Store summary statistics as a node
    stats = {
        "people_count": len(data["people"]),
        "teams_count": len(data["teams"]),
        "groups_count": len(data["groups"]),
        "policies_count": len(data["policies"]),
        "skills_count": len(data["skills"]),
        "projects_count": len(data["projects"]),
        "clients_count": len(data["clients"]),
        "sprints_count": len(data["sprints"]),
        "offices_count": len(data["offices"]),
        "languages_count": len(data["languages"]),
        "holidays_count": len(data["holidays"]),
        "compliance_count": len(data["compliance"]),
        "data_residency_count": len(data["data_residency"]),
        "schedules_count": len(data["schedules"]),
        "incidents_count": len(data["incidents"]),
        "visas_count": len(data["visas"]),
        "metrics_count": len(data["metrics"]),
        "cloud_regions_count": len(data["cloud_regions"]),
        "platform_components_count": len(data["platform_components"]),
        "seeded_at": datetime.now().isoformat()
    }
    
    query = f"""CREATE (s:SeedStats {{
        people_count: {stats['people_count']},
        teams_count: {stats['teams_count']},
        groups_count: {stats['groups_count']},
        policies_count: {stats['policies_count']},
        skills_count: {stats['skills_count']},
        projects_count: {stats['projects_count']},
        clients_count: {stats['clients_count']},
        sprints_count: {stats['sprints_count']},
        offices_count: {stats['offices_count']},
        languages_count: {stats['languages_count']},
        holidays_count: {stats['holidays_count']},
        compliance_count: {stats['compliance_count']},
        data_residency_count: {stats['data_residency_count']},
        schedules_count: {stats['schedules_count']},
        incidents_count: {stats['incidents_count']},
        visas_count: {stats['visas_count']},
        metrics_count: {stats['metrics_count']},
        cloud_regions_count: {stats['cloud_regions_count']},
        platform_components_count: {stats['platform_components_count']},
        seeded_at: '{stats['seeded_at']}'
    }})"""
    db.query(query)
    
    print(f"✅ Seeded {stats['people_count']} people, {stats['teams_count']} teams, {stats['groups_count']} groups, {stats['policies_count']} policies")
    print(f"✅ Added {stats['skills_count']} skills, {stats['projects_count']} projects, {stats['clients_count']} clients, {stats['sprints_count']} sprints")
    print(f"✅ Added {stats['offices_count']} offices, {stats['languages_count']} languages, {stats['holidays_count']} holidays")
    print(f"✅ Added {stats['compliance_count']} compliance frameworks, {stats['data_residency_count']} data residency zones")
    print(f"✅ Added {stats['schedules_count']} schedules, {stats['incidents_count']} incidents")
    print(f"✅ Added {stats['visas_count']} visas, {stats['metrics_count']} performance metrics")
    print(f"✅ Added {stats['cloud_regions_count']} cloud regions, {stats['platform_components_count']} platform components")
    print(f"✅ Created {len(data['relationships']['person_team_memberships'])} team memberships")
    print(f"✅ Created {len(data['relationships']['person_group_memberships'])} group memberships") 
    print(f"✅ Created {len(data['relationships']['team_policy_responsibilities'])} team policy responsibilities")
    print(f"✅ Created {len(data['relationships']['group_policy_responsibilities'])} group policy responsibilities")
    print(f"✅ Created {len(data['relationships']['person_skills'])} person-skill relationships")
    print(f"✅ Created {len(data['relationships']['person_project_allocations'])} project allocations")
    print(f"✅ Created {len(data['relationships']['project_skill_requirements'])} project skill requirements")
    print(f"✅ Created {len(data['relationships']['person_mentorships'])} mentorship relationships")
    print(f"✅ Created {len(data['relationships']['person_backups'])} backup relationships")
    print(f"✅ Created {len(data['relationships']['person_office_assignments'])} office assignments")
    print(f"✅ Created {len(data['relationships']['person_languages'])} language skills")
    print(f"✅ Created {len(data['relationships']['office_collaborations'])} office collaborations")
    print(f"✅ Created {len(data['compliance'])} compliance frameworks")
    print(f"✅ Created {len(data['data_residency'])} data residency zones")
    print(f"✅ Created {len(data['relationships']['office_compliance'])} office-compliance relationships")
    print(f"✅ Created {len(data['relationships']['client_compliance'])} client-compliance requirements")
    print(f"✅ Created {len(data['relationships']['office_data_residency'])} office-data residency assignments")
    print(f"✅ Created {len(data['relationships']['project_data_residency'])} project-data residency assignments")
    print(f"✅ Created {len(data['relationships']['person_on_call'])} on-call assignments")
    print(f"✅ Created {len(data['relationships']['person_incident_response'])} incident responses")
    print(f"✅ Created {len(data['relationships']['team_handoffs'])} team handoff relationships")
    print(f"✅ Created {len(data['relationships']['person_visas'])} person-visa relationships")
    print(f"✅ Created {len(data['relationships']['team_supports_region'])} team-supports-region relationships")
    print(f"✅ Created {len(data['relationships']['component_deployed_in'])} component-deployed-in relationships")
    print(f"✅ Created {len(data['relationships']['client_uses_component'])} client-uses-component relationships")
    print(f"✅ Created {len(data['relationships']['person_expert_in'])} person-expert-in relationships")
    
    return data

if __name__ == "__main__":
    # Initialize FalkorDB client
    try:
        falkor_host = os.getenv("FALKOR_HOST", "localhost")
        falkor_port = int(os.getenv("FALKOR_PORT", 6379))
        
        print(f"🔌 Connecting to FalkorDB at {falkor_host}:{falkor_port}...")
        client = falkordb.FalkorDB(host=falkor_host, port=falkor_port)
        
        # Run the seed function
        seed_database(client)
        
        print("✅ Database seeding completed successfully!")
        
    except Exception as e:
        print(f"❌ Error seeding database: {e}")
        import traceback
        traceback.print_exc()