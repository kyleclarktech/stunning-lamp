#!/usr/bin/env python3
"""
New modular seed data script for FalkorDB.
This script orchestrates the data generation and database seeding process.
"""

import sys
import os
import traceback
from datetime import datetime

# Add the parent directory to the path to import the data_generators package
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from scripts.data_generators.database import DatabaseConnection, DatabaseSeeder
from scripts.data_generators.entities import (
    PeopleGenerator, TeamsGenerator, GroupsGenerator, OfficesGenerator,
    SkillsGenerator, LanguagesGenerator, ProjectsGenerator, SprintsGenerator,
    ClientsGenerator, PlatformComponentsGenerator, CloudRegionsGenerator,
    PoliciesGenerator, ComplianceFrameworksGenerator, DataResidencyGenerator,
    HolidaysGenerator, SchedulesGenerator, IncidentsGenerator, VisasGenerator,
    MetricsGenerator
)
from scripts.data_generators.relationships import (
    PersonTeamMembershipGenerator, PersonGroupMembershipGenerator,
    TeamPolicyResponsibilityGenerator, GroupPolicyResponsibilityGenerator,
    PersonReportsToGenerator, PersonMentorshipGenerator, PersonBackupGenerator,
    PersonOfficeAssignmentGenerator, TeamHandoffGenerator,
    PersonSkillGenerator, PersonSpecializationGenerator, PersonLanguageGenerator,
    PersonExpertInGenerator, PersonProjectAllocationGenerator,
    ProjectSkillRequirementGenerator, TeamProjectDeliveryGenerator,
    ProjectClientRelationshipGenerator, SprintProjectRelationshipGenerator,
    ProjectDataResidencyGenerator, ComponentDeployedInGenerator,
    ClientUsesComponentGenerator, PersonOnCallGenerator,
    PersonIncidentResponseGenerator, PersonVisaGenerator,
    TeamSupportsRegionGenerator, OfficeComplianceGenerator,
    ClientComplianceGenerator, OfficeDataResidencyGenerator,
    HolidayOfficeRelationshipGenerator, OfficeCollaborationGenerator
)


def generate_all_data():
    """Generate all data using the modular generators."""
    print("🎲 Generating test data...")
    
    # Initialize entity generators
    people_gen = PeopleGenerator()
    teams_gen = TeamsGenerator()
    groups_gen = GroupsGenerator()
    offices_gen = OfficesGenerator()
    skills_gen = SkillsGenerator()
    languages_gen = LanguagesGenerator()
    clients_gen = ClientsGenerator()
    platform_gen = PlatformComponentsGenerator()
    cloud_regions_gen = CloudRegionsGenerator()
    policies_gen = PoliciesGenerator()
    compliance_gen = ComplianceFrameworksGenerator()
    data_residency_gen = DataResidencyGenerator()
    holidays_gen = HolidaysGenerator()
    schedules_gen = SchedulesGenerator()
    incidents_gen = IncidentsGenerator()
    visas_gen = VisasGenerator()
    metrics_gen = MetricsGenerator()
    
    # Generate base entities
    print("  • Generating entities...")
    people = people_gen.generate()
    teams = teams_gen.generate()
    groups = groups_gen.generate()
    offices = offices_gen.generate()
    skills = skills_gen.generate()
    languages = languages_gen.generate()
    clients = clients_gen.generate()
    platform_components = platform_gen.generate()
    cloud_regions = cloud_regions_gen.generate()
    policies = policies_gen.generate()
    compliance_frameworks = compliance_gen.generate()
    data_residency_zones = data_residency_gen.generate()
    holidays = holidays_gen.generate()
    schedules = schedules_gen.generate()
    incidents = incidents_gen.generate()
    visas = visas_gen.generate()
    metrics = metrics_gen.generate()
    
    # Generate entities that depend on others
    projects_gen = ProjectsGenerator()
    projects = projects_gen.generate()
    
    sprints_gen = SprintsGenerator(projects)
    sprints = sprints_gen.generate()
    
    # Generate relationships
    print("  • Generating relationships...")
    
    # Initialize relationship generators
    person_team_gen = PersonTeamMembershipGenerator(people, teams)
    person_group_gen = PersonGroupMembershipGenerator(people, groups)
    team_policy_gen = TeamPolicyResponsibilityGenerator(teams, policies)
    group_policy_gen = GroupPolicyResponsibilityGenerator(groups, policies)
    person_mentorship_gen = PersonMentorshipGenerator(people)
    person_backup_gen = PersonBackupGenerator(people)
    person_office_gen = PersonOfficeAssignmentGenerator(people, offices)
    person_skill_gen = PersonSkillGenerator(people, skills)
    person_spec_gen = PersonSpecializationGenerator(people)
    person_project_gen = PersonProjectAllocationGenerator(people, projects)
    project_skill_gen = ProjectSkillRequirementGenerator(projects, skills)
    team_project_gen = TeamProjectDeliveryGenerator(teams, projects)
    person_expert_gen = PersonExpertInGenerator(people, platform_components)
    component_deployed_gen = ComponentDeployedInGenerator(platform_components, cloud_regions)
    client_uses_gen = ClientUsesComponentGenerator(clients, platform_components)
    team_supports_gen = TeamSupportsRegionGenerator(teams, clients)
    office_compliance_gen = OfficeComplianceGenerator(offices, compliance_frameworks)
    client_compliance_gen = ClientComplianceGenerator(clients, compliance_frameworks)
    office_dr_gen = OfficeDataResidencyGenerator(offices, data_residency_zones)
    office_collab_gen = OfficeCollaborationGenerator(offices)
    
    # Generate basic relationships
    person_team_memberships = person_team_gen.generate()
    person_group_memberships = person_group_gen.generate()
    team_policy_responsibilities = team_policy_gen.generate()
    group_policy_responsibilities = group_policy_gen.generate()
    person_skills = person_skill_gen.generate()
    person_project_allocations = person_project_gen.generate()
    project_skill_requirements = project_skill_gen.generate()
    team_project_delivery = team_project_gen.generate()
    person_mentorships = person_mentorship_gen.generate()
    person_backups = person_backup_gen.generate()
    person_specializations = person_spec_gen.generate()
    person_office_assignments = person_office_gen.generate()
    person_expert_in = person_expert_gen.generate()
    component_deployed_in = component_deployed_gen.generate()
    client_uses_component = client_uses_gen.generate()
    team_supports_region = team_supports_gen.generate()
    office_compliance = office_compliance_gen.generate()
    client_compliance = client_compliance_gen.generate()
    office_data_residency = office_dr_gen.generate()
    office_collaborations = office_collab_gen.generate()
    
    # Generate relationships that depend on other relationships
    person_lang_gen = PersonLanguageGenerator(people, languages, person_office_assignments)
    person_languages = person_lang_gen.generate()
    
    team_handoff_gen = TeamHandoffGenerator(teams, offices, person_team_memberships, person_office_assignments)
    team_handoffs = team_handoff_gen.generate()
    
    person_on_call_gen = PersonOnCallGenerator(people, schedules, offices, person_office_assignments)
    person_on_call = person_on_call_gen.generate()
    
    person_incident_gen = PersonIncidentResponseGenerator(people, incidents, offices, person_office_assignments)
    person_incident_response = person_incident_gen.generate()
    
    person_visa_gen = PersonVisaGenerator(people, visas, offices, person_office_assignments)
    person_visas = person_visa_gen.generate()
    
    project_dr_gen = ProjectDataResidencyGenerator(projects, clients, data_residency_zones, client_compliance)
    project_data_residency = project_dr_gen.generate()
    
    # Compile all data
    data = {
        "people": people,
        "teams": teams,
        "groups": groups,
        "offices": offices,
        "skills": skills,
        "languages": languages,
        "clients": clients,
        "projects": projects,
        "sprints": sprints,
        "platform_components": platform_components,
        "cloud_regions": cloud_regions,
        "policies": policies,
        "compliance": compliance_frameworks,
        "data_residency": data_residency_zones,
        "holidays": holidays,
        "schedules": schedules,
        "incidents": incidents,
        "visas": visas,
        "metrics": metrics,
        "relationships": {
            "person_team_memberships": person_team_memberships,
            "person_group_memberships": person_group_memberships,
            "team_policy_responsibilities": team_policy_responsibilities,
            "group_policy_responsibilities": group_policy_responsibilities,
            "person_skills": person_skills,
            "person_project_allocations": person_project_allocations,
            "project_skill_requirements": project_skill_requirements,
            "team_project_delivery": team_project_delivery,
            "person_mentorships": person_mentorships,
            "person_backups": person_backups,
            "person_specializations": person_specializations,
            "person_office_assignments": person_office_assignments,
            "person_languages": person_languages,
            "office_collaborations": office_collaborations,
            "office_compliance": office_compliance,
            "client_compliance": client_compliance,
            "office_data_residency": office_data_residency,
            "project_data_residency": project_data_residency,
            "person_on_call": person_on_call,
            "person_incident_response": person_incident_response,
            "team_handoffs": team_handoffs,
            "person_visas": person_visas,
            "team_supports_region": team_supports_region,
            "component_deployed_in": component_deployed_in,
            "client_uses_component": client_uses_component,
            "person_expert_in": person_expert_in
        }
    }
    
    return data


def main():
    """Main function to orchestrate the seeding process."""
    try:
        # Create database connection
        connection = DatabaseConnection()
        
        # Generate all data
        data = generate_all_data()
        
        # Seed the database
        seeder = DatabaseSeeder(connection)
        seeder.seed(data)
        
        print("✅ Database seeding completed successfully!")
        
    except Exception as e:
        print(f"❌ Error seeding database: {e}")
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()