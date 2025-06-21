from typing import List, Dict, Any
import random
from faker import Faker
from ..base import BaseGenerator

fake = Faker()


class PersonSkillGenerator(BaseGenerator):
    """Generate person-skill relationships"""
    
    def __init__(self, people: List[Dict[str, Any]], skills: List[Dict[str, Any]]):
        self.people = people
        self.skills = skills
    
    def generate(self) -> List[Dict[str, Any]]:
        relationships = []
        
        # Assign skills to people based on their role and department
        for person in self.people:
            num_skills = random.randint(3, 8)
            
            # Core skills based on department
            if person["department"] in ["Data Platform Engineering", "Analytics Engineering"]:
                core_skills = ["skill_1", "skill_6", "skill_12", "skill_13", "skill_14", "skill_15", "skill_16", "skill_17", "skill_18"]
            elif person["department"] == "Data Science":
                core_skills = ["skill_1", "skill_6", "skill_21", "skill_22", "skill_23", "skill_24", "skill_25"]
            elif person["department"] in ["Engineering", "Infrastructure & DevOps"]:
                core_skills = ["skill_1", "skill_2", "skill_3", "skill_4", "skill_5", "skill_26", "skill_27", "skill_28"]
            else:
                core_skills = ["skill_1", "skill_6", "skill_39", "skill_40", "skill_41"]
            
            # Add cloud skills for technical roles
            if person["department"] in ["Data Platform Engineering", "Engineering", "Infrastructure & DevOps", "Data Science"]:
                core_skills.extend(["skill_9", "skill_10", "skill_11"])
            
            selected_skills = random.sample(core_skills, min(num_skills, len(core_skills)))
            
            for skill_id in selected_skills:
                proficiency = random.choice(["beginner", "intermediate", "advanced", "expert"])
                years_exp = random.randint(1, min(10, person["years_experience"]))
                
                relationships.append({
                    "person_id": person["id"],
                    "skill_id": skill_id,
                    "proficiency_level": proficiency,
                    "years_experience": years_exp,
                    "last_used": fake.date_between(start_date='-6m', end_date='today').isoformat()
                })
        
        return relationships


class PersonSpecializationGenerator(BaseGenerator):
    """Generate person specialization relationships"""
    
    def __init__(self, people: List[Dict[str, Any]]):
        self.people = people
    
    def generate(self) -> List[Dict[str, Any]]:
        relationships = []
        
        # Create specialization relationships
        for person in self.people:
            # 20% of people have specializations
            if random.random() < 0.2:
                if person["department"] in ["Data Platform Engineering", "Analytics Engineering"]:
                    specializations = ["Real-time Processing", "Data Governance", "Performance Optimization", "Data Modeling"]
                elif person["department"] == "Data Science":
                    specializations = ["Computer Vision", "NLP", "Time Series", "Recommender Systems", "MLOps"]
                elif person["department"] == "Engineering":
                    specializations = ["API Design", "Microservices", "Frontend Architecture", "Security"]
                else:
                    specializations = ["Process Improvement", "Strategic Planning", "Cross-functional Leadership"]
                
                spec = random.choice(specializations)
                relationships.append({
                    "person_id": person["id"],
                    "specialization": spec,
                    "expertise_level": random.choice(["recognized", "expert", "thought_leader"]),
                    "years_in_specialty": random.randint(2, 8)
                })
        
        return relationships


class PersonLanguageGenerator(BaseGenerator):
    """Generate person-language relationships"""
    
    def __init__(self, people: List[Dict[str, Any]], languages: List[Dict[str, Any]], 
                 person_office_assignments: List[Dict[str, Any]]):
        self.people = people
        self.languages = languages
        self.person_office_assignments = person_office_assignments
    
    def generate(self) -> List[Dict[str, Any]]:
        relationships = []
        
        # Language mapping based on office/location
        office_language_map = {
            "office_sf": ["lang_en", "lang_es"],  # English + Spanish common in California
            "office_ny": ["lang_en", "lang_es"],   # English + Spanish common in NY
            "office_london": ["lang_en"],
            "office_frankfurt": ["lang_de", "lang_en"],
            "office_paris": ["lang_fr", "lang_en"],
            "office_tokyo": ["lang_ja", "lang_en"],
            "office_hk": ["lang_zh", "lang_en"],
            "office_sydney": ["lang_en"]
        }
        
        for person_office in self.person_office_assignments:
            person_id = person_office["person_id"]
            office_id = person_office["office_id"]
            office_languages = office_language_map.get(office_id, ["lang_en"])
            
            # Everyone speaks at least one language
            primary_lang = office_languages[0]
            relationships.append({
                "person_id": person_id,
                "language_id": primary_lang,
                "proficiency": "native" if primary_lang != "lang_en" else random.choice(["native", "fluent"]),
                "is_primary": True,
                "certified": False,
                "certification_date": None
            })
            
            # English as secondary language for non-English primary speakers
            if primary_lang != "lang_en":
                relationships.append({
                    "person_id": person_id,
                    "language_id": "lang_en",
                    "proficiency": random.choice(["fluent", "professional", "professional"]),  # Most are professional
                    "is_primary": False,
                    "certified": random.random() < 0.3,  # 30% have certification
                    "certification_date": fake.date_between(start_date='-5y', end_date='today').isoformat() if random.random() < 0.3 else None
                })
            
            # 20% of people speak an additional language
            if random.random() < 0.2:
                additional_langs = ["lang_es", "lang_fr", "lang_de", "lang_zh", "lang_ja", "lang_ko", "lang_pt", "lang_it", "lang_ru", "lang_ar", "lang_hi"]
                # Remove languages they already speak
                existing_langs = [rel["language_id"] for rel in relationships if rel["person_id"] == person_id]
                available_langs = [lang for lang in additional_langs if lang not in existing_langs]
                
                if available_langs:
                    additional_lang = random.choice(available_langs)
                    relationships.append({
                        "person_id": person_id,
                        "language_id": additional_lang,
                        "proficiency": random.choice(["basic", "professional", "fluent"]),
                        "is_primary": False,
                        "certified": False,
                        "certification_date": None
                    })
        
        return relationships


class PersonExpertInGenerator(BaseGenerator):
    """Generate person expertise in platform components"""
    
    def __init__(self, people: List[Dict[str, Any]], platform_components: List[Dict[str, Any]]):
        self.people = people
        self.platform_components = platform_components
    
    def generate(self) -> List[Dict[str, Any]]:
        relationships = []
        
        # Engineers and architects have expertise in specific components
        technical_people = [p for p in self.people if any(role in p["role"] for role in 
                           ["Engineer", "Architect", "Developer", "Scientist", "DevOps", "SRE"])]
        
        for person in technical_people:
            # Number of components they're expert in depends on seniority
            if "Principal" in person["role"] or "Staff" in person["role"]:
                num_expertises = random.randint(3, 6)
            elif "Senior" in person["role"]:
                num_expertises = random.randint(2, 4)
            else:
                num_expertises = random.randint(1, 2)
            
            # Select components based on their role/department
            if "Data" in person["department"]:
                relevant_components = [c for c in self.platform_components if 
                                     any(word in c["name"] for word in ["Data", "Pipeline", "Lake", "Stream", "Batch"])]
            elif "ML" in person["role"] or "Data Science" in person["department"]:
                relevant_components = [c for c in self.platform_components if 
                                     any(word in c["name"] for word in ["ML", "Model", "Feature", "Analytics"])]
            elif "Infrastructure" in person["department"] or "DevOps" in person["role"]:
                relevant_components = [c for c in self.platform_components if 
                                     c["type"] in ["database", "service"] or "Infrastructure" in c["name"]]
            else:
                relevant_components = self.platform_components
            
            if relevant_components:
                expert_components = random.sample(relevant_components, 
                                               min(num_expertises, len(relevant_components)))
                for component in expert_components:
                    # Expertise level based on seniority
                    if "Principal" in person["role"] or "Staff" in person["role"]:
                        expertise_level = random.randint(4, 5)
                    elif "Senior" in person["role"]:
                        expertise_level = random.randint(3, 4)
                    else:
                        expertise_level = random.randint(1, 3)
                    
                    relationships.append({
                        "person_id": person["id"],
                        "component_id": component["id"],
                        "expertise_level": expertise_level
                    })
        
        return relationships