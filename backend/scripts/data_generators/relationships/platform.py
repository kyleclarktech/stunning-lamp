from typing import List, Dict, Any
import random
from ..base import BaseGenerator


class ComponentDeployedInGenerator(BaseGenerator):
    """Generate platform component deployment in cloud regions"""
    
    def __init__(self, platform_components: List[Dict[str, Any]], cloud_regions: List[Dict[str, Any]]):
        self.platform_components = platform_components
        self.cloud_regions = cloud_regions
    
    def generate(self) -> List[Dict[str, Any]]:
        relationships = []
        
        # Deploy components across multiple regions for redundancy
        for component in self.platform_components:
            # Core components deployed in all major regions
            if component["tier"] == "core":
                num_regions = random.randint(6, 12)
            else:
                num_regions = random.randint(2, 6)
            
            deployed_regions = random.sample(self.cloud_regions, num_regions)
            for region in deployed_regions:
                relationships.append({
                    "component_id": component["id"],
                    "region_id": region["id"]
                })
        
        return relationships


class ClientUsesComponentGenerator(BaseGenerator):
    """Generate client usage of platform components"""
    
    def __init__(self, clients: List[Dict[str, Any]], platform_components: List[Dict[str, Any]]):
        self.clients = clients
        self.platform_components = platform_components
    
    def generate(self) -> List[Dict[str, Any]]:
        relationships = []
        
        for client in self.clients:
            # All clients use core components
            core_components = [c for c in self.platform_components if c["tier"] == "core"]
            for component in core_components:
                usage_level = "high" if client["tier"] == "strategic" else random.choice(["low", "medium", "high"])
                relationships.append({
                    "client_id": client["id"],
                    "component_id": component["id"],
                    "usage_level": usage_level
                })
            
            # Strategic and enterprise clients use additional components
            if client["tier"] in ["strategic", "enterprise"]:
                supporting_components = [c for c in self.platform_components if c["tier"] == "supporting"]
                num_supporting = random.randint(2, len(supporting_components))
                for component in random.sample(supporting_components, num_supporting):
                    relationships.append({
                        "client_id": client["id"],
                        "component_id": component["id"],
                        "usage_level": random.choice(["low", "medium"])
                    })
        
        return relationships


class PersonExpertInComponentGenerator(BaseGenerator):
    """Generate person expertise in platform components"""
    
    def __init__(self, people: List[Dict[str, Any]], platform_components: List[Dict[str, Any]]):
        self.people = people
        self.platform_components = platform_components
    
    def generate(self) -> List[Dict[str, Any]]:
        relationships = []
        
        # Group components by type
        components_by_type = {}
        for component in self.platform_components:
            comp_type = component["type"]
            if comp_type not in components_by_type:
                components_by_type[comp_type] = []
            components_by_type[comp_type].append(component)
        
        # Assign expertise based on person's role and department
        for person in self.people:
            expertise_areas = []
            
            # Engineering roles have technical expertise
            if person["department"] == "Engineering":
                if person["role"] == "Principal Engineer":
                    # Principals are experts in core components
                    expertise_areas = [c for c in self.platform_components if c["tier"] == "core"]
                    expertise_level_range = (4, 5)
                elif person["role"] == "Senior Engineer":
                    # Seniors specialize in specific component types
                    comp_type = random.choice(list(components_by_type.keys()))
                    expertise_areas = components_by_type[comp_type]
                    expertise_level_range = (3, 5)
                elif person["role"] == "Software Engineer":
                    # Engineers have moderate expertise in a few components
                    num_components = random.randint(2, 4)
                    expertise_areas = random.sample(self.platform_components, min(num_components, len(self.platform_components)))
                    expertise_level_range = (2, 4)
            
            # Operations roles understand deployment and monitoring
            elif person["department"] == "Operations":
                if person["role"] == "Site Reliability Engineer":
                    # SREs are experts in infrastructure components
                    expertise_areas = [c for c in self.platform_components if c["type"] in ["infrastructure", "monitoring"]]
                    expertise_level_range = (3, 5)
                elif person["role"] == "DevOps Engineer":
                    # DevOps engineers know deployment pipelines
                    expertise_areas = [c for c in self.platform_components if c["type"] in ["pipeline", "deployment"]]
                    expertise_level_range = (3, 4)
            
            # Customer Success understands customer-facing components
            elif person["department"] == "Customer Success":
                if person["role"] in ["Technical Account Manager", "Solution Architect"]:
                    # TAMs and SAs understand customer-facing components
                    expertise_areas = [c for c in self.platform_components if c["type"] in ["api", "ui", "integration"]]
                    expertise_level_range = (2, 4)
            
            # Create expertise relationships
            for component in expertise_areas:
                expertise_level = random.randint(*expertise_level_range)
                relationships.append({
                    "person_id": person["id"],
                    "component_id": component["id"],
                    "expertise_level": expertise_level
                })
        
        return relationships