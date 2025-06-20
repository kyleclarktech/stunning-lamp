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
        {"name": "Data Lake Modernization", "type": "infrastructure", "client_id": "client_1"},
        {"name": "Real-time Analytics Platform", "type": "platform", "client_id": "client_2"},
        {"name": "ML Pipeline Implementation", "type": "ml", "client_id": "client_3"},
        {"name": "Customer 360 Data Platform", "type": "analytics", "client_id": "client_4"},
        {"name": "Cost Optimization Initiative", "type": "optimization", "client_id": "client_5"},
        {"name": "Data Governance Framework", "type": "governance", "client_id": "client_6"},
        {"name": "Multi-Cloud Migration", "type": "infrastructure", "client_id": "client_7"},
        {"name": "Streaming Data Pipeline", "type": "platform", "client_id": "client_8"},
        {"name": "Self-Service Analytics Portal", "type": "analytics", "client_id": "client_9"},
        {"name": "API Platform v2.0", "type": "platform", "client_id": "client_10"},
        {"name": "Security Compliance Audit", "type": "governance", "client_id": "client_11"},
        {"name": "Performance Optimization Sprint", "type": "optimization", "client_id": "client_12"}
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
    """Generate client data"""
    clients = []
    client_names = [
        "Acme Financial Services", "Global Retail Corp", "HealthTech Solutions",
        "Manufacturing Industries", "Telecomm Giant", "E-commerce Leader",
        "Media Conglomerate", "Energy Corporation", "Pharma Innovations",
        "Logistics Network", "Insurance Group", "Banking Consortium"
    ]
    
    for i, name in enumerate(client_names):
        client = {
            "id": f"client_{i+1}",
            "name": name,
            "industry": random.choice(["Financial Services", "Retail", "Healthcare", "Manufacturing", "Telecom", "E-commerce", "Media", "Energy", "Pharmaceutical", "Logistics", "Insurance"]),
            "tier": random.choice(["enterprise", "mid-market", "strategic"]),
            "annual_value": random.randint(500000, 5000000),
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
        "person_specializations": []
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
    
    return {
        "people": people,
        "teams": teams,
        "groups": groups,
        "policies": policies,
        "skills": skills,
        "projects": projects,
        "clients": clients,
        "sprints": sprints,
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
        query = f"""CREATE (c:Client {{
            id: '{client['id']}',
            name: '{escaped_name}',
            industry: '{client['industry']}',
            tier: '{client['tier']}',
            annual_value: {client['annual_value']},
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
        seeded_at: '{stats['seeded_at']}'
    }})"""
    db.query(query)
    
    print(f"✅ Seeded {stats['people_count']} people, {stats['teams_count']} teams, {stats['groups_count']} groups, {stats['policies_count']} policies")
    print(f"✅ Added {stats['skills_count']} skills, {stats['projects_count']} projects, {stats['clients_count']} clients, {stats['sprints_count']} sprints")
    print(f"✅ Created {len(data['relationships']['person_team_memberships'])} team memberships")
    print(f"✅ Created {len(data['relationships']['person_group_memberships'])} group memberships") 
    print(f"✅ Created {len(data['relationships']['team_policy_responsibilities'])} team policy responsibilities")
    print(f"✅ Created {len(data['relationships']['group_policy_responsibilities'])} group policy responsibilities")
    print(f"✅ Created {len(data['relationships']['person_skills'])} person-skill relationships")
    print(f"✅ Created {len(data['relationships']['person_project_allocations'])} project allocations")
    print(f"✅ Created {len(data['relationships']['project_skill_requirements'])} project skill requirements")
    print(f"✅ Created {len(data['relationships']['person_mentorships'])} mentorship relationships")
    print(f"✅ Created {len(data['relationships']['person_backups'])} backup relationships")
    
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