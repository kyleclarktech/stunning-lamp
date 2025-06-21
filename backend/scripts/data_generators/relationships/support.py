from typing import List, Dict, Any
import random
from datetime import datetime
from ..base import BaseGenerator


class PersonOnCallGenerator(BaseGenerator):
    """Generate person on-call schedule relationships"""
    
    def __init__(self, people: List[Dict[str, Any]], schedules: List[Dict[str, Any]], 
                 offices: List[Dict[str, Any]], person_office_assignments: List[Dict[str, Any]]):
        self.people = people
        self.schedules = schedules
        self.offices = offices
        self.person_office_assignments = person_office_assignments
    
    def generate(self) -> List[Dict[str, Any]]:
        relationships = []
        
        # Get people by office and expertise for realistic assignments
        people_by_office = {}
        for person_office in self.person_office_assignments:
            office_id = person_office["office_id"]
            if office_id not in people_by_office:
                people_by_office[office_id] = []
            people_by_office[office_id].append(person_office["person_id"])
        
        # Assign people to schedules based on office and schedule type
        for schedule in self.schedules:
            if schedule["office_id"] and schedule["office_id"] in people_by_office:
                # Get people from this office
                office_people = people_by_office[schedule["office_id"]]
                
                # Filter by seniority for different coverage types
                available_people = []
                for person_id in office_people:
                    person = next((p for p in self.people if p["id"] == person_id), None)
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
                        relationships.append({
                            "person_id": person_id,
                            "schedule_id": schedule["id"],
                            "role": schedule["coverage_type"],
                            "reachable_via": reachable_via
                        })
            
            # Handle P0 escalation schedules (cross-office)
            elif schedule.get("severity_focus") == "P0":
                # Get senior engineers from the region
                region_offices = [o for o in self.offices if o["region"] == schedule["region"]]
                region_people = []
                for office in region_offices:
                    if office["id"] in people_by_office:
                        for person_id in people_by_office[office["id"]]:
                            person = next((p for p in self.people if p["id"] == person_id), None)
                            if person and person["seniority"] in ["Senior", "Staff", "Principal"]:
                                region_people.append(person_id)
                
                # Assign 2-3 people for P0 coverage
                if region_people:
                    assigned = random.sample(region_people, min(3, len(region_people)))
                    for person_id in assigned:
                        relationships.append({
                            "person_id": person_id,
                            "schedule_id": schedule["id"],
                            "role": "p0_escalation",
                            "reachable_via": "pagerduty"
                        })
        
        return relationships


class PersonIncidentResponseGenerator(BaseGenerator):
    """Generate person incident response relationships"""
    
    def __init__(self, people: List[Dict[str, Any]], incidents: List[Dict[str, Any]], 
                 offices: List[Dict[str, Any]], person_office_assignments: List[Dict[str, Any]]):
        self.people = people
        self.incidents = incidents
        self.offices = offices
        self.person_office_assignments = person_office_assignments
    
    def generate(self) -> List[Dict[str, Any]]:
        relationships = []
        
        # Get people by office
        people_by_office = {}
        for person_office in self.person_office_assignments:
            office_id = person_office["office_id"]
            if office_id not in people_by_office:
                people_by_office[office_id] = []
            people_by_office[office_id].append(person_office["person_id"])
        
        # Create RESPONDED_TO relationships between people and incidents
        for incident in self.incidents:
            if incident["status"] == "resolved":
                # Get people from affected regions who could respond
                responders = []
                for region in incident["affected_regions"]:
                    region_offices = [o for o in self.offices if o["region"] == region]
                    for office in region_offices:
                        if office["id"] in people_by_office:
                            office_people = people_by_office[office["id"]]
                            # For P0/P1, prefer senior people; for P2/P3, anyone can respond
                            for person_id in office_people:
                                person = next((p for p in self.people if p["id"] == person_id), None)
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
                        
                        relationships.append({
                            "person_id": person_id,
                            "incident_id": incident["id"],
                            "response_time_minutes": response_time,
                            "role": role
                        })
        
        return relationships


class PersonVisaGenerator(BaseGenerator):
    """Generate person visa relationships"""
    
    def __init__(self, people: List[Dict[str, Any]], visas: List[Dict[str, Any]], 
                 offices: List[Dict[str, Any]], person_office_assignments: List[Dict[str, Any]]):
        self.people = people
        self.visas = visas
        self.offices = offices
        self.person_office_assignments = person_office_assignments
    
    def generate(self) -> List[Dict[str, Any]]:
        relationships = []
        
        # Create person-visa relationships
        # Assign visas to people based on their office location
        for person in self.people:
            # Find person's office
            person_office_rel = next((rel for rel in self.person_office_assignments if rel["person_id"] == person["id"]), None)
            if person_office_rel:
                office = next((o for o in self.offices if o["id"] == person_office_rel["office_id"]), None)
                if office:
                    # Determine if person needs visa based on office location
                    # Assume some people are locals, some need visas
                    needs_visa = random.random() < 0.3  # 30% of people need visas
                    
                    if needs_visa:
                        # Find appropriate visas for the office country
                        country_visas = [v for v in self.visas if v["country"] == office["country"] and v["type"] != "Business"]
                        
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
                            
                            relationships.append({
                                "person_id": person["id"],
                                "visa_id": visa["id"],
                                "status": status,
                                "sponsor": sponsor
                            })
        
        # Add some people with multiple visas (e.g., business visas for travel)
        senior_people = [p for p in self.people if p["seniority"] in ["Principal", "Staff", "Senior"]]
        for person in random.sample(senior_people, min(20, len(senior_people))):
            # Add business visas for frequent travelers
            business_visas = [v for v in self.visas if v["type"] == "Business"]
            if business_visas:
                for _ in range(random.randint(1, 3)):  # 1-3 business visas
                    visa = random.choice(business_visas)
                    # Check if person already has this visa
                    existing = any(rel["person_id"] == person["id"] and rel["visa_id"] == visa["id"] 
                                  for rel in relationships)
                    if not existing:
                        relationships.append({
                            "person_id": person["id"],
                            "visa_id": visa["id"],
                            "status": "active",
                            "sponsor": "Self"
                        })
        
        return relationships


class TeamSupportsRegionGenerator(BaseGenerator):
    """Generate team-client regional support relationships"""
    
    def __init__(self, teams: List[Dict[str, Any]], clients: List[Dict[str, Any]]):
        self.teams = teams
        self.clients = clients
    
    def generate(self) -> List[Dict[str, Any]]:
        relationships = []
        
        # Customer Success and Professional Services teams support clients based on regions
        support_teams = [t for t in self.teams if t["department"] in ["Customer Success", "Professional Services", "Solutions Architecture"]]
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
            for client in self.clients:
                if client["primary_region"] in supported_regions:
                    coverage_hours = {
                        "AMERICAS": "8:00-20:00 EST",
                        "EMEA": "8:00-20:00 GMT",
                        "APAC": "8:00-20:00 JST"
                    }.get(client["primary_region"], "24/7")
                    
                    relationships.append({
                        "team_id": team["id"],
                        "client_id": client["id"],
                        "coverage_hours": coverage_hours
                    })
        
        return relationships