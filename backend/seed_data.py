import json
import falkordb
from faker import Faker
import random
from datetime import datetime, timedelta

fake = Faker()

def generate_people_data():
    """Generate realistic people data for a B2B data analytics platform company"""
    people = []
    departments = [
        "Data Platform Engineering", "Analytics Engineering", "Product", "Data Science", 
        "Infrastructure & DevOps", "Security & Compliance", "Customer Success", 
        "Professional Services", "Sales", "Marketing", "Finance", "Legal", 
        "People Operations", "Engineering", "Solutions Architecture"
    ]
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
        
        person = {
            "id": f"person_{i+1}",
            "name": full_name,
            "email": email,
            "department": dept,
            "role": random.choice(roles[dept]),
            "hire_date": fake.date_between(start_date='-3y', end_date='today').isoformat(),
            "location": random.choice([
                "San Francisco", "New York", "Austin", "Remote", "Seattle", "Boston", 
                "Chicago", "Los Angeles", "Denver", "Atlanta", "Portland", "Miami",
                "Toronto", "London", "Berlin", "Singapore", "Sydney"
            ]),
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
    
    relationships = {
        "person_team_memberships": [],
        "person_group_memberships": [],
        "team_policy_responsibilities": [],
        "group_policy_responsibilities": []
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
    
    return {
        "people": people,
        "teams": teams,
        "groups": groups,
        "policies": policies,
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
            hire_date: '{person['hire_date']}',
            location: '{person['location']}',
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
    
    # Store summary statistics as a node
    stats = {
        "people_count": len(data["people"]),
        "teams_count": len(data["teams"]),
        "groups_count": len(data["groups"]),
        "policies_count": len(data["policies"]),
        "seeded_at": datetime.now().isoformat()
    }
    
    query = f"""CREATE (s:SeedStats {{
        people_count: {stats['people_count']},
        teams_count: {stats['teams_count']},
        groups_count: {stats['groups_count']},
        policies_count: {stats['policies_count']},
        seeded_at: '{stats['seeded_at']}'
    }})"""
    db.query(query)
    
    print(f"✅ Seeded {stats['people_count']} people, {stats['teams_count']} teams, {stats['groups_count']} groups, {stats['policies_count']} policies")
    print(f"✅ Created {len(data['relationships']['person_team_memberships'])} team memberships")
    print(f"✅ Created {len(data['relationships']['person_group_memberships'])} group memberships") 
    print(f"✅ Created {len(data['relationships']['team_policy_responsibilities'])} team policy responsibilities")
    print(f"✅ Created {len(data['relationships']['group_policy_responsibilities'])} group policy responsibilities")
    
    return data