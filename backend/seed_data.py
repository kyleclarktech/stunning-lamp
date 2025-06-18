import json
import falkordb
from faker import Faker
import random
from datetime import datetime, timedelta

fake = Faker()

def generate_people_data():
    """Generate realistic people data"""
    people = []
    departments = [
        "Engineering", "Product", "Design", "Data Science", "DevOps", "Security", 
        "Marketing", "Sales", "HR", "Finance", "Legal", "Operations", "Customer Success",
        "Quality Assurance", "Research", "Business Development"
    ]
    roles = {
        "Engineering": [
            "Junior Software Engineer", "Software Engineer", "Senior Software Engineer", 
            "Staff Engineer", "Principal Engineer", "Engineering Manager", "Senior Engineering Manager",
            "Director of Engineering", "VP of Engineering", "Frontend Engineer", "Backend Engineer",
            "Full Stack Engineer", "Mobile Engineer", "Platform Engineer"
        ],
        "Product": [
            "Associate Product Manager", "Product Manager", "Senior Product Manager", 
            "Principal Product Manager", "Group Product Manager", "Product Director", 
            "VP of Product", "Chief Product Officer", "Product Marketing Manager",
            "Technical Product Manager", "Growth Product Manager"
        ],
        "Design": [
            "UX Designer", "Senior UX Designer", "Staff UX Designer", "Design Lead", 
            "Principal Designer", "Design Director", "VP of Design", "UI Designer",
            "UX Researcher", "Product Designer", "Visual Designer", "Design Systems Lead"
        ],
        "Data Science": [
            "Data Analyst", "Data Scientist", "Senior Data Scientist", "Staff Data Scientist",
            "ML Engineer", "Senior ML Engineer", "Data Engineer", "Senior Data Engineer",
            "Analytics Engineer", "Data Science Manager", "Head of Data Science",
            "Research Scientist", "Applied Scientist"
        ],
        "DevOps": [
            "DevOps Engineer", "Senior DevOps Engineer", "Staff DevOps Engineer",
            "Platform Engineer", "SRE", "Senior SRE", "Infrastructure Engineer",
            "Cloud Engineer", "DevOps Manager", "Director of Platform"
        ],
        "Security": [
            "Security Analyst", "Security Engineer", "Senior Security Engineer", 
            "Security Architect", "Principal Security Engineer", "Security Manager",
            "CISO", "Compliance Officer", "Privacy Engineer", "Threat Intelligence Analyst"
        ],
        "Marketing": [
            "Marketing Coordinator", "Marketing Manager", "Senior Marketing Manager", 
            "Marketing Director", "VP of Marketing", "Content Marketing Manager",
            "Digital Marketing Manager", "Brand Manager", "Marketing Operations Manager"
        ],
        "Sales": [
            "Sales Development Representative", "Account Executive", "Senior Account Executive",
            "Sales Manager", "Regional Sales Manager", "VP of Sales", "Chief Revenue Officer",
            "Sales Engineer", "Customer Success Manager", "Account Manager"
        ],
        "HR": [
            "HR Coordinator", "HR Generalist", "Senior HR Generalist", "HR Business Partner",
            "HR Manager", "Senior HR Manager", "HR Director", "VP of People", "Chief People Officer",
            "Talent Acquisition Manager", "Learning & Development Manager"
        ],
        "Finance": [
            "Financial Analyst", "Senior Financial Analyst", "Finance Manager", 
            "Senior Finance Manager", "Finance Director", "VP of Finance", "CFO",
            "Controller", "Accounting Manager", "FP&A Manager", "Treasury Manager"
        ],
        "Legal": [
            "Legal Counsel", "Senior Legal Counsel", "Associate General Counsel", 
            "General Counsel", "Chief Legal Officer", "Contract Manager", "Paralegal"
        ],
        "Operations": [
            "Operations Coordinator", "Operations Manager", "Senior Operations Manager",
            "Operations Director", "VP of Operations", "Chief Operating Officer",
            "Business Operations Manager", "Revenue Operations Manager"
        ],
        "Customer Success": [
            "Customer Success Associate", "Customer Success Manager", "Senior Customer Success Manager",
            "Customer Success Director", "VP of Customer Success", "Customer Support Manager",
            "Technical Account Manager"
        ],
        "Quality Assurance": [
            "QA Tester", "QA Engineer", "Senior QA Engineer", "QA Manager", 
            "QA Director", "Test Automation Engineer", "Performance Test Engineer"
        ],
        "Research": [
            "Research Analyst", "Research Manager", "Senior Research Manager",
            "Research Director", "User Researcher", "Market Research Manager"
        ],
        "Business Development": [
            "Business Development Associate", "Business Development Manager", 
            "Senior Business Development Manager", "BD Director", "VP of Business Development",
            "Partnership Manager", "Strategic Partnerships Manager"
        ]
    }
    
    for i in range(500):
        dept = random.choice(departments)
        person = {
            "id": f"person_{i+1}",
            "name": fake.name(),
            "email": fake.email(),
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
    """Generate realistic team data"""
    teams = [
        # Engineering Teams
        {"id": "team_1", "name": "Core Platform", "department": "Engineering", "focus": "Platform infrastructure and core services"},
        {"id": "team_2", "name": "Frontend Web", "department": "Engineering", "focus": "Web application development and user interfaces"},
        {"id": "team_3", "name": "Mobile Apps", "department": "Engineering", "focus": "iOS and Android native applications"},
        {"id": "team_4", "name": "Backend Services", "department": "Engineering", "focus": "API development and microservices architecture"},
        {"id": "team_5", "name": "Platform Tools", "department": "Engineering", "focus": "Developer tools and internal platforms"},
        {"id": "team_6", "name": "Integration", "department": "Engineering", "focus": "Third-party integrations and external APIs"},
        
        # Data Science Teams
        {"id": "team_7", "name": "Data Pipeline", "department": "Data Science", "focus": "Data ingestion, processing, and ETL workflows"},
        {"id": "team_8", "name": "ML Platform", "department": "Data Science", "focus": "Machine learning infrastructure and model deployment"},
        {"id": "team_9", "name": "Analytics", "department": "Data Science", "focus": "Business intelligence and data visualization"},
        {"id": "team_10", "name": "AI Research", "department": "Data Science", "focus": "Applied research and experimental ML models"},
        
        # Product Teams
        {"id": "team_11", "name": "Core Product", "department": "Product", "focus": "Core platform features and user workflows"},
        {"id": "team_12", "name": "Growth Product", "department": "Product", "focus": "User acquisition, activation, and retention"},
        {"id": "team_13", "name": "Enterprise Product", "department": "Product", "focus": "Enterprise features and B2B functionality"},
        {"id": "team_14", "name": "Mobile Product", "department": "Product", "focus": "Mobile app strategy and features"},
        
        # Design Teams
        {"id": "team_15", "name": "User Experience", "department": "Design", "focus": "User research and experience design"},
        {"id": "team_16", "name": "Visual Design", "department": "Design", "focus": "Brand, visual identity, and design systems"},
        {"id": "team_17", "name": "Product Design", "department": "Design", "focus": "Product interface design and prototyping"},
        
        # DevOps Teams
        {"id": "team_18", "name": "Platform Engineering", "department": "DevOps", "focus": "Kubernetes, containers, and cloud infrastructure"},
        {"id": "team_19", "name": "Site Reliability", "department": "DevOps", "focus": "Monitoring, alerting, and system reliability"},
        {"id": "team_20", "name": "CI/CD", "department": "DevOps", "focus": "Build automation and deployment pipelines"},
        
        # Security Teams
        {"id": "team_21", "name": "Infrastructure Security", "department": "Security", "focus": "Cloud security and infrastructure hardening"},
        {"id": "team_22", "name": "Application Security", "department": "Security", "focus": "Code security, vulnerability scanning, and SAST/DAST"},
        {"id": "team_23", "name": "Compliance", "department": "Security", "focus": "SOC2, GDPR, and regulatory compliance"},
        
        # Marketing Teams
        {"id": "team_24", "name": "Content Marketing", "department": "Marketing", "focus": "Blog, documentation, and educational content"},
        {"id": "team_25", "name": "Digital Marketing", "department": "Marketing", "focus": "SEO, SEM, and online advertising campaigns"},
        {"id": "team_26", "name": "Product Marketing", "department": "Marketing", "focus": "Go-to-market strategy and product positioning"},
        
        # Sales Teams
        {"id": "team_27", "name": "Enterprise Sales", "department": "Sales", "focus": "Large enterprise deals and strategic accounts"},
        {"id": "team_28", "name": "SMB Sales", "department": "Sales", "focus": "Small and medium business customer acquisition"},
        {"id": "team_29", "name": "Sales Engineering", "department": "Sales", "focus": "Technical sales support and demos"},
        
        # Customer Success Teams
        {"id": "team_30", "name": "Customer Success", "department": "Customer Success", "focus": "Customer onboarding and relationship management"},
        {"id": "team_31", "name": "Support Engineering", "department": "Customer Success", "focus": "Technical customer support and troubleshooting"},
        
        # Quality Assurance Teams
        {"id": "team_32", "name": "QA Automation", "department": "Quality Assurance", "focus": "Test automation and continuous testing"},
        {"id": "team_33", "name": "Manual Testing", "department": "Quality Assurance", "focus": "Exploratory testing and user acceptance testing"},
        
        # Operations Teams
        {"id": "team_34", "name": "Business Operations", "department": "Operations", "focus": "Process optimization and operational efficiency"},
        {"id": "team_35", "name": "Revenue Operations", "department": "Operations", "focus": "Sales and marketing operations and analytics"}
    ]
    
    return teams

def generate_groups_data():
    """Generate cross-functional groups that span multiple teams"""
    groups = [
        {
            "id": "group_1",
            "name": "Security Council",
            "description": "Cross-functional security governance, policy oversight, and threat assessment",
            "type": "governance",
            "lead_department": "Security"
        },
        {
            "id": "group_2", 
            "name": "Data Governance Committee",
            "description": "Data privacy, compliance, quality standards, and governance across all teams",
            "type": "governance",
            "lead_department": "Data Science"
        },
        {
            "id": "group_3",
            "name": "Architecture Review Board",
            "description": "Technical architecture decisions, design standards, and technology strategy",
            "type": "technical",
            "lead_department": "Engineering"
        },
        {
            "id": "group_4",
            "name": "Product Strategy Group",
            "description": "Cross-product strategy, roadmap alignment, and market positioning",
            "type": "strategic",
            "lead_department": "Product"
        },
        {
            "id": "group_5",
            "name": "Incident Response Team",
            "description": "24/7 incident response, crisis management, and post-incident reviews",
            "type": "operational",
            "lead_department": "DevOps"
        },
        {
            "id": "group_6",
            "name": "Compliance Working Group",
            "description": "SOC2, GDPR, ISO27001, and regulatory compliance coordination",
            "type": "compliance",
            "lead_department": "Security"
        },
        {
            "id": "group_7",
            "name": "Engineering Excellence Committee",
            "description": "Code quality standards, engineering best practices, and technical debt management",
            "type": "technical",
            "lead_department": "Engineering"
        },
        {
            "id": "group_8",
            "name": "Diversity & Inclusion Council",
            "description": "Promoting diversity, equity, and inclusion across all departments",
            "type": "cultural",
            "lead_department": "HR"
        },
        {
            "id": "group_9",
            "name": "API Standards Committee",
            "description": "API design standards, versioning strategies, and developer experience",
            "type": "technical",
            "lead_department": "Engineering"
        },
        {
            "id": "group_10",
            "name": "Customer Advisory Board",
            "description": "Customer feedback integration, product prioritization, and user experience insights",
            "type": "strategic",
            "lead_department": "Product"
        },
        {
            "id": "group_11",
            "name": "Business Continuity Planning",
            "description": "Disaster recovery, business continuity, and operational resilience planning",
            "type": "operational",
            "lead_department": "Operations"
        },
        {
            "id": "group_12",
            "name": "Open Source Committee",
            "description": "Open source contribution guidelines, license management, and community engagement",
            "type": "technical",
            "lead_department": "Engineering"
        },
        {
            "id": "group_13",
            "name": "Performance Optimization Task Force",
            "description": "System performance analysis, optimization strategies, and scalability planning",
            "type": "technical",
            "lead_department": "DevOps"
        },
        {
            "id": "group_14",
            "name": "Sales & Marketing Alignment",
            "description": "Sales and marketing coordination, lead qualification, and customer journey optimization",
            "type": "strategic",
            "lead_department": "Sales"
        },
        {
            "id": "group_15",
            "name": "Employee Wellness Committee",
            "description": "Employee mental health, work-life balance, and workplace wellness initiatives",
            "type": "cultural",
            "lead_department": "HR"
        }
    ]
    
    return groups

def generate_policies_data():
    """Generate realistic policy data with detailed descriptions"""
    policies = [
        {
            "id": "policy_1",
            "name": "Code Review Policy",
            "description": "All code changes must be reviewed by at least one qualified engineer before merging. Reviews must check for security vulnerabilities, code quality, performance impact, and adherence to coding standards. Critical system changes require review by senior engineers.",
            "category": "development",
            "severity": "high",
            "responsible_type": "team",
            "compliance_frameworks": ["SOC2", "Internal", "ISO27001"]
        },
        {
            "id": "policy_2", 
            "name": "Data Retention and Deletion Policy",
            "description": "Personal data must be retained only for as long as necessary for business purposes. Customer data retention periods: account data (7 years after closure), activity logs (2 years), marketing data (3 years with consent). Automated deletion processes must be implemented with audit trails.",
            "category": "data_privacy",
            "severity": "critical",
            "responsible_type": "group",
            "compliance_frameworks": ["GDPR", "SOC2", "CCPA"]
        },
        {
            "id": "policy_3",
            "name": "Identity and Access Management Policy", 
            "description": "User access must follow principle of least privilege. Access requests require manager approval and periodic review (quarterly for privileged access, annually for standard access). Multi-factor authentication mandatory for all systems. Access must be revoked within 4 hours of employment termination.",
            "category": "security",
            "severity": "critical",
            "responsible_type": "group",
            "compliance_frameworks": ["SOC2", "ISO27001", "NIST"]
        },
        {
            "id": "policy_4",
            "name": "Security Incident Response Policy",
            "description": "Security incidents must be detected, contained, and resolved according to severity levels. Critical incidents (P0) require immediate response within 15 minutes, high severity (P1) within 1 hour. All incidents require post-mortem analysis and documentation. External notifications required for data breaches within 72 hours.",
            "category": "security",
            "severity": "critical", 
            "responsible_type": "group",
            "compliance_frameworks": ["SOC2", "ISO27001", "GDPR"]
        },
        {
            "id": "policy_5",
            "name": "API Security and Design Standards",
            "description": "All APIs must implement authentication, authorization, rate limiting, and input validation. API keys must be rotated quarterly. Public APIs require additional security testing and documentation. API versioning strategy must ensure backward compatibility for minimum 18 months.",
            "category": "security",
            "severity": "high",
            "responsible_type": "team",
            "compliance_frameworks": ["SOC2", "Internal", "OWASP"]
        },
        {
            "id": "policy_6",
            "name": "Data Encryption and Protection Policy",
            "description": "All data must be encrypted at rest using AES-256 and in transit using TLS 1.3+. Database encryption keys must be managed through dedicated key management service with rotation every 90 days. Backup data must maintain same encryption standards.",
            "category": "security",
            "severity": "high",
            "responsible_type": "team",
            "compliance_frameworks": ["SOC2", "PCI-DSS", "FIPS 140-2"]
        },
        {
            "id": "policy_7",
            "name": "Secure Software Development Lifecycle",
            "description": "Security must be integrated throughout SDLC including threat modeling, secure coding standards, static/dynamic analysis, and security testing. Dependency scanning required for all third-party libraries. Security sign-off required before production deployment.",
            "category": "development",
            "severity": "high",
            "responsible_type": "team",
            "compliance_frameworks": ["Internal", "SOC2", "NIST"]
        },
        {
            "id": "policy_8",
            "name": "Data Classification and Handling Policy",
            "description": "Data must be classified as Public, Internal, Confidential, or Restricted. Each classification has specific handling, access, and retention requirements. PII and financial data automatically classified as Restricted. Data labeling required on all systems and documents.",
            "category": "data_privacy",
            "severity": "high",
            "responsible_type": "group",
            "compliance_frameworks": ["GDPR", "SOC2", "CCPA"]
        },
        {
            "id": "policy_9",
            "name": "Third Party Risk Management Policy",
            "description": "All vendors handling company or customer data must undergo security assessment. Due diligence includes security questionnaires, certifications review, and on-site assessments for critical vendors. Contracts must include security requirements and audit rights. Annual vendor reviews required.",
            "category": "security",
            "severity": "medium",
            "responsible_type": "group",
            "compliance_frameworks": ["SOC2", "Internal", "ISO27001"]
        },
        {
            "id": "policy_10",
            "name": "Infrastructure Monitoring and Alerting Policy",
            "description": "All production systems must have monitoring and alerting for availability, performance, and security events. Alert escalation procedures defined with response time SLAs. Security events require immediate notification to security team. Monitoring data retained for minimum 1 year.",
            "category": "operational",
            "severity": "medium",
            "responsible_type": "team",
            "compliance_frameworks": ["SOC2", "Internal"]
        },
        {
            "id": "policy_11",
            "name": "Change Management Policy",
            "description": "All production changes must follow formal change management process including impact assessment, approval workflow, rollback plan, and post-deployment verification. Emergency changes allowed with retroactive approval within 24 hours. Change advisory board reviews high-risk changes weekly.",
            "category": "operational",
            "severity": "high",
            "responsible_type": "group",
            "compliance_frameworks": ["SOC2", "ITIL", "Internal"]
        },
        {
            "id": "policy_12",
            "name": "Business Continuity and Disaster Recovery Policy", 
            "description": "Critical business functions must maintain RTO of 4 hours and RPO of 1 hour. Disaster recovery plans tested quarterly with annual full-scale exercises. Backup systems maintained in geographically separate regions. Communication plans include customer and stakeholder notification procedures.",
            "category": "operational",
            "severity": "critical",
            "responsible_type": "group",
            "compliance_frameworks": ["SOC2", "ISO22301", "Internal"]
        },
        {
            "id": "policy_13",
            "name": "Employee Background Check Policy",
            "description": "All employees require background checks appropriate to their access level. Standard checks for general employees, enhanced checks for privileged access roles. Checks must be completed before access provisioning. Re-verification required every 5 years for high-privilege roles.",
            "category": "hr_security",
            "severity": "medium",
            "responsible_type": "group",
            "compliance_frameworks": ["SOC2", "Internal"]
        },
        {
            "id": "policy_14",
            "name": "Acceptable Use Policy",
            "description": "Company resources must be used only for legitimate business purposes. Prohibited activities include unauthorized software installation, personal file storage, accessing inappropriate content, and circumventing security controls. Violations may result in disciplinary action.",
            "category": "hr_security",
            "severity": "medium",
            "responsible_type": "group",
            "compliance_frameworks": ["Internal", "SOC2"]
        },
        {
            "id": "policy_15",
            "name": "Security Awareness Training Policy",
            "description": "All employees must complete security awareness training within 30 days of hire and annually thereafter. Training covers phishing, social engineering, password security, and incident reporting. Specialized training required for developers and administrators. Completion tracking and reporting required.",
            "category": "training",
            "severity": "medium",
            "responsible_type": "group",
            "compliance_frameworks": ["SOC2", "ISO27001", "Internal"]
        },
        {
            "id": "policy_16",
            "name": "Cloud Security Configuration Policy",
            "description": "Cloud resources must follow security baselines including network segmentation, access controls, logging, and encryption. Infrastructure as Code required for reproducible deployments. Cloud security posture monitoring with automated compliance checking. Regular security configuration reviews required.",
            "category": "security",
            "severity": "high",
            "responsible_type": "team",
            "compliance_frameworks": ["SOC2", "CSF", "CIS"]
        },
        {
            "id": "policy_17",
            "name": "Privacy by Design Policy",
            "description": "Privacy considerations must be integrated into all product development from initial design. Privacy impact assessments required for new features handling personal data. Data minimization principles applied with purpose limitation and consent management. Privacy officer approval required for data processing changes.",
            "category": "data_privacy",
            "severity": "high",
            "responsible_type": "group",
            "compliance_frameworks": ["GDPR", "CCPA", "PIPEDA"]
        },
        {
            "id": "policy_18",
            "name": "Mobile Device Management Policy",
            "description": "Corporate mobile devices must be enrolled in MDM system with encryption, passcode requirements, and remote wipe capability. BYOD devices accessing corporate data require containerization and security app installation. Lost or stolen devices must be reported immediately for remote wipe.",
            "category": "security",
            "severity": "medium",
            "responsible_type": "group",
            "compliance_frameworks": ["SOC2", "Internal"]
        },
        {
            "id": "policy_19",
            "name": "Open Source Software Policy",
            "description": "Open source components must be reviewed for license compatibility, security vulnerabilities, and maintenance status before use. Vulnerability scanning required for all dependencies with prompt patching of critical issues. Legal review required for copyleft licenses. Contribution guidelines established for employee contributions.",
            "category": "development",
            "severity": "medium",
            "responsible_type": "group",
            "compliance_frameworks": ["Internal", "SOC2"]
        },
        {
            "id": "policy_20",
            "name": "Records Management and Retention Policy",
            "description": "Business records must be classified, retained, and disposed of according to legal and regulatory requirements. Legal hold procedures established for litigation and investigations. Electronic records require metadata preservation and audit trails. Retention schedules reviewed annually and updated for regulatory changes.",
            "category": "compliance",
            "severity": "medium",
            "responsible_type": "group",
            "compliance_frameworks": ["SOX", "GDPR", "Internal"]
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
        if group["lead_department"] == "Security":
            relevant_people = [p for p in people if p["department"] in ["Security", "Engineering", "DevOps"]]
        elif group["lead_department"] == "Data Science":
            relevant_people = [p for p in people if p["department"] in ["Data Science", "Engineering", "Product"]]
        elif group["lead_department"] == "Engineering":
            relevant_people = [p for p in people if p["department"] in ["Engineering", "DevOps", "Security"]]
        elif group["lead_department"] == "Product":
            relevant_people = [p for p in people if p["department"] in ["Product", "Design", "Engineering"]]
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
            if policy["category"] in ["development", "operational"]:
                eligible_teams = [t for t in teams if t["department"] in ["Engineering", "DevOps"]]
            elif policy["category"] == "security":
                eligible_teams = [t for t in teams if t["department"] in ["Security", "Engineering", "DevOps"]]
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
            if policy["category"] == "security":
                eligible_groups = [g for g in groups if "Security" in g["name"] or "Incident" in g["name"]]
            elif policy["category"] == "data_privacy":
                eligible_groups = [g for g in groups if "Data" in g["name"] or "Compliance" in g["name"]]
            elif policy["category"] == "development":
                eligible_groups = [g for g in groups if "Architecture" in g["name"]]
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