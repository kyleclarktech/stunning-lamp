"""Database seeder orchestrator."""

from typing import Dict, List, Any
from datetime import datetime
import json
from ..base import escape_string
from .connection import DatabaseConnection
from .indexes import IndexCreator


class DatabaseSeeder:
    """Orchestrates the database seeding process."""
    
    def __init__(self, connection: DatabaseConnection):
        self.connection = connection
        self.db = connection.db
        self.index_creator = IndexCreator(connection)
    
    def seed(self, data: Dict[str, Any]) -> None:
        """Seed the database with all data."""
        print("🌱 Seeding database with test data...")
        
        # Clear existing data
        self.connection.clear_graph()
        
        # Create indexes
        self.index_creator.create_all_indexes()
        
        # Create nodes
        self._create_people(data["people"])
        self._create_teams(data["teams"])
        self._create_groups(data["groups"])
        self._create_policies(data["policies"])
        self._create_skills(data["skills"])
        self._create_clients(data["clients"])
        self._create_projects(data["projects"])
        self._create_sprints(data["sprints"])
        self._create_offices(data["offices"])
        self._create_languages(data["languages"])
        self._create_holidays(data["holidays"])
        self._create_compliance(data["compliance"])
        self._create_data_residency(data["data_residency"])
        self._create_cloud_regions(data["cloud_regions"])
        self._create_platform_components(data["platform_components"])
        self._create_schedules(data["schedules"])
        self._create_incidents(data["incidents"])
        self._create_visas(data["visas"])
        self._create_metrics(data["metrics"])
        
        # Create relationships
        self._create_relationships(data["relationships"])
        
        # Store statistics
        self._store_statistics(data)
        
        self._print_summary(data)
    
    def _create_people(self, people: List[Dict[str, Any]]) -> None:
        """Create Person nodes."""
        for person in people:
            query = f"""CREATE (p:Person {{
                id: '{person['id']}',
                name: '{escape_string(person['name'])}',
                email: '{person['email']}',
                department: '{person['department']}',
                role: '{escape_string(person['role'])}',
                seniority: '{person['seniority']}',
                hire_date: '{person['hire_date']}',
                location: '{person['location']}',
                timezone: '{person['timezone']}',
                capacity_hours_per_week: {person['capacity_hours_per_week']},
                current_utilization: {person['current_utilization']},
                billing_rate: {person['billing_rate']},
                years_experience: {person['years_experience']},
                manager_id: '{person.get('manager_id', '')}'
            }})"""
            self.db.query(query)
    
    def _create_teams(self, teams: List[Dict[str, Any]]) -> None:
        """Create Team nodes."""
        for team in teams:
            query = f"""CREATE (t:Team {{
                id: '{team['id']}',
                name: '{escape_string(team['name'])}',
                department: '{team['department']}',
                focus: '{escape_string(team['focus'])}'
            }})"""
            self.db.query(query)
    
    def _create_groups(self, groups: List[Dict[str, Any]]) -> None:
        """Create Group nodes."""
        for group in groups:
            query = f"""CREATE (g:Group {{
                id: '{group['id']}',
                name: '{escape_string(group['name'])}',
                description: '{escape_string(group['description'])}',
                type: '{group['type']}',
                lead_department: '{group['lead_department']}'
            }})"""
            self.db.query(query)
    
    def _create_policies(self, policies: List[Dict[str, Any]]) -> None:
        """Create Policy nodes."""
        for policy in policies:
            frameworks = ','.join(policy['compliance_frameworks'])
            query = f"""CREATE (p:Policy {{
                id: '{policy['id']}',
                name: '{escape_string(policy['name'])}',
                description: '{escape_string(policy['description'])}',
                category: '{policy['category']}',
                severity: '{policy['severity']}',
                responsible_type: '{policy['responsible_type']}',
                compliance_frameworks: '{frameworks}'
            }})"""
            self.db.query(query)
    
    def _create_skills(self, skills: List[Dict[str, Any]]) -> None:
        """Create Skill nodes."""
        for skill in skills:
            query = f"""CREATE (s:Skill {{
                id: '{skill['id']}',
                name: '{escape_string(skill['name'])}',
                category: '{skill['category']}',
                type: '{skill['type']}'
            }})"""
            self.db.query(query)
    
    def _create_clients(self, clients: List[Dict[str, Any]]) -> None:
        """Create Client nodes."""
        for client in clients:
            time_zones_str = ','.join(client['time_zone_preferences'])
            query = f"""CREATE (c:Client {{
                id: '{client['id']}',
                name: '{escape_string(client['name'])}',
                industry: '{client['industry']}',
                tier: '{client['tier']}',
                annual_value: {client['annual_value']},
                mrr: {client['mrr']},
                data_volume_gb: {client['data_volume_gb']},
                active_users: {client['active_users']},
                support_tier: '{client['support_tier']}',
                primary_region: '{client['primary_region']}',
                time_zone_preferences: '{time_zones_str}',
                relationship_start: '{client['relationship_start']}'
            }})"""
            self.db.query(query)
    
    def _create_projects(self, projects: List[Dict[str, Any]]) -> None:
        """Create Project nodes."""
        for project in projects:
            query = f"""CREATE (pr:Project {{
                id: '{project['id']}',
                name: '{escape_string(project['name'])}',
                type: '{project['type']}',
                status: '{project['status']}',
                start_date: '{project['start_date']}',
                end_date: '{project['end_date']}',
                budget: {project['budget']},
                priority: '{project['priority']}',
                client_id: '{project['client_id']}',
                description: '{escape_string(project['description'])}'
            }})"""
            self.db.query(query)
    
    def _create_sprints(self, sprints: List[Dict[str, Any]]) -> None:
        """Create Sprint nodes."""
        for sprint in sprints:
            velocity = sprint['velocity'] if sprint['velocity'] is not None else 0
            query = f"""CREATE (s:Sprint {{
                id: '{sprint['id']}',
                name: '{escape_string(sprint['name'])}',
                project_id: '{sprint['project_id']}',
                sprint_number: {sprint['sprint_number']},
                start_date: '{sprint['start_date']}',
                end_date: '{sprint['end_date']}',
                status: '{sprint['status']}',
                velocity: {velocity}
            }})"""
            self.db.query(query)
    
    def _create_offices(self, offices: List[Dict[str, Any]]) -> None:
        """Create Office nodes."""
        for office in offices:
            languages_str = ','.join(office['languages'])
            query = f"""CREATE (o:Office {{
                id: '{office['id']}',
                name: '{escape_string(office['name'])}',
                city: '{escape_string(office['city'])}',
                country: '{escape_string(office['country'])}',
                country_code: '{office['country_code']}',
                region: '{office['region']}',
                timezone: '{office['timezone']}',
                timezone_offset: {office['timezone_offset']},
                business_hours_start: '{office['business_hours_start']}',
                business_hours_end: '{office['business_hours_end']}',
                business_hours_start_utc: '{office['business_hours_start_utc']}',
                business_hours_end_utc: '{office['business_hours_end_utc']}',
                languages: '{languages_str}',
                currency: '{office['currency']}',
                data_residency_zone: '{office['data_residency_zone']}',
                is_headquarters: {str(office['is_headquarters']).lower()},
                established_date: '{office['established_date']}'
            }})"""
            self.db.query(query)
    
    def _create_languages(self, languages: List[Dict[str, Any]]) -> None:
        """Create Language nodes."""
        for language in languages:
            query = f"""CREATE (l:Language {{
                id: '{language['id']}',
                code: '{language['code']}',
                name: '{language['name']}',
                native_name: '{escape_string(language['native_name'])}',
                script: '{language['script']}',
                direction: '{language['direction']}',
                is_business_language: {str(language['is_business_language']).lower()}
            }})"""
            self.db.query(query)
    
    def _create_holidays(self, holidays: List[Dict[str, Any]]) -> None:
        """Create Holiday nodes."""
        for holiday in holidays:
            offices_str = ','.join(holiday.get('offices', []))
            # Use double quotes for name to handle apostrophes
            escaped_name = holiday['name'].replace("'", "\\'")
            query = f"""CREATE (h:Holiday {{
                id: '{holiday['id']}',
                name: "{escaped_name}",
                date: '{holiday['date']}',
                type: '{holiday['type']}',
                recurring: {str(holiday['recurring']).lower()},
                impact: '{holiday['impact']}',
                coverage_required: {str(holiday['coverage_required']).lower()},
                offices: '{offices_str}'
            }})"""
            self.db.query(query)
    
    def _create_compliance(self, frameworks: List[Dict[str, Any]]) -> None:
        """Create Compliance nodes."""
        for framework in frameworks:
            # Convert requirements dict to JSON string
            requirements_str = json.dumps(framework['requirements']) if isinstance(framework['requirements'], dict) else framework['requirements']
            penalties_str = json.dumps(framework['penalties']) if isinstance(framework['penalties'], dict) else framework['penalties']
            
            query = f"""CREATE (c:Compliance {{
                id: '{framework['id']}',
                framework: '{framework['framework']}',
                version: '{framework['version']}',
                jurisdiction: '{framework['jurisdiction']}',
                geographic_scope: '{','.join(framework['geographic_scope'])}',
                type: '{framework['type']}',
                requirements: '{escape_string(requirements_str)}',
                penalties: '{escape_string(penalties_str)}',
                effective_date: '{framework['effective_date']}',
                last_updated: '{framework['last_updated']}',
                status: '{framework['status']}'
            }})"""
            self.db.query(query)
    
    def _create_data_residency(self, zones: List[Dict[str, Any]]) -> None:
        """Create DataResidency nodes."""
        for zone in zones:
            countries_str = ','.join(zone['countries'])
            regulations_str = ','.join(zone['regulations'])
            locations_str = ','.join(zone['storage_locations'])
            restrictions_str = ','.join(zone['transfer_restrictions'])
            
            query = f"""CREATE (dr:DataResidency {{
                id: '{zone['id']}',
                zone: '{zone['zone']}',
                countries: '{countries_str}',
                regulations: '{regulations_str}',
                storage_locations: '{locations_str}',
                transfer_restrictions: '{restrictions_str}',
                encryption_required: {str(zone['encryption_required']).lower()}
            }})"""
            self.db.query(query)
    
    def _create_cloud_regions(self, regions: List[Dict[str, Any]]) -> None:
        """Create CloudRegion nodes."""
        for region in regions:
            query = f"""CREATE (cr:CloudRegion {{
                id: '{region['id']}',
                provider: '{region['provider']}',
                region_code: '{region['region_code']}',
                region_name: '{escape_string(region['region_name'])}',
                availability_zones: {region['availability_zones']},
                data_residency_zone: '{region['data_residency_zone']}'
            }})"""
            self.db.query(query)
    
    def _create_platform_components(self, components: List[Dict[str, Any]]) -> None:
        """Create PlatformComponent nodes."""
        for component in components:
            query = f"""CREATE (pc:PlatformComponent {{
                id: '{component['id']}',
                name: '{escape_string(component['name'])}',
                type: '{component['type']}',
                tier: '{component['tier']}',
                owner_team_id: '{component['owner_team_id']}',
                documentation_url: '{component['documentation_url']}'
            }})"""
            self.db.query(query)
    
    def _create_schedules(self, schedules: List[Dict[str, Any]]) -> None:
        """Create Schedule nodes."""
        for schedule in schedules:
            query = f"""CREATE (s:Schedule {{
                id: '{schedule['id']}',
                type: '{schedule['type']}',
                timezone: '{schedule['timezone']}',
                start_datetime: '{schedule['start_datetime']}',
                end_datetime: '{schedule['end_datetime']}',
                recurring_pattern: '{schedule.get('recurring_pattern', '')}',
                coverage_type: '{schedule['coverage_type']}',
                office_id: '{schedule.get('office_id', '')}',
                region: '{schedule['region']}',
                severity_focus: '{schedule.get('severity_focus', '')}'
            }})"""
            self.db.query(query)
    
    def _create_incidents(self, incidents: List[Dict[str, Any]]) -> None:
        """Create Incident nodes."""
        for incident in incidents:
            regions_str = ','.join(incident['affected_regions'])
            services_str = ','.join(incident['affected_services'])
            
            query = f"""CREATE (i:Incident {{
                id: '{incident['id']}',
                severity: '{incident['severity']}',
                status: '{incident['status']}',
                description: '{escape_string(incident['description'])}',
                affected_regions: '{regions_str}',
                affected_services: '{services_str}',
                created_at: '{incident['created_at']}',
                resolved_at: '{incident.get('resolved_at', '')}',
                mttr_minutes: {incident.get('mttr_minutes', 0)},
                root_cause: '{escape_string(incident.get('root_cause', ''))}'
            }})"""
            self.db.query(query)
    
    def _create_visas(self, visas: List[Dict[str, Any]]) -> None:
        """Create Visa nodes."""
        for visa in visas:
            restrictions_str = ','.join(visa.get('restrictions', []))
            
            query = f"""CREATE (v:Visa {{
                id: '{visa['id']}',
                type: '{visa['type']}',
                name: '{escape_string(visa['name'])}',
                country: '{visa['country']}',
                issued_date: '{visa['issued_date']}',
                expiry_date: '{visa['expiry_date']}',
                restrictions: '{restrictions_str}',
                allows_client_site: {str(visa['allows_client_site']).lower()},
                max_duration_years: {visa['max_duration_years']},
                renewable: {str(visa['renewable']).lower()}
            }})"""
            self.db.query(query)
    
    def _create_metrics(self, metrics: List[Dict[str, Any]]) -> None:
        """Create Metric nodes."""
        # Sample a subset of metrics to avoid overwhelming the database
        sample_size = min(1000, len(metrics))
        sampled_metrics = metrics[::len(metrics)//sample_size] if len(metrics) > sample_size else metrics
        
        for metric in sampled_metrics:
            query = f"""CREATE (m:Metric {{
                id: '{metric['id']}',
                type: '{metric['type']}',
                service: '{metric['service']}',
                region: '{metric['region']}',
                value: {metric['value']},
                unit: '{metric['unit']}',
                timestamp: '{metric['timestamp']}',
                percentile: {metric['percentile']}
            }})"""
            self.db.query(query)
    
    def _create_relationships(self, relationships: Dict[str, List[Dict[str, Any]]]) -> None:
        """Create all relationships."""
        print("🔗 Creating relationships...")
        
        # Person relationships
        for membership in relationships.get("person_team_memberships", []):
            query = f"""MATCH (p:Person {{id: '{membership['person_id']}'}}), (t:Team {{id: '{membership['team_id']}'}}) 
                       CREATE (p)-[:MEMBER_OF {{role: '{escape_string(membership['role'])}', is_lead: {str(membership['is_lead']).lower()}}}]->(t)"""
            self.db.query(query)
        
        for membership in relationships.get("person_group_memberships", []):
            query = f"""MATCH (p:Person {{id: '{membership['person_id']}'}}), (g:Group {{id: '{membership['group_id']}'}}) 
                       CREATE (p)-[:MEMBER_OF {{role: '{membership['role']}', joined_date: '{membership['joined_date']}'}}]->(g)"""
            self.db.query(query)
        
        # Policy responsibilities
        for responsibility in relationships.get("team_policy_responsibilities", []):
            query = f"""MATCH (t:Team {{id: '{responsibility['team_id']}'}}), (p:Policy {{id: '{responsibility['policy_id']}'}}) 
                       CREATE (t)-[:RESPONSIBLE_FOR {{responsibility_type: '{responsibility['responsibility_type']}', assigned_date: '{responsibility['assigned_date']}'}}]->(p)"""
            self.db.query(query)
        
        for responsibility in relationships.get("group_policy_responsibilities", []):
            query = f"""MATCH (g:Group {{id: '{responsibility['group_id']}'}}), (p:Policy {{id: '{responsibility['policy_id']}'}}) 
                       CREATE (g)-[:RESPONSIBLE_FOR {{responsibility_type: '{responsibility['responsibility_type']}', assigned_date: '{responsibility['assigned_date']}'}}]->(p)"""
            self.db.query(query)
        
        # Create manager relationships (REPORTS_TO)
        people = self.db.query("MATCH (p:Person) RETURN p").result_set
        for person_record in people:
            person = dict(person_record[0].properties)
            if person.get('manager_id'):
                query = f"""MATCH (p:Person {{id: '{person['id']}'}}), (m:Person {{id: '{person['manager_id']}'}}) 
                           CREATE (p)-[:REPORTS_TO]->(m)"""
                self.db.query(query)
        
        # Skill relationships
        for skill_rel in relationships.get("person_skills", []):
            query = f"""MATCH (p:Person {{id: '{skill_rel['person_id']}'}}), (s:Skill {{id: '{skill_rel['skill_id']}'}}) 
                       CREATE (p)-[:HAS_SKILL {{
                           proficiency_level: '{skill_rel['proficiency_level']}',
                           years_experience: {skill_rel['years_experience']},
                           last_used: '{skill_rel['last_used']}'
                       }}]->(s)"""
            self.db.query(query)
        
        # Project relationships
        for allocation in relationships.get("person_project_allocations", []):
            query = f"""MATCH (p:Person {{id: '{allocation['person_id']}'}}), (pr:Project {{id: '{allocation['project_id']}'}}) 
                       CREATE (p)-[:ALLOCATED_TO {{
                           allocation_percentage: {allocation['allocation_percentage']},
                           start_date: '{allocation['start_date']}',
                           end_date: '{allocation['end_date']}',
                           role_on_project: '{allocation['role_on_project']}'
                       }}]->(pr)"""
            self.db.query(query)
        
        for req in relationships.get("project_skill_requirements", []):
            query = f"""MATCH (pr:Project {{id: '{req['project_id']}'}}), (s:Skill {{id: '{req['skill_id']}'}}) 
                       CREATE (pr)-[:REQUIRES_SKILL {{
                           priority: '{req['priority']}',
                           min_proficiency_level: '{req['min_proficiency_level']}',
                           headcount_needed: {req['headcount_needed']}
                       }}]->(s)"""
            self.db.query(query)
        
        for delivery in relationships.get("team_project_delivery", []):
            query = f"""MATCH (t:Team {{id: '{delivery['team_id']}'}}), (pr:Project {{id: '{delivery['project_id']}'}}) 
                       CREATE (t)-[:DELIVERS {{
                           responsibility: '{delivery['responsibility']}',
                           committed_capacity: {delivery['committed_capacity']}
                       }}]->(pr)"""
            self.db.query(query)
        
        # Create project-client relationships
        projects = self.db.query("MATCH (p:Project) RETURN p").result_set
        for project_record in projects:
            project = dict(project_record[0].properties)
            query = f"""MATCH (pr:Project {{id: '{project['id']}'}}), (c:Client {{id: '{project['client_id']}'}}) 
                       CREATE (pr)-[:FOR_CLIENT]->(c)"""
            self.db.query(query)
        
        # Create sprint-project relationships
        sprints = self.db.query("MATCH (s:Sprint) RETURN s").result_set
        for sprint_record in sprints:
            sprint = dict(sprint_record[0].properties)
            query = f"""MATCH (s:Sprint {{id: '{sprint['id']}'}}), (pr:Project {{id: '{sprint['project_id']}'}}) 
                       CREATE (s)-[:PART_OF]->(pr)"""
            self.db.query(query)
        
        # Mentorship and backup relationships
        for mentorship in relationships.get("person_mentorships", []):
            query = f"""MATCH (mentor:Person {{id: '{mentorship['mentor_id']}'}}), (mentee:Person {{id: '{mentorship['mentee_id']}'}}) 
                       CREATE (mentee)-[:MENTORED_BY {{
                           start_date: '{mentorship['start_date']}',
                           focus_area: '{mentorship['focus_area']}'
                       }}]->(mentor)"""
            self.db.query(query)
        
        for backup in relationships.get("person_backups", []):
            query = f"""MATCH (primary:Person {{id: '{backup['primary_person_id']}'}}), (backup:Person {{id: '{backup['backup_person_id']}'}}) 
                       CREATE (backup)-[:BACKUP_FOR {{
                           coverage_type: '{backup['coverage_type']}',
                           readiness_level: '{backup['readiness_level']}'
                       }}]->(primary)"""
            self.db.query(query)
        
        # Specialization relationships
        for spec in relationships.get("person_specializations", []):
            # Create Technology nodes on the fly for specializations
            query = f"""MERGE (tech:Technology {{name: '{escape_string(spec['specialization'])}'}})"""
            self.db.query(query)
            
            query = f"""MATCH (p:Person {{id: '{spec['person_id']}'}}), (tech:Technology {{name: '{escape_string(spec['specialization'])}'}}) 
                       CREATE (p)-[:SPECIALIZES_IN {{
                           expertise_level: '{spec['expertise_level']}',
                           years_in_specialty: {spec['years_in_specialty']}
                       }}]->(tech)"""
            self.db.query(query)
        
        # Office and language relationships
        for assignment in relationships.get("person_office_assignments", []):
            desk_location = f", desk_location: '{assignment['desk_location']}'" if assignment['desk_location'] else ""
            query = f"""MATCH (p:Person {{id: '{assignment['person_id']}'}}), (o:Office {{id: '{assignment['office_id']}'}}) 
                       CREATE (p)-[:WORKS_AT {{
                           start_date: '{assignment['start_date']}',
                           is_remote: {str(assignment['is_remote']).lower()}{desk_location}
                       }}]->(o)"""
            self.db.query(query)
        
        for lang_rel in relationships.get("person_languages", []):
            cert_date = f", certification_date: '{lang_rel['certification_date']}'" if lang_rel['certification_date'] else ""
            query = f"""MATCH (p:Person {{id: '{lang_rel['person_id']}'}}), (l:Language {{id: '{lang_rel['language_id']}'}}) 
                       CREATE (p)-[:SPEAKS {{
                           proficiency: '{lang_rel['proficiency']}',
                           is_primary: {str(lang_rel['is_primary']).lower()},
                           certified: {str(lang_rel['certified']).lower()}{cert_date}
                       }}]->(l)"""
            self.db.query(query)
        
        # Holiday-office relationships
        holidays = self.db.query("MATCH (h:Holiday) RETURN h").result_set
        for holiday_record in holidays:
            holiday = dict(holiday_record[0].properties)
            if 'offices' in holiday and holiday['offices']:
                office_ids = holiday['offices'].split(',')
                for office_id in office_ids:
                    query = f"""MATCH (h:Holiday {{id: '{holiday['id']}'}}), (o:Office {{id: '{office_id}'}}) 
                               CREATE (h)-[:OBSERVED_BY]->(o)"""
                    self.db.query(query)
        
        # Office collaboration relationships
        for collab in relationships.get("office_collaborations", []):
            meeting_times_str = ','.join(collab['preferred_meeting_times'])
            query = f"""MATCH (o1:Office {{id: '{collab['office1_id']}'}}), (o2:Office {{id: '{collab['office2_id']}'}}) 
                       CREATE (o1)-[:COLLABORATES_WITH {{
                           overlap_hours: {collab['overlap_hours']},
                           preferred_meeting_times: '{meeting_times_str}'
                       }}]->(o2)"""
            self.db.query(query)
        
        # Compliance relationships
        for office_comp in relationships.get("office_compliance", []):
            query = f"""MATCH (o:Office {{id: '{office_comp['office_id']}'}}), (c:Compliance {{id: '{office_comp['compliance_id']}'}}) 
                       CREATE (o)-[:OPERATES_UNDER {{
                           since: '{office_comp['since']}',
                           attestation_date: '{office_comp['attestation_date']}',
                           next_audit: '{office_comp['next_audit']}'
                       }}]->(c)"""
            self.db.query(query)
        
        for client_comp in relationships.get("client_compliance", []):
            query = f"""MATCH (cl:Client {{id: '{client_comp['client_id']}'}}), (c:Compliance {{id: '{client_comp['compliance_id']}'}}) 
                       CREATE (cl)-[:REQUIRES_COMPLIANCE {{
                           contractual: {str(client_comp['contractual']).lower()},
                           sla_impact: '{client_comp['sla_impact']}'
                       }}]->(c)"""
            self.db.query(query)
        
        # Data residency relationships
        for office_dr in relationships.get("office_data_residency", []):
            query = f"""MATCH (o:Office {{id: '{office_dr['office_id']}'}}), (dr:DataResidency {{id: '{office_dr['data_residency_id']}'}}) 
                       CREATE (o)-[:ENFORCES]->(dr)"""
            self.db.query(query)
        
        for proj_dr in relationships.get("project_data_residency", []):
            query = f"""MATCH (p:Project {{id: '{proj_dr['project_id']}'}}), (dr:DataResidency {{id: '{proj_dr['data_residency_id']}'}}) 
                       CREATE (p)-[:STORES_DATA_IN]->(dr)"""
            self.db.query(query)
        
        # Support relationships
        for on_call in relationships.get("person_on_call", []):
            query = f"""MATCH (p:Person {{id: '{on_call['person_id']}'}}), (s:Schedule {{id: '{on_call['schedule_id']}'}}) 
                       CREATE (p)-[:ON_CALL {{
                           role: '{on_call['role']}',
                           reachable_via: '{on_call['reachable_via']}'
                       }}]->(s)"""
            self.db.query(query)
        
        for response in relationships.get("person_incident_response", []):
            query = f"""MATCH (p:Person {{id: '{response['person_id']}'}}), (i:Incident {{id: '{response['incident_id']}'}}) 
                       CREATE (p)-[:RESPONDED_TO {{
                           response_time_minutes: {response['response_time_minutes']},
                           role: '{response['role']}'
                       }}]->(i)"""
            self.db.query(query)
        
        for handoff in relationships.get("team_handoffs", []):
            query = f"""MATCH (t1:Team {{id: '{handoff['from_team_id']}'}}), (t2:Team {{id: '{handoff['to_team_id']}'}}) 
                       CREATE (t1)-[:HANDS_OFF_TO {{
                           handoff_time: '{handoff['handoff_time']}',
                           handoff_type: '{handoff['handoff_type']}'
                       }}]->(t2)"""
            self.db.query(query)
        
        for visa_rel in relationships.get("person_visas", []):
            query = f"""MATCH (p:Person {{id: '{visa_rel['person_id']}'}}), (v:Visa {{id: '{visa_rel['visa_id']}'}}) 
                       CREATE (p)-[:HAS_VISA {{
                           status: '{visa_rel['status']}',
                           sponsor: '{visa_rel['sponsor']}'
                       }}]->(v)"""
            self.db.query(query)
        
        for support in relationships.get("team_supports_region", []):
            query = f"""MATCH (t:Team {{id: '{support['team_id']}'}}), (c:Client {{id: '{support['client_id']}'}}) 
                       CREATE (t)-[:SUPPORTS {{
                           coverage_hours: '{support['coverage_hours']}'
                       }}]->(c)"""
            self.db.query(query)
        
        # Platform relationships
        for deployment in relationships.get("component_deployed_in", []):
            query = f"""MATCH (c:PlatformComponent {{id: '{deployment['component_id']}'}}), (r:CloudRegion {{id: '{deployment['region_id']}'}}) 
                       CREATE (c)-[:DEPLOYED_IN]->(r)"""
            self.db.query(query)
        
        for usage in relationships.get("client_uses_component", []):
            query = f"""MATCH (c:Client {{id: '{usage['client_id']}'}}), (pc:PlatformComponent {{id: '{usage['component_id']}'}}) 
                       CREATE (c)-[:USES {{
                           usage_level: '{usage['usage_level']}'
                       }}]->(pc)"""
            self.db.query(query)
        
        for expertise in relationships.get("person_expert_in", []):
            query = f"""MATCH (p:Person {{id: '{expertise['person_id']}'}}), (pc:PlatformComponent {{id: '{expertise['component_id']}'}}) 
                       CREATE (p)-[:EXPERT_IN {{
                           expertise_level: {expertise['expertise_level']}
                       }}]->(pc)"""
            self.db.query(query)
        
    def _store_statistics(self, data: Dict[str, Any]) -> None:
        """Store seeding statistics."""
        stats = {
            "people_count": len(data["people"]),
            "teams_count": len(data["teams"]),
            "groups_count": len(data["groups"]),
            "policies_count": len(data["policies"]),
            "skills_count": len(data["skills"]),
            "projects_count": len(data["projects"]),
            "clients_count": len(data["clients"]),
            "sprints_count": len(data["sprints"]),
            "offices_count": len(data["offices"]),
            "languages_count": len(data["languages"]),
            "holidays_count": len(data["holidays"]),
            "compliance_count": len(data["compliance"]),
            "data_residency_count": len(data["data_residency"]),
            "schedules_count": len(data["schedules"]),
            "incidents_count": len(data["incidents"]),
            "visas_count": len(data["visas"]),
            "metrics_count": len(data["metrics"]),
            "cloud_regions_count": len(data["cloud_regions"]),
            "platform_components_count": len(data["platform_components"]),
            "seeded_at": datetime.now().isoformat()
        }
        
        query = f"""CREATE (s:SeedStats {{
            people_count: {stats['people_count']},
            teams_count: {stats['teams_count']},
            groups_count: {stats['groups_count']},
            policies_count: {stats['policies_count']},
            skills_count: {stats['skills_count']},
            projects_count: {stats['projects_count']},
            clients_count: {stats['clients_count']},
            sprints_count: {stats['sprints_count']},
            offices_count: {stats['offices_count']},
            languages_count: {stats['languages_count']},
            holidays_count: {stats['holidays_count']},
            compliance_count: {stats['compliance_count']},
            data_residency_count: {stats['data_residency_count']},
            schedules_count: {stats['schedules_count']},
            incidents_count: {stats['incidents_count']},
            visas_count: {stats['visas_count']},
            metrics_count: {stats['metrics_count']},
            cloud_regions_count: {stats['cloud_regions_count']},
            platform_components_count: {stats['platform_components_count']},
            seeded_at: '{stats['seeded_at']}'
        }})"""
        self.db.query(query)
    
    def _print_summary(self, data: Dict[str, Any]) -> None:
        """Print seeding summary."""
        print(f"✅ Seeded {len(data['people'])} people, {len(data['teams'])} teams, {len(data['groups'])} groups, {len(data['policies'])} policies")
        print(f"✅ Added {len(data['skills'])} skills, {len(data['projects'])} projects, {len(data['clients'])} clients, {len(data['sprints'])} sprints")
        print(f"✅ Added {len(data['offices'])} offices, {len(data['languages'])} languages, {len(data['holidays'])} holidays")
        print(f"✅ Added {len(data['compliance'])} compliance frameworks, {len(data['data_residency'])} data residency zones")
        print(f"✅ Added {len(data['schedules'])} schedules, {len(data['incidents'])} incidents")
        print(f"✅ Added {len(data['visas'])} visas, {len(data['metrics'])} performance metrics")
        print(f"✅ Added {len(data['cloud_regions'])} cloud regions, {len(data['platform_components'])} platform components")