from typing import List, Dict, Any
import random
from datetime import datetime, timedelta
from faker import Faker
from ..base import BaseGenerator
from ..config import REGIONS

fake = Faker()


class SchedulesGenerator(BaseGenerator):
    """Generate 24/7 on-call schedule data for global operations"""
    
    def generate(self) -> List[Dict[str, Any]]:
        schedules = []
        schedule_id = 1
        
        # Define schedule types and patterns
        schedule_types = [
            {"type": "on_call", "coverage_type": "primary", "recurring_pattern": "weekly"},
            {"type": "on_call", "coverage_type": "backup", "recurring_pattern": "weekly"},
            {"type": "on_call", "coverage_type": "escalation", "recurring_pattern": "weekly"},
            {"type": "maintenance", "coverage_type": "primary", "recurring_pattern": "weekly"},
            {"type": "coverage", "coverage_type": "primary", "recurring_pattern": "daily"}
        ]
        
        # Define basic office info for scheduling
        offices_info = [
            {"id": "office_1", "timezone": "America/Los_Angeles", "region": "AMERICAS"},
            {"id": "office_2", "timezone": "America/New_York", "region": "AMERICAS"},
            {"id": "office_3", "timezone": "Europe/London", "region": "EMEA"},
            {"id": "office_4", "timezone": "Europe/Berlin", "region": "EMEA"},
            {"id": "office_5", "timezone": "Europe/Paris", "region": "EMEA"},
            {"id": "office_6", "timezone": "Asia/Tokyo", "region": "APAC"},
            {"id": "office_7", "timezone": "Asia/Hong_Kong", "region": "APAC"},
            {"id": "office_8", "timezone": "Australia/Sydney", "region": "APAC"}
        ]
        
        # Generate schedules for each office and type
        base_date = datetime(2024, 1, 1)
        
        for office in offices_info:
            for schedule_type in schedule_types:
                # Create 12 weeks of schedules for each type (3 months)
                for week in range(12):
                    start_date = base_date + timedelta(weeks=week)
                    
                    # On-call schedules are weekly rotations
                    if schedule_type["recurring_pattern"] == "weekly":
                        end_date = start_date + timedelta(days=7)
                    else:  # Daily coverage schedules
                        # Create daily schedules for the week
                        for day in range(7):
                            day_start = start_date + timedelta(days=day)
                            schedules.append({
                                "id": f"schedule_{schedule_id}",
                                "type": schedule_type["type"],
                                "timezone": office["timezone"],
                                "start_datetime": day_start.isoformat(),
                                "end_datetime": (day_start + timedelta(days=1)).isoformat(),
                                "recurring_pattern": schedule_type["recurring_pattern"],
                                "coverage_type": schedule_type["coverage_type"],
                                "office_id": office["id"],
                                "region": office["region"]
                            })
                            schedule_id += 1
                        continue
                    
                    schedules.append({
                        "id": f"schedule_{schedule_id}",
                        "type": schedule_type["type"],
                        "timezone": office["timezone"],
                        "start_datetime": start_date.isoformat(),
                        "end_datetime": end_date.isoformat(),
                        "recurring_pattern": schedule_type["recurring_pattern"],
                        "coverage_type": schedule_type["coverage_type"],
                        "office_id": office["id"],
                        "region": office["region"]
                    })
                    schedule_id += 1
        
        # Add special schedules for P0 incident coverage (24/7)
        for region in REGIONS:
            # Create P0 escalation schedules with 4-hour shifts for follow-the-sun coverage
            for week in range(12):
                week_start = base_date + timedelta(weeks=week)
                for day in range(7):
                    day_start = week_start + timedelta(days=day)
                    # 6 shifts per day (4 hours each)
                    for shift in range(6):
                        shift_start = day_start + timedelta(hours=shift*4)
                        schedules.append({
                            "id": f"schedule_{schedule_id}",
                            "type": "on_call",
                            "timezone": "UTC",  # P0 schedules in UTC for global coordination
                            "start_datetime": shift_start.isoformat(),
                            "end_datetime": (shift_start + timedelta(hours=4)).isoformat(),
                            "recurring_pattern": "daily",
                            "coverage_type": "p0_escalation",
                            "office_id": None,  # Cross-office coverage
                            "region": region,
                            "severity_focus": "P0"
                        })
                        schedule_id += 1
        
        return schedules


class IncidentsGenerator(BaseGenerator):
    """Generate historical incident data with P0-P3 severities"""
    
    def generate(self) -> List[Dict[str, Any]]:
        incidents = []
        incident_id = 1
        
        # Incident templates by severity
        incident_types = {
            "P0": [
                {"desc": "Complete platform outage", "services": ["api", "database", "web"], "mttr_range": (30, 120)},
                {"desc": "Data pipeline failure affecting all customers", "services": ["data_pipeline", "etl"], "mttr_range": (45, 180)},
                {"desc": "Authentication service down", "services": ["auth", "sso"], "mttr_range": (15, 90)},
                {"desc": "Critical data corruption detected", "services": ["database", "storage"], "mttr_range": (60, 240)},
                {"desc": "Security breach detected", "services": ["security", "monitoring"], "mttr_range": (30, 360)}
            ],
            "P1": [
                {"desc": "API degradation affecting 30% of requests", "services": ["api"], "mttr_range": (20, 90)},
                {"desc": "Significant query performance degradation", "services": ["database", "analytics"], "mttr_range": (30, 120)},
                {"desc": "Partial data pipeline failure", "services": ["data_pipeline"], "mttr_range": (25, 100)},
                {"desc": "Customer dashboard loading issues", "services": ["web", "frontend"], "mttr_range": (15, 60)},
                {"desc": "Real-time analytics delay >5 minutes", "services": ["streaming", "analytics"], "mttr_range": (20, 80)}
            ],
            "P2": [
                {"desc": "Non-critical feature unavailable", "services": ["web"], "mttr_range": (60, 480)},
                {"desc": "Scheduled job failures", "services": ["scheduler", "jobs"], "mttr_range": (45, 240)},
                {"desc": "Reporting dashboard slow response", "services": ["reporting", "analytics"], "mttr_range": (30, 180)},
                {"desc": "Email notifications delayed", "services": ["notifications", "email"], "mttr_range": (60, 360)},
                {"desc": "Documentation site intermittent errors", "services": ["docs", "web"], "mttr_range": (120, 720)}
            ],
            "P3": [
                {"desc": "UI cosmetic issues", "services": ["frontend"], "mttr_range": (240, 2880)},
                {"desc": "Non-critical monitoring alerts", "services": ["monitoring"], "mttr_range": (180, 1440)},
                {"desc": "Legacy API deprecation warnings", "services": ["api"], "mttr_range": (360, 2880)},
                {"desc": "Minor documentation errors", "services": ["docs"], "mttr_range": (480, 4320)},
                {"desc": "Low-priority feature requests", "services": ["product"], "mttr_range": (720, 10080)}
            ]
        }
        
        # Regional distribution for incidents
        regions = [
            {"region": "AMERICAS", "offices": ["office_sf", "office_ny"], "weight": 0.4},
            {"region": "EMEA", "offices": ["office_london", "office_frankfurt"], "weight": 0.35},
            {"region": "APAC", "offices": ["office_singapore", "office_tokyo", "office_sydney", "office_bangalore"], "weight": 0.25}
        ]
        
        # Generate incidents over the past 90 days
        base_date = datetime.now() - timedelta(days=90)
        
        # Severity distribution: P0: 5%, P1: 15%, P2: 35%, P3: 45%
        severity_distribution = [
            ("P0", 5, 0.05),
            ("P1", 15, 0.15),
            ("P2", 35, 0.35),
            ("P3", 45, 0.45)
        ]
        
        # Generate ~100 incidents over 90 days
        for _ in range(100):
            # Select severity based on distribution
            severity = random.choices(
                [s[0] for s in severity_distribution],
                weights=[s[2] for s in severity_distribution]
            )[0]
            
            # Select incident type
            incident_template = random.choice(incident_types[severity])
            
            # Select affected regions (P0 often affects multiple regions)
            if severity == "P0" and random.random() < 0.6:
                # 60% chance P0 affects multiple regions
                num_regions = random.randint(2, 3)
                affected_regions = random.sample([r["region"] for r in regions], num_regions)
            else:
                # Other severities usually affect single region
                region = random.choices(regions, weights=[r["weight"] for r in regions])[0]
                affected_regions = [region["region"]]
            
            # Generate random timestamp within the past 90 days
            days_ago = random.uniform(0, 90)
            hours_offset = random.uniform(0, 24)
            created_at = base_date + timedelta(days=days_ago, hours=hours_offset)
            
            # Calculate MTTR based on severity
            mttr_minutes = random.randint(*incident_template["mttr_range"])
            resolved_at = created_at + timedelta(minutes=mttr_minutes)
            
            # Add some unresolved recent incidents
            if days_ago < 2 and severity in ["P2", "P3"] and random.random() < 0.2:
                resolved_at = None
                status = "open"
                mttr_minutes = None
            else:
                status = "resolved"
            
            incidents.append({
                "id": f"incident_{incident_id}",
                "severity": severity,
                "status": status,
                "description": incident_template["desc"],
                "affected_regions": affected_regions,
                "affected_services": incident_template["services"],
                "created_at": created_at.isoformat(),
                "resolved_at": resolved_at.isoformat() if resolved_at else None,
                "mttr_minutes": mttr_minutes,
                "root_cause": random.choice([
                    "Configuration change",
                    "Infrastructure failure", 
                    "Code deployment",
                    "Third-party service outage",
                    "Capacity exceeded",
                    "Network issues",
                    "Human error",
                    "Unknown"
                ]) if status == "resolved" else None
            })
            incident_id += 1
        
        # Sort incidents by created_at for realistic ordering
        incidents.sort(key=lambda x: x["created_at"])
        
        return incidents


class VisasGenerator(BaseGenerator):
    """Generate visa and work authorization data for global workforce"""
    
    def generate(self) -> List[Dict[str, Any]]:
        visas = []
        visa_id = 1
        
        # Common visa types by country
        visa_types = {
            "United States": [
                {"type": "H-1B", "name": "Specialty Occupation Work Visa", "max_duration_years": 6},
                {"type": "L-1A", "name": "Intracompany Transferee Executive", "max_duration_years": 7},
                {"type": "L-1B", "name": "Intracompany Transferee Specialized Knowledge", "max_duration_years": 5},
                {"type": "O-1", "name": "Extraordinary Ability Work Visa", "max_duration_years": 3},
                {"type": "TN", "name": "NAFTA Professional Work Visa", "max_duration_years": 3},
                {"type": "Green Card", "name": "Permanent Resident Card", "max_duration_years": 10}
            ],
            "United Kingdom": [
                {"type": "Skilled Worker", "name": "Skilled Worker Visa", "max_duration_years": 5},
                {"type": "ICT", "name": "Intra-company Transfer Visa", "max_duration_years": 5},
                {"type": "Global Talent", "name": "Global Talent Visa", "max_duration_years": 5},
                {"type": "ILR", "name": "Indefinite Leave to Remain", "max_duration_years": 0}  # Permanent
            ],
            "Germany": [
                {"type": "EU Blue Card", "name": "EU Blue Card", "max_duration_years": 4},
                {"type": "ICT Card", "name": "Intra-Corporate Transfer Card", "max_duration_years": 3},
                {"type": "Employment Visa", "name": "Employment Visa", "max_duration_years": 3},
                {"type": "Permanent Residence", "name": "Niederlassungserlaubnis", "max_duration_years": 0}
            ],
            "France": [
                {"type": "Passeport Talent", "name": "Talent Passport", "max_duration_years": 4},
                {"type": "ICT Permit", "name": "Intra-Company Transfer Permit", "max_duration_years": 3},
                {"type": "EU Blue Card", "name": "EU Blue Card France", "max_duration_years": 4}
            ],
            "Japan": [
                {"type": "Engineer/Specialist", "name": "Engineer/Specialist in Humanities", "max_duration_years": 5},
                {"type": "Highly Skilled Professional", "name": "Highly Skilled Professional Visa", "max_duration_years": 5},
                {"type": "Intra-company Transferee", "name": "Intra-company Transferee", "max_duration_years": 5},
                {"type": "Permanent Resident", "name": "Permanent Resident", "max_duration_years": 0}
            ],
            "Australia": [
                {"type": "TSS 482", "name": "Temporary Skill Shortage Visa", "max_duration_years": 4},
                {"type": "186 ENS", "name": "Employer Nomination Scheme", "max_duration_years": 0},  # Permanent
                {"type": "189", "name": "Skilled Independent Visa", "max_duration_years": 0},
                {"type": "494", "name": "Skilled Employer Sponsored Regional", "max_duration_years": 5}
            ],
            "Hong Kong": [
                {"type": "Employment Visa", "name": "General Employment Policy", "max_duration_years": 3},
                {"type": "QMAS", "name": "Quality Migrant Admission Scheme", "max_duration_years": 8},
                {"type": "Right of Abode", "name": "Right of Abode", "max_duration_years": 0}
            ]
        }
        
        # Generate visas for different scenarios
        now = datetime.now()
        
        # US H-1B visas (common for tech workers)
        for i in range(50):
            issued_date = now - timedelta(days=random.randint(30, 1095))  # 1 month to 3 years ago
            visa_type_info = random.choice(visa_types["United States"][:3])  # Work visas only
            
            visas.append({
                "id": f"visa_{visa_id}",
                "type": visa_type_info["type"],
                "name": visa_type_info["name"],
                "country": "United States",
                "issued_date": issued_date.strftime("%Y-%m-%d"),
                "expiry_date": (issued_date + timedelta(days=365 * 3)).strftime("%Y-%m-%d"),  # 3 year validity
                "restrictions": ["Single employer", "Requires sponsorship"],
                "allows_client_site": True,
                "max_duration_years": visa_type_info["max_duration_years"],
                "renewable": True
            })
            visa_id += 1
        
        # UK Skilled Worker visas
        for i in range(30):
            issued_date = now - timedelta(days=random.randint(30, 730))
            visa_type_info = visa_types["United Kingdom"][0]
            
            visas.append({
                "id": f"visa_{visa_id}",
                "type": visa_type_info["type"],
                "name": visa_type_info["name"],
                "country": "United Kingdom",
                "issued_date": issued_date.strftime("%Y-%m-%d"),
                "expiry_date": (issued_date + timedelta(days=365 * 5)).strftime("%Y-%m-%d"),
                "restrictions": ["Tied to sponsor", "Minimum salary requirement"],
                "allows_client_site": True,
                "max_duration_years": visa_type_info["max_duration_years"],
                "renewable": True
            })
            visa_id += 1
        
        # EU Blue Cards (Germany, France)
        for country in ["Germany", "France"]:
            for i in range(20):
                issued_date = now - timedelta(days=random.randint(30, 730))
                visa_type_info = next(v for v in visa_types[country] if "Blue Card" in v["name"])
                
                visas.append({
                    "id": f"visa_{visa_id}",
                    "type": visa_type_info["type"],
                    "name": visa_type_info["name"],
                    "country": country,
                    "issued_date": issued_date.strftime("%Y-%m-%d"),
                    "expiry_date": (issued_date + timedelta(days=365 * 4)).strftime("%Y-%m-%d"),
                    "restrictions": ["Highly qualified employment", "Minimum salary threshold"],
                    "allows_client_site": True,
                    "max_duration_years": visa_type_info["max_duration_years"],
                    "renewable": True
                })
                visa_id += 1
        
        # APAC visas (Japan, Australia, Hong Kong)
        for country in ["Japan", "Australia", "Hong Kong"]:
            for i in range(15):
                issued_date = now - timedelta(days=random.randint(30, 730))
                visa_type_info = random.choice(visa_types[country][:2])
                
                duration_years = 3 if visa_type_info["max_duration_years"] > 0 else 10
                restrictions = []
                if country == "Japan":
                    restrictions = ["Company sponsorship required", "Residence card required"]
                elif country == "Australia":
                    restrictions = ["Employer nomination required", "Skills assessment required"]
                else:
                    restrictions = ["Local sponsor required"]
                
                visas.append({
                    "id": f"visa_{visa_id}",
                    "type": visa_type_info["type"],
                    "name": visa_type_info["name"],
                    "country": country,
                    "issued_date": issued_date.strftime("%Y-%m-%d"),
                    "expiry_date": (issued_date + timedelta(days=365 * duration_years)).strftime("%Y-%m-%d"),
                    "restrictions": restrictions,
                    "allows_client_site": True,
                    "max_duration_years": visa_type_info["max_duration_years"],
                    "renewable": True
                })
                visa_id += 1
        
        # Some business visit visas
        business_visa_countries = ["United States", "China", "India", "Brazil", "Russia"]
        for country in business_visa_countries:
            for i in range(10):
                issued_date = now - timedelta(days=random.randint(30, 365))
                
                visas.append({
                    "id": f"visa_{visa_id}",
                    "type": "Business",
                    "name": "Business Visitor Visa",
                    "country": country,
                    "issued_date": issued_date.strftime("%Y-%m-%d"),
                    "expiry_date": (issued_date + timedelta(days=365 * 5)).strftime("%Y-%m-%d"),  # 5 year validity
                    "restrictions": ["No employment allowed", "Max 90 days per visit"],
                    "allows_client_site": True,
                    "max_duration_years": 0,  # Visit only
                    "renewable": False
                })
                visa_id += 1
        
        # Some permanent residencies
        pr_countries = ["United States", "United Kingdom", "Germany", "Australia", "Japan"]
        for country in pr_countries:
            for i in range(5):
                issued_date = now - timedelta(days=random.randint(365, 1825))  # 1-5 years ago
                
                # Find the permanent visa type for this country
                pr_type = next((v for v in visa_types.get(country, []) if v["max_duration_years"] == 0), None)
                if pr_type:
                    visas.append({
                        "id": f"visa_{visa_id}",
                        "type": pr_type["type"],
                        "name": pr_type["name"],
                        "country": country,
                        "issued_date": issued_date.strftime("%Y-%m-%d"),
                        "expiry_date": (issued_date + timedelta(days=365 * 10)).strftime("%Y-%m-%d"),  # 10 year card
                        "restrictions": [],
                        "allows_client_site": True,
                        "max_duration_years": 0,
                        "renewable": True
                    })
                    visa_id += 1
        
        return visas
