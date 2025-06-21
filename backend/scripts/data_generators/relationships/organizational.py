from typing import List, Dict, Any
import random
from faker import Faker
from ..base import BaseGenerator

fake = Faker()


class PersonTeamMembershipGenerator(BaseGenerator):
    """Generate person-team membership relationships"""
    
    def __init__(self, people: List[Dict[str, Any]], teams: List[Dict[str, Any]]):
        self.people = people
        self.teams = teams
    
    def generate(self) -> List[Dict[str, Any]]:
        relationships = []
        
        # Assign people to teams (each person belongs to 1 primary team)
        for person in self.people:
            # Find teams in the same department
            dept_teams = [t for t in self.teams if t["department"] == person["department"]]
            if dept_teams:
                team = random.choice(dept_teams)
            else:
                team = random.choice(self.teams)
            
            relationships.append({
                "person_id": person["id"],
                "team_id": team["id"],
                "role": person["role"],
                "is_lead": random.random() < 0.15  # 15% chance of being team lead
            })
        
        return relationships


class PersonGroupMembershipGenerator(BaseGenerator):
    """Generate person-group membership relationships"""
    
    def __init__(self, people: List[Dict[str, Any]], groups: List[Dict[str, Any]]):
        self.people = people
        self.groups = groups
    
    def generate(self) -> List[Dict[str, Any]]:
        relationships = []
        
        # Assign people to groups (cross-functional, 3-8 people per group)
        for group in self.groups:
            # Get people from relevant departments
            if group["lead_department"] == "Security & Compliance":
                relevant_people = [p for p in self.people if p["department"] in ["Security & Compliance", "Engineering", "Infrastructure & DevOps"]]
            elif group["lead_department"] == "Data Science":
                relevant_people = [p for p in self.people if p["department"] in ["Data Science", "Analytics Engineering", "Product"]]
            elif group["lead_department"] == "Engineering":
                relevant_people = [p for p in self.people if p["department"] in ["Engineering", "Infrastructure & DevOps", "Security & Compliance"]]
            elif group["lead_department"] == "Data Platform Engineering":
                relevant_people = [p for p in self.people if p["department"] in ["Data Platform Engineering", "Analytics Engineering", "Infrastructure & DevOps"]]
            elif group["lead_department"] == "Product":
                relevant_people = [p for p in self.people if p["department"] in ["Product", "Engineering", "Data Science"]]
            elif group["lead_department"] == "Customer Success":
                relevant_people = [p for p in self.people if p["department"] in ["Customer Success", "Professional Services", "Solutions Architecture"]]
            elif group["lead_department"] == "Infrastructure & DevOps":
                relevant_people = [p for p in self.people if p["department"] in ["Infrastructure & DevOps", "Engineering", "Security & Compliance"]]
            elif group["lead_department"] == "Solutions Architecture":
                relevant_people = [p for p in self.people if p["department"] in ["Solutions Architecture", "Professional Services", "Engineering"]]
            elif group["lead_department"] == "Sales":
                relevant_people = [p for p in self.people if p["department"] in ["Sales", "Marketing", "Customer Success"]]
            else:
                relevant_people = self.people
            
            # Select 3-8 people for this group
            group_size = random.randint(3, min(8, len(relevant_people)))
            group_members = random.sample(relevant_people, group_size)
            
            for i, person in enumerate(group_members):
                relationships.append({
                    "person_id": person["id"],
                    "group_id": group["id"],
                    "role": "Lead" if i == 0 else "Member",
                    "joined_date": fake.date_between(start_date='-2y', end_date='today').isoformat()
                })
        
        return relationships


class TeamPolicyResponsibilityGenerator(BaseGenerator):
    """Generate team-policy responsibility relationships"""
    
    def __init__(self, teams: List[Dict[str, Any]], policies: List[Dict[str, Any]]):
        self.teams = teams
        self.policies = policies
    
    def generate(self) -> List[Dict[str, Any]]:
        relationships = []
        
        # Assign policies to teams based on responsible_type
        for policy in self.policies:
            if policy["responsible_type"] == "team":
                # Assign to relevant teams based on policy category
                if policy["category"] == "data_governance":
                    eligible_teams = [t for t in self.teams if t["department"] in ["Data Platform Engineering", "Analytics Engineering", "Data Science"]]
                elif policy["category"] == "platform":
                    eligible_teams = [t for t in self.teams if t["department"] in ["Engineering", "Data Platform Engineering", "Infrastructure & DevOps"]]
                elif policy["category"] == "security":
                    eligible_teams = [t for t in self.teams if t["department"] in ["Security & Compliance", "Engineering", "Infrastructure & DevOps"]]
                elif policy["category"] in ["development", "operations"]:
                    eligible_teams = [t for t in self.teams if t["department"] in ["Engineering", "Infrastructure & DevOps", "Data Platform Engineering"]]
                else:
                    eligible_teams = self.teams
                
                # Assign to 1-3 teams
                responsible_teams = random.sample(eligible_teams, random.randint(1, min(3, len(eligible_teams))))
                for team in responsible_teams:
                    relationships.append({
                        "team_id": team["id"],
                        "policy_id": policy["id"],
                        "responsibility_type": random.choice(["owner", "contributor", "reviewer"]),
                        "assigned_date": fake.date_between(start_date='-1y', end_date='today').isoformat()
                    })
        
        return relationships


class GroupPolicyResponsibilityGenerator(BaseGenerator):
    """Generate group-policy responsibility relationships"""
    
    def __init__(self, groups: List[Dict[str, Any]], policies: List[Dict[str, Any]]):
        self.groups = groups
        self.policies = policies
    
    def generate(self) -> List[Dict[str, Any]]:
        relationships = []
        
        # Assign policies to groups based on responsible_type
        for policy in self.policies:
            if policy["responsible_type"] == "group":
                # Assign to relevant groups
                if policy["category"] == "data_governance":
                    eligible_groups = [g for g in self.groups if "Data Governance" in g["name"] or "Data Quality" in g["name"]]
                elif policy["category"] == "security":
                    eligible_groups = [g for g in self.groups if "Security" in g["name"] or "Compliance" in g["name"]]
                elif policy["category"] == "data_privacy":
                    eligible_groups = [g for g in self.groups if "Data" in g["name"] or "Compliance" in g["name"] or "Privacy" in g["name"]]
                elif policy["category"] == "platform":
                    eligible_groups = [g for g in self.groups if "API" in g["name"] or "SLA" in g["name"] or "Architecture" in g["name"]]
                elif policy["category"] == "development":
                    eligible_groups = [g for g in self.groups if "Architecture" in g["name"] or "API" in g["name"]]
                else:
                    eligible_groups = self.groups
                
                if eligible_groups:
                    responsible_group = random.choice(eligible_groups)
                    relationships.append({
                        "group_id": responsible_group["id"],
                        "policy_id": policy["id"],
                        "responsibility_type": "owner",
                        "assigned_date": fake.date_between(start_date='-1y', end_date='today').isoformat()
                    })
        
        return relationships


class PersonReportsToGenerator(BaseGenerator):
    """Generate reporting relationships between people"""
    
    def __init__(self, people: List[Dict[str, Any]]):
        self.people = people
    
    def generate(self) -> List[Dict[str, Any]]:
        # This is handled in the entity generation phase where manager_id is set
        # Return empty list as relationships are created directly in seeder
        return []


class PersonMentorshipGenerator(BaseGenerator):
    """Generate mentorship relationships"""
    
    def __init__(self, people: List[Dict[str, Any]]):
        self.people = people
    
    def generate(self) -> List[Dict[str, Any]]:
        relationships = []
        
        # Create mentorship relationships
        senior_people = [p for p in self.people if p["seniority"] in ["Senior", "Staff", "Principal"]]
        junior_people = [p for p in self.people if p["seniority"] in ["Junior", "Mid"]]
        
        for mentor in random.sample(senior_people, min(30, len(senior_people))):
            # Each mentor has 1-3 mentees
            num_mentees = random.randint(1, 3)
            potential_mentees = [p for p in junior_people if p["department"] == mentor["department"]]
            
            if potential_mentees:
                mentees = random.sample(potential_mentees, min(num_mentees, len(potential_mentees)))
                for mentee in mentees:
                    relationships.append({
                        "mentor_id": mentor["id"],
                        "mentee_id": mentee["id"],
                        "start_date": fake.date_between(start_date='-1y', end_date='today').isoformat(),
                        "focus_area": random.choice(["technical skills", "career development", "domain expertise", "leadership"])
                    })
        
        return relationships


class PersonBackupGenerator(BaseGenerator):
    """Generate backup relationships for critical roles"""
    
    def __init__(self, people: List[Dict[str, Any]]):
        self.people = people
    
    def generate(self) -> List[Dict[str, Any]]:
        relationships = []
        
        # Create backup relationships for critical roles
        critical_people = [p for p in self.people if "Lead" in p["role"] or "Manager" in p["role"] or "Principal" in p["role"]]
        
        for person in critical_people:
            # Find potential backups in same department
            potential_backups = [p for p in self.people if p["department"] == person["department"] and p["id"] != person["id"]]
            
            if potential_backups:
                backup = random.choice(potential_backups)
                relationships.append({
                    "primary_person_id": person["id"],
                    "backup_person_id": backup["id"],
                    "coverage_type": random.choice(["full", "partial", "emergency"]),
                    "readiness_level": random.choice(["ready", "in_training", "identified"])
                })
        
        return relationships


class PersonOfficeAssignmentGenerator(BaseGenerator):
    """Generate person-office assignment relationships"""
    
    def __init__(self, people: List[Dict[str, Any]], offices: List[Dict[str, Any]]):
        self.people = people
        self.offices = offices
    
    def generate(self) -> List[Dict[str, Any]]:
        relationships = []
        
        # Office mapping based on location
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
        
        for person in self.people:
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
            
            relationships.append({
                "person_id": person["id"],
                "office_id": office_id,
                "start_date": person["hire_date"],
                "is_remote": person["location"] == "Remote",
                "desk_location": f"Floor {random.randint(1, 5)}, Section {random.choice(['A', 'B', 'C', 'D'])}" if person["location"] != "Remote" else None
            })
        
        return relationships


class TeamHandoffGenerator(BaseGenerator):
    """Generate team handoff relationships for 24/7 coverage"""
    
    def __init__(self, teams: List[Dict[str, Any]], offices: List[Dict[str, Any]], 
                 person_team_memberships: List[Dict[str, Any]], 
                 person_office_assignments: List[Dict[str, Any]]):
        self.teams = teams
        self.offices = offices
        self.person_team_memberships = person_team_memberships
        self.person_office_assignments = person_office_assignments
    
    def generate(self) -> List[Dict[str, Any]]:
        relationships = []
        
        # Map teams to their primary office timezone
        team_timezones = {}
        for team in self.teams:
            # Find the most common office among team members
            team_offices = {}
            for membership in self.person_team_memberships:
                if membership["team_id"] == team["id"]:
                    person_id = membership["person_id"]
                    # Find person's office
                    for office_assignment in self.person_office_assignments:
                        if office_assignment["person_id"] == person_id:
                            office_id = office_assignment["office_id"]
                            team_offices[office_id] = team_offices.get(office_id, 0) + 1
                            break
            
            # Assign team to most common office
            if team_offices:
                primary_office_id = max(team_offices, key=team_offices.get)
                office = next((o for o in self.offices if o["id"] == primary_office_id), None)
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
            from_teams = [t for t in self.teams if t["id"] in team_timezones and team_timezones[t["id"]]["region"] == pattern["from_region"]]
            to_teams = [t for t in self.teams if t["id"] in team_timezones and team_timezones[t["id"]]["region"] == pattern["to_region"]]
            
            # Match teams by department/focus area
            for from_team in from_teams:
                matching_to_teams = [t for t in to_teams if t["department"] == from_team["department"] or t["focus"] == from_team["focus"]]
                if matching_to_teams and from_team["id"] != matching_to_teams[0]["id"]:
                    to_team = matching_to_teams[0]
                    relationships.append({
                        "from_team_id": from_team["id"],
                        "to_team_id": to_team["id"],
                        "handoff_time": pattern["handoff_time"],
                        "handoff_type": pattern["handoff_type"]
                    })
        
        return relationships