"""Projects and Sprints entity generators."""

import random
from typing import List, Dict, Any
from datetime import datetime, timedelta
from ..base import BaseGenerator, generate_date_range
from ..config import (
    PROJECTS_COUNT, SPRINTS_PER_PROJECT, PROJECT_TYPES, 
    PROJECT_STATUSES, CLIENTS_COUNT
)


class ProjectsGenerator(BaseGenerator):
    """Generator for Project entities."""
    
    def __init__(self, count: int = PROJECTS_COUNT, seed: int = None):
        super().__init__(seed)
        self.count = count
        self.project_templates = [
            # Platform projects
            {"name": "Data Lake Modernization", "type": "platform", 
             "description": "Modernize data lake infrastructure with next-gen storage and compute"},
            {"name": "Real-time Analytics Platform", "type": "platform", 
             "description": "Build real-time analytics capabilities for streaming data"},
            {"name": "Multi-Cloud Data Platform", "type": "platform", 
             "description": "Implement multi-cloud data platform with seamless data movement"},
            {"name": "Data Mesh Implementation", "type": "platform", 
             "description": "Transition to decentralized data mesh architecture"},
            
            # Analytics projects
            {"name": "Customer 360 Analytics", "type": "analytics", 
             "description": "Unified customer analytics across all touchpoints"},
            {"name": "Revenue Analytics Dashboard", "type": "analytics", 
             "description": "Executive dashboard for revenue and growth metrics"},
            {"name": "Supply Chain Analytics", "type": "analytics", 
             "description": "End-to-end supply chain visibility and optimization"},
            {"name": "Marketing Attribution", "type": "analytics", 
             "description": "Multi-touch attribution modeling for marketing campaigns"},
            
            # ML projects
            {"name": "Churn Prediction Model", "type": "ml", 
             "description": "Machine learning model to predict customer churn"},
            {"name": "Recommendation Engine", "type": "ml", 
             "description": "Personalized product recommendation system"},
            {"name": "Fraud Detection System", "type": "ml", 
             "description": "Real-time fraud detection using ML algorithms"},
            {"name": "Demand Forecasting", "type": "ml", 
             "description": "ML-based demand forecasting for inventory optimization"},
            
            # Integration projects
            {"name": "Salesforce Integration", "type": "integration", 
             "description": "Bi-directional data sync with Salesforce CRM"},
            {"name": "ERP Data Pipeline", "type": "integration", 
             "description": "Automated data ingestion from SAP ERP system"},
            {"name": "API Gateway Implementation", "type": "integration", 
             "description": "Unified API gateway for all data services"},
            {"name": "Legacy System Migration", "type": "integration", 
             "description": "Migrate data from legacy mainframe systems"},
            
            # Optimization projects
            {"name": "Query Performance Optimization", "type": "optimization", 
             "description": "Optimize slow-running queries and data models"},
            {"name": "Cost Optimization Initiative", "type": "optimization", 
             "description": "Reduce cloud infrastructure costs by 30%"},
            {"name": "Data Quality Framework", "type": "optimization", 
             "description": "Implement automated data quality monitoring"},
            {"name": "Pipeline Reliability", "type": "optimization", 
             "description": "Improve data pipeline reliability to 99.9% SLA"}
        ]
    
    def generate(self) -> List[Dict[str, Any]]:
        """Generate project data."""
        projects = []
        
        for i in range(self.count):
            template = self.project_templates[i % len(self.project_templates)]
            
            # Project timing
            if i < 5:  # First 5 projects are active
                status = "active"
                start_date = self.fake.date_between(start_date='-6m', end_date='-1m')
                end_date = self.fake.date_between(start_date='+1m', end_date='+6m')
            elif i < 10:  # Next 5 are planning
                status = "planning"
                start_date = self.fake.date_between(start_date='+1m', end_date='+3m')
                end_date = self.fake.date_between(start_date='+4m', end_date='+9m')
            elif i < 15:  # Next 5 are completed
                status = "completed"
                start_date = self.fake.date_between(start_date='-18m', end_date='-7m')
                end_date = self.fake.date_between(start_date='-6m', end_date='-1m')
            else:  # Rest are on hold
                status = "on_hold"
                start_date = self.fake.date_between(start_date='-12m', end_date='-3m')
                end_date = self.fake.date_between(start_date='+1m', end_date='+12m')
            
            # Budget based on project type
            budget_ranges = {
                "platform": (500000, 2000000),
                "analytics": (200000, 800000),
                "ml": (300000, 1000000),
                "integration": (100000, 500000),
                "optimization": (150000, 600000)
            }
            budget_min, budget_max = budget_ranges.get(template["type"], (100000, 500000))
            
            project = {
                "id": f"project_{i+1}",
                "name": f"{template['name']} - Phase {(i // len(self.project_templates)) + 1}",
                "type": template["type"],
                "status": status,
                "start_date": start_date.isoformat(),
                "end_date": end_date.isoformat(),
                "budget": random.randint(budget_min, budget_max),
                "priority": random.choice(["low", "medium", "high", "critical"]),
                "client_id": f"client_{(i % CLIENTS_COUNT) + 1}",
                "description": template["description"]
            }
            projects.append(project)
        
        return projects


class SprintsGenerator(BaseGenerator):
    """Generator for Sprint entities."""
    
    def __init__(self, projects: List[Dict[str, Any]], seed: int = None):
        super().__init__(seed)
        self.projects = projects
    
    def generate(self) -> List[Dict[str, Any]]:
        """Generate sprint data for projects."""
        sprints = []
        sprint_id = 1
        
        for project in self.projects:
            if project["status"] in ["active", "completed"]:
                # Generate 2-8 sprints per active/completed project
                num_sprints = random.randint(2, 8)
                project_start = datetime.fromisoformat(project["start_date"])
                
                for sprint_num in range(num_sprints):
                    sprint_start = project_start + timedelta(weeks=sprint_num * 2)
                    sprint_end = sprint_start + timedelta(weeks=2)
                    
                    # Determine sprint status
                    now = datetime.now()
                    if sprint_end < now - timedelta(days=7):
                        status = "completed"
                        velocity = random.randint(20, 40)
                    elif sprint_start <= now <= sprint_end:
                        status = "active"
                        velocity = None  # Active sprints don't have velocity yet
                    else:
                        status = "planned"
                        velocity = None
                    
                    sprint = {
                        "id": f"sprint_{sprint_id}",
                        "name": f"Sprint {sprint_num + 1}",
                        "project_id": project["id"],
                        "sprint_number": sprint_num + 1,
                        "start_date": sprint_start.isoformat(),
                        "end_date": sprint_end.isoformat(),
                        "status": status,
                        "velocity": velocity
                    }
                    sprints.append(sprint)
                    sprint_id += 1
        
        return sprints