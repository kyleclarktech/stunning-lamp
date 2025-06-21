"""People entity generator."""

import random
from typing import List, Dict, Any
from ..base import BaseGenerator
from ..config import (
    PEOPLE_COUNT, DEPARTMENTS, SENIORITY_LEVELS, TIMEZONES
)


class PeopleGenerator(BaseGenerator):
    """Generator for Person entities."""
    
    def __init__(self, count: int = PEOPLE_COUNT, seed: int = None):
        super().__init__(seed)
        self.count = count
        self.roles = self._get_roles_mapping()
        self.locations = [
            "San Francisco", "New York", "Austin", "Remote", "Seattle", "Boston", 
            "Chicago", "Los Angeles", "Denver", "Atlanta", "Portland", "Miami",
            "Toronto", "London", "Berlin", "Singapore", "Sydney"
        ]
        self.timezone_map = {
            "San Francisco": "US/Pacific", "Seattle": "US/Pacific", 
            "Los Angeles": "US/Pacific", "Portland": "US/Pacific",
            "Denver": "US/Mountain", "Austin": "US/Central", "Chicago": "US/Central",
            "New York": "US/Eastern", "Boston": "US/Eastern", 
            "Atlanta": "US/Eastern", "Miami": "US/Eastern",
            "Toronto": "US/Eastern", "London": "Europe/London", "Berlin": "Europe/Berlin",
            "Singapore": "Asia/Singapore", "Sydney": "Australia/Sydney", 
            "Remote": None  # Will be randomly assigned
        }
    
    def _get_roles_mapping(self) -> Dict[str, List[str]]:
        """Get the department to roles mapping."""
        return {
            "Data Platform Engineering": [
                "Data Platform Engineer", "Senior Data Platform Engineer", 
                "Staff Data Platform Engineer", "Principal Data Platform Engineer", 
                "Data Infrastructure Engineer", "Senior Data Infrastructure Engineer",
                "Streaming Data Engineer", "Data Pipeline Engineer", 
                "Platform Engineering Manager", "Director of Data Platform", 
                "VP of Data Engineering", "Data Platform Architect"
            ],
            "Analytics Engineering": [
                "Analytics Engineer", "Senior Analytics Engineer", 
                "Lead Analytics Engineer", "Analytics Engineering Manager", 
                "BI Developer", "Senior BI Developer", "Data Modeling Engineer", 
                "Metrics Engineer", "Analytics Platform Engineer"
            ],
            "Engineering": [
                "Backend Engineer", "Senior Backend Engineer", "Staff Backend Engineer", 
                "Frontend Engineer", "Senior Frontend Engineer", "Full Stack Engineer",
                "API Engineer", "Senior API Engineer", "Engineering Manager", 
                "Director of Engineering"
            ],
            "Product": [
                "Product Manager - Analytics", "Senior Product Manager - Data Platform", 
                "Principal Product Manager", "Group Product Manager - Enterprise", 
                "Product Director", "VP of Product", "Technical Product Manager - APIs", 
                "Product Manager - Data Governance", "Product Manager - Visualization", 
                "Product Manager - Data Integration"
            ],
            "Data Science": [
                "Data Scientist", "Senior Data Scientist", "Staff Data Scientist", 
                "Principal Data Scientist", "ML Engineer", "Senior ML Engineer", 
                "Applied Scientist", "Research Data Scientist", "Data Science Manager", 
                "Director of Data Science", "VP of Data Science", "Algorithm Engineer", 
                "ML Platform Engineer"
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
                "Customer Success Manager", "Senior Customer Success Manager", 
                "Enterprise CSM", "Technical Account Manager", "Senior TAM", 
                "Customer Success Engineer", "Implementation Specialist", 
                "Customer Success Director", "VP of Customer Success",
                "Onboarding Specialist", "Customer Success Operations Manager"
            ],
            "Professional Services": [
                "Data Consultant", "Senior Data Consultant", "Lead Data Consultant",
                "Solutions Consultant", "Implementation Engineer", 
                "Senior Implementation Engineer", "Professional Services Manager", 
                "Engagement Manager", "Director of Professional Services",
                "Data Architect - Consulting", "Analytics Consultant"
            ],
            "Sales": [
                "Sales Development Representative", "Account Executive - Mid Market", 
                "Enterprise Account Executive", "Senior Enterprise AE", "Sales Engineer", 
                "Senior Sales Engineer", "Sales Manager", "Regional Sales Director", 
                "VP of Sales", "Chief Revenue Officer", "Channel Partner Manager", 
                "Strategic Account Manager"
            ],
            "Marketing": [
                "Product Marketing Manager", "Senior Product Marketing Manager", 
                "Content Marketing Manager", "Demand Generation Manager", 
                "Marketing Operations Manager", "Developer Relations Manager",
                "Marketing Director", "VP of Marketing", "Technical Writer", 
                "Marketing Analyst", "Event Marketing Manager", "Partner Marketing Manager"
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
                "Solutions Architect", "Senior Solutions Architect", 
                "Principal Solutions Architect", "Data Solutions Architect", 
                "Enterprise Architect", "Technical Solutions Manager",
                "Integration Architect", "Solutions Engineering Manager", 
                "Director of Solutions Architecture", "Pre-Sales Engineer", 
                "Customer Solutions Engineer"
            ]
        }
    
    def generate(self) -> List[Dict[str, Any]]:
        """Generate people data."""
        people = []
        
        for i in range(self.count):
            dept = random.choice(DEPARTMENTS)
            
            # Generate a name first
            full_name = self.fake.name()
            
            # Create email from the name
            first_name = full_name.split()[0].lower()
            last_name = full_name.split()[-1].lower()
            # Remove any apostrophes or special characters from names
            first_name = first_name.replace("'", "").replace("-", "")
            last_name = last_name.replace("'", "").replace("-", "")
            email = f"{first_name}.{last_name}@company.com"
            
            role = random.choice(self.roles[dept])
            hire_date = self.fake.date_between(start_date='-3y', end_date='today')
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
            
            location = random.choice(self.locations)
            
            # Map location to timezone
            timezone = self.timezone_map.get(location)
            if timezone is None:  # Remote location
                timezone = random.choice(TIMEZONES)
            
            person = {
                "id": f"person_{i+1}",
                "name": full_name,
                "email": email,
                "department": dept,
                "role": role,
                "seniority": seniority,
                "hire_date": hire_date.isoformat(),
                "location": location,
                "timezone": timezone,
                "capacity_hours_per_week": 40,
                "current_utilization": random.randint(60, 100),  # percentage
                "billing_rate": base_rate,
                "years_experience": years_exp,
                "manager_id": None  # Will be set later
            }
            people.append(person)
        
        # Set managers (roughly 1 manager per 6-8 people)
        num_managers = max(20, self.count // 25)
        managers = random.sample(people, k=num_managers)
        for manager in managers:
            if "Manager" not in manager["role"]:
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