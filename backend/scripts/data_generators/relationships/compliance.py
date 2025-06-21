from typing import List, Dict, Any
import random
from faker import Faker
from ..base import BaseGenerator

fake = Faker()


class OfficeComplianceGenerator(BaseGenerator):
    """Generate office-compliance framework relationships"""
    
    def __init__(self, offices: List[Dict[str, Any]], compliance_frameworks: List[Dict[str, Any]]):
        self.offices = offices
        self.compliance_frameworks = compliance_frameworks
    
    def generate(self) -> List[Dict[str, Any]]:
        relationships = []
        
        # Map offices to their applicable compliance frameworks based on region
        for office in self.offices:
            applicable_frameworks = []
            
            # GDPR for EU offices
            if office["region"] == "EMEA" and office["country"] in ["United Kingdom", "Germany", "France"]:
                applicable_frameworks.append("comp_gdpr")
            
            # CCPA for California (San Francisco office)
            if office["id"] == "office_1":
                applicable_frameworks.append("comp_ccpa")
            
            # SOC2 for all offices (company-wide)
            applicable_frameworks.append("comp_soc2")
            
            # APPI for Japan
            if office["country"] == "Japan":
                applicable_frameworks.append("comp_appi")
            
            # PIPEDA for Canada (if we had Canadian offices)
            # LGPD for Brazil (if we had Brazilian offices)
            
            for framework_id in applicable_frameworks:
                relationships.append({
                    "office_id": office["id"],
                    "compliance_id": framework_id,
                    "since": "2022-01-01",
                    "attestation_date": "2023-12-15",
                    "next_audit": "2024-12-15"
                })
        
        return relationships


class ClientComplianceGenerator(BaseGenerator):
    """Generate client compliance requirement relationships"""
    
    def __init__(self, clients: List[Dict[str, Any]], compliance_frameworks: List[Dict[str, Any]]):
        self.clients = clients
        self.compliance_frameworks = compliance_frameworks
    
    def generate(self) -> List[Dict[str, Any]]:
        relationships = []
        
        # Different clients require different compliance based on their industry
        for client in self.clients:
            required_frameworks = []
            
            # Healthcare clients need HIPAA
            if client["industry"] == "Healthcare":
                required_frameworks.append({
                    "framework_id": "comp_hipaa",
                    "contractual": True,
                    "sla_impact": "critical"
                })
            
            # Pharmaceutical clients also need HIPAA for patient data
            if client["industry"] == "Pharmaceutical":
                required_frameworks.append({
                    "framework_id": "comp_hipaa",
                    "contractual": True,
                    "sla_impact": "high"
                })
            
            # Financial services need PCI-DSS and SOC2
            if client["industry"] in ["Financial Services", "Insurance"]:
                required_frameworks.extend([
                    {"framework_id": "comp_pci_dss", "contractual": True, "sla_impact": "high"},
                    {"framework_id": "comp_soc2", "contractual": True, "sla_impact": "critical"}
                ])
            
            # Government clients need strict compliance
            if client["industry"] == "Government":
                required_frameworks.extend([
                    {"framework_id": "comp_soc2", "contractual": True, "sla_impact": "critical"},
                    {"framework_id": "comp_gdpr", "contractual": False, "sla_impact": "medium"}  # For citizen data
                ])
            
            # Education clients handling student data
            if client["industry"] == "Education":
                required_frameworks.append({
                    "framework_id": "comp_soc2",
                    "contractual": True,
                    "sla_impact": "high"
                })
            
            # EU-based clients need GDPR
            # For this example, randomly assign some clients as EU-based
            if random.choice([True, False]) and client["tier"] in ["enterprise", "strategic"]:
                if not any(f["framework_id"] == "comp_gdpr" for f in required_frameworks):
                    required_frameworks.append({
                        "framework_id": "comp_gdpr",
                        "contractual": True,
                        "sla_impact": "critical"
                    })
            
            # All enterprise clients require SOC2
            if client["tier"] == "enterprise":
                if not any(f["framework_id"] == "comp_soc2" for f in required_frameworks):
                    required_frameworks.append({
                        "framework_id": "comp_soc2",
                        "contractual": True,
                        "sla_impact": "high"
                    })
            
            for req in required_frameworks:
                relationships.append({
                    "client_id": client["id"],
                    "compliance_id": req["framework_id"],
                    "contractual": req["contractual"],
                    "sla_impact": req["sla_impact"]
                })
        
        return relationships


class OfficeDataResidencyGenerator(BaseGenerator):
    """Generate office data residency enforcement relationships"""
    
    def __init__(self, offices: List[Dict[str, Any]], data_residency_zones: List[Dict[str, Any]]):
        self.offices = offices
        self.data_residency_zones = data_residency_zones
    
    def generate(self) -> List[Dict[str, Any]]:
        relationships = []
        
        # Map offices to their data residency zones
        office_to_dr_zone = {
            "office_1": "dr_us",      # San Francisco
            "office_2": "dr_us",      # New York
            "office_3": "dr_uk",      # London
            "office_4": "dr_eu",      # Frankfurt
            "office_5": "dr_eu",      # Paris
            "office_6": "dr_apac",    # Tokyo
            "office_7": "dr_apac",    # Hong Kong
            "office_8": "dr_apac"     # Sydney
        }
        
        for office_id, dr_zone_id in office_to_dr_zone.items():
            relationships.append({
                "office_id": office_id,
                "data_residency_id": dr_zone_id
            })
        
        return relationships


class HolidayOfficeRelationshipGenerator(BaseGenerator):
    """Generate holiday-office observance relationships"""
    
    def __init__(self, holidays: List[Dict[str, Any]], offices: List[Dict[str, Any]]):
        self.holidays = holidays
        self.offices = offices
    
    def generate(self) -> List[Dict[str, Any]]:
        # This is handled directly in the holiday entity which has offices list
        # Return empty list as relationships are created directly in seeder
        return []


class OfficeCollaborationGenerator(BaseGenerator):
    """Generate office collaboration relationships based on timezone overlap"""
    
    def __init__(self, offices: List[Dict[str, Any]]):
        self.offices = offices
    
    def generate(self) -> List[Dict[str, Any]]:
        relationships = []
        
        # Create office collaboration relationships based on timezone overlap
        office_pairs = [
            ("office_1", "office_2", 3),      # SF-NY: 3 hours overlap
            ("office_2", "office_3", 4),      # NY-London: 4 hours overlap
            ("office_3", "office_4", 8),      # London-Frankfurt: Full overlap
            ("office_3", "office_5", 8),      # London-Paris: Full overlap
            ("office_4", "office_5", 8),      # Frankfurt-Paris: Full overlap
            ("office_6", "office_7", 7),      # Tokyo-HK: 7 hours overlap
            ("office_7", "office_8", 5),      # HK-Sydney: 5 hours overlap
            ("office_1", "office_8", 2),      # SF-Sydney: 2 hours overlap (across date line)
            ("office_3", "office_7", 1),      # London-HK: 1 hour overlap
        ]
        
        for office1_id, office2_id, overlap_hours in office_pairs:
            # Bidirectional relationships
            relationships.append({
                "office1_id": office1_id,
                "office2_id": office2_id,
                "overlap_hours": overlap_hours,
                "preferred_meeting_times": [f"{10+i}:00" for i in range(overlap_hours)]  # Starting from 10am
            })
            relationships.append({
                "office1_id": office2_id,
                "office2_id": office1_id,
                "overlap_hours": overlap_hours,
                "preferred_meeting_times": [f"{10+i}:00" for i in range(overlap_hours)]
            })
        
        return relationships