"""Client entity generator."""

import random
from typing import List, Dict, Any
from ..base import BaseGenerator, generate_date_range
from ..config import (
    CLIENTS_COUNT, CLIENT_INDUSTRIES, CLIENT_TIERS, 
    SUPPORT_TIERS, REGIONS, REGION_TIMEZONE_MAP
)


class ClientsGenerator(BaseGenerator):
    """Generator for Client entities."""
    
    def __init__(self, count: int = CLIENTS_COUNT, seed: int = None):
        super().__init__(seed)
        self.count = count
        self.industry_clients = [
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
    
    def generate(self) -> List[Dict[str, Any]]:
        """Generate client data with at least one client per industry."""
        clients = []
        
        for i, client_info in enumerate(self.industry_clients):
            # Tier assignment based on industry and position
            if client_info["industry"] in ["Financial Services", "Healthcare", "Government"]:
                tier = random.choice(["enterprise", "strategic"])  # Higher tier for regulated industries
            elif i < len(CLIENT_INDUSTRIES):  # First client of each industry
                tier = "enterprise"  # Ensure at least one enterprise client per industry
            else:
                tier = random.choice(CLIENT_TIERS)
            
            annual_value = (random.randint(500000, 5000000) if tier == "mid-market" 
                          else random.randint(1000000, 10000000))
            
            # Assign primary region based on industry and randomization
            if client_info["industry"] == "Government" and "Federal" in client_info["name"]:
                primary_region = "AMERICAS"
            else:
                primary_region = random.choice(REGIONS)
            
            # Set support tier based on client tier
            support_tier = random.choice(SUPPORT_TIERS[tier])
            
            client = {
                "id": f"client_{i+1}",
                "name": client_info["name"],
                "industry": client_info["industry"],
                "tier": tier,
                "annual_value": annual_value,
                "mrr": round(annual_value / 12, 2),
                "data_volume_gb": random.randint(100, 50000),
                "active_users": random.randint(10, 5000),
                "support_tier": support_tier,
                "primary_region": primary_region,
                "time_zone_preferences": random.sample(
                    REGION_TIMEZONE_MAP[primary_region], 
                    k=random.randint(1, 3)
                ),
                "relationship_start": generate_date_range(1095, 180)  # 3 years to 6 months ago
            }
            clients.append(client)
        
        return clients