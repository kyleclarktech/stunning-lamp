from typing import List, Dict, Any
import random
from faker import Faker
from ..base import BaseGenerator

fake = Faker()


class PersonProjectAllocationGenerator(BaseGenerator):
    """Generate person-project allocation relationships"""
    
    def __init__(self, people: List[Dict[str, Any]], projects: List[Dict[str, Any]]):
        self.people = people
        self.projects = projects
    
    def generate(self) -> List[Dict[str, Any]]:
        relationships = []
        
        # Assign people to projects
        active_projects = [p for p in self.projects if p["status"] in ["active", "planning"]]
        for project in active_projects:
            # Allocate 3-12 people per project
            num_people = random.randint(3, 12)
            allocated_people = random.sample(self.people, num_people)
            
            for person in allocated_people:
                allocation = random.randint(20, 100)  # percentage
                relationships.append({
                    "person_id": person["id"],
                    "project_id": project["id"],
                    "allocation_percentage": allocation,
                    "start_date": project["start_date"],
                    "end_date": project["end_date"],
                    "role_on_project": random.choice(["lead", "contributor", "advisor", "reviewer"])
                })
        
        return relationships


class ProjectSkillRequirementGenerator(BaseGenerator):
    """Generate project skill requirement relationships"""
    
    def __init__(self, projects: List[Dict[str, Any]], skills: List[Dict[str, Any]]):
        self.projects = projects
        self.skills = skills
    
    def generate(self) -> List[Dict[str, Any]]:
        relationships = []
        
        # Define project skill requirements
        for project in self.projects:
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
                relevant_skills = [f"skill_{i}" for i in range(1, 53)]
            
            selected_skills = random.sample(relevant_skills, min(num_required_skills, len(relevant_skills)))
            
            for skill_id in selected_skills:
                relationships.append({
                    "project_id": project["id"],
                    "skill_id": skill_id,
                    "priority": random.choice(["critical", "high", "medium", "low"]),
                    "min_proficiency_level": random.choice(["intermediate", "advanced", "expert"]),
                    "headcount_needed": random.randint(1, 3)
                })
        
        return relationships


class TeamProjectDeliveryGenerator(BaseGenerator):
    """Generate team-project delivery relationships"""
    
    def __init__(self, teams: List[Dict[str, Any]], projects: List[Dict[str, Any]]):
        self.teams = teams
        self.projects = projects
    
    def generate(self) -> List[Dict[str, Any]]:
        relationships = []
        
        # Assign teams to deliver projects
        for project in self.projects:
            # 1-3 teams per project
            num_teams = random.randint(1, 3)
            selected_teams = random.sample(self.teams, num_teams)
            
            for team in selected_teams:
                relationships.append({
                    "team_id": team["id"],
                    "project_id": project["id"],
                    "responsibility": random.choice(["primary", "supporting", "consulting"]),
                    "committed_capacity": random.randint(20, 80)  # percentage of team capacity
                })
        
        return relationships


class ProjectClientRelationshipGenerator(BaseGenerator):
    """Generate project-client relationships"""
    
    def __init__(self, projects: List[Dict[str, Any]]):
        self.projects = projects
    
    def generate(self) -> List[Dict[str, Any]]:
        # This is handled directly in the project entity which has client_id
        # Return empty list as relationships are created directly in seeder
        return []


class SprintProjectRelationshipGenerator(BaseGenerator):
    """Generate sprint-project relationships"""
    
    def __init__(self, sprints: List[Dict[str, Any]]):
        self.sprints = sprints
    
    def generate(self) -> List[Dict[str, Any]]:
        # This is handled directly in the sprint entity which has project_id
        # Return empty list as relationships are created directly in seeder
        return []


class ProjectDataResidencyGenerator(BaseGenerator):
    """Generate project data residency relationships"""
    
    def __init__(self, projects: List[Dict[str, Any]], clients: List[Dict[str, Any]], 
                 data_residency_zones: List[Dict[str, Any]], client_compliance: List[Dict[str, Any]]):
        self.projects = projects
        self.clients = clients
        self.data_residency_zones = data_residency_zones
        self.client_compliance = client_compliance
    
    def generate(self) -> List[Dict[str, Any]]:
        relationships = []
        
        # Projects store data based on their primary client's requirements
        for project in self.projects:
            # Find the client for this project
            client = next((c for c in self.clients if c["id"] == project["client_id"]), None)
            if client:
                # Determine data residency based on client and project type
                dr_zone_id = "dr_us"  # Default
                
                # If client requires GDPR, use EU data residency
                if any(cc["client_id"] == client["id"] and cc["compliance_id"] == "comp_gdpr" 
                       for cc in self.client_compliance):
                    dr_zone_id = "dr_eu"
                # Healthcare projects might need specific US regions
                elif "health" in client["industry"].lower():
                    dr_zone_id = "dr_us"
                # Financial projects in APAC
                elif "financial" in client["industry"].lower() and project["id"] in ["project_7", "project_8"]:
                    dr_zone_id = "dr_apac"
                
                relationships.append({
                    "project_id": project["id"],
                    "data_residency_id": dr_zone_id
                })
        
        return relationships