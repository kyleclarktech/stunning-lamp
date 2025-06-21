from typing import List, Dict, Any
import json
from faker import Faker
from ..base import BaseGenerator

fake = Faker()


class PoliciesGenerator(BaseGenerator):
    """Generate comprehensive policies for B2B data analytics platform"""
    
    def generate(self) -> List[Dict[str, Any]]:
        policies = [
            {
                "id": "policy_1",
                "name": "Customer Data Processing Policy",
                "description": "All customer data processing must comply with data processing agreements (DPAs). Data must be processed only for agreed purposes with explicit consent. Data minimization principles apply - collect only necessary data. Customer data segregation must be maintained with encryption at rest and in transit. Processing logs retained for audit purposes.",
                "category": "data_governance",
                "severity": "critical",
                "responsible_type": "group",
                "compliance_frameworks": ["GDPR", "CCPA", "SOC2"]
            },
            {
                "id": "policy_2", 
                "name": "Data Classification Policy",
                "description": "All data must be classified as Public, Internal, Confidential, or Restricted. Classification determines handling requirements including encryption, access controls, and retention periods. Restricted data requires additional security controls and audit logging. Automated classification tools must scan and tag data. Quarterly classification reviews required.",
                "category": "data_governance",
                "severity": "high",
                "responsible_type": "team",
                "compliance_frameworks": ["SOC2", "ISO27001", "NIST"]
            },
            {
                "id": "policy_3",
                "name": "Data Quality Standards Policy", 
                "description": "Data quality metrics must be defined and monitored for all datasets. Quality thresholds: completeness >95%, accuracy >99%, consistency >98%. Automated quality checks required for all data pipelines. Quality issues must be remediated within SLA timeframes. Data quality scorecards published monthly.",
                "category": "data_governance",
                "severity": "high",
                "responsible_type": "team",
                "compliance_frameworks": ["SOC2", "Internal"]
            },
            {
                "id": "policy_4",
                "name": "Data Lineage and Metadata Policy",
                "description": "Complete data lineage must be maintained for all datasets showing origin, transformations, and dependencies. Metadata cataloging required including schema, ownership, quality metrics, and usage. Lineage must be queryable and auditable. Updates to lineage tracking within 24 hours of pipeline changes.",
                "category": "data_governance",
                "severity": "medium", 
                "responsible_type": "team",
                "compliance_frameworks": ["SOC2", "Internal"]
            },
            {
                "id": "policy_5",
                "name": "Encryption Policy",
                "description": "All data must be encrypted at rest (AES-256) and in transit (TLS 1.2+). Encryption keys managed via HSM with annual rotation. Customer data requires envelope encryption with customer-managed keys option. Key escrow and recovery procedures required. Encryption status monitored continuously.",
                "category": "security",
                "severity": "critical",
                "responsible_type": "team",
                "compliance_frameworks": ["SOC2", "ISO27001", "FIPS"]
            },
            {
                "id": "policy_6",
                "name": "Access Control Policy",
                "description": "Role-based access control (RBAC) required for all systems. Just-in-time access for privileged operations. Access reviews quarterly for admins, semi-annually for users. Break-glass procedures for emergency access with full audit trail. Customer data access restricted to authorized personnel only.",
                "category": "security",
                "severity": "critical",
                "responsible_type": "group",
                "compliance_frameworks": ["SOC2", "ISO27001", "NIST"]
            },
            {
                "id": "policy_7",
                "name": "Audit Logging Policy",
                "description": "All data access, modifications, and administrative actions must be logged. Logs retained for 2 years minimum, 7 years for compliance data. Log integrity protection via write-once storage. Real-time anomaly detection on audit logs. Customer audit logs available via API.",
                "category": "security",
                "severity": "high",
                "responsible_type": "team",
                "compliance_frameworks": ["SOC2", "GDPR", "HIPAA"]
            },
            {
                "id": "policy_8",
                "name": "API Rate Limiting Policy",
                "description": "All APIs must implement rate limiting based on customer tier. Default limits: 1000 requests/hour for standard, 10000/hour for premium, custom for enterprise. Burst allowances up to 2x limit for 5 minutes. Clear error messages and retry headers required. Rate limit monitoring and alerting.",
                "category": "platform",
                "severity": "high",
                "responsible_type": "team",
                "compliance_frameworks": ["SOC2", "Internal"]
            },
            {
                "id": "policy_9",
                "name": "SLA and Uptime Policy",
                "description": "Platform SLA: 99.9% uptime for standard, 99.95% for premium, 99.99% for enterprise. Planned maintenance windows excluded. SLA credits issued automatically for breaches. Real-time status page required with incident history. Performance SLAs for query response times.",
                "category": "platform",
                "severity": "critical",
                "responsible_type": "group",
                "compliance_frameworks": ["SOC2", "Internal"]
            },
            {
                "id": "policy_10",
                "name": "Multi-tenancy Isolation Policy",
                "description": "Complete logical isolation between customer tenants. Resource quotas enforced per tenant. No shared compute or storage resources. Network isolation via VPC/namespace separation. Regular isolation testing required. Data leakage prevention controls mandatory.",
                "category": "platform",
                "severity": "critical",
                "responsible_type": "team",
                "compliance_frameworks": ["SOC2", "ISO27001", "FedRAMP"]
            },
            {
                "id": "policy_11",
                "name": "Data Export Policy",
                "description": "Customers must be able to export all their data within 30 days of request. Standard formats: CSV, JSON, Parquet. Bulk export via secure channels. Export includes all data, metadata, and configurations. Automated export capabilities required. Data portability compliance.",
                "category": "platform",
                "severity": "high",
                "responsible_type": "team",
                "compliance_frameworks": ["GDPR", "CCPA", "Internal"]
            },
            {
                "id": "policy_12",
                "name": "Data Processing Agreement Policy", 
                "description": "Signed DPAs required for all customers before data processing. DPAs must specify purposes, retention, sub-processors, and security measures. Annual review and updates required. Template DPAs for standard offerings, custom for enterprise. Sub-processor list maintained publicly.",
                "category": "legal",
                "severity": "critical",
                "responsible_type": "group",
                "compliance_frameworks": ["GDPR", "CCPA", "SOC2"]
            },
            {
                "id": "policy_13",
                "name": "Right to Erasure Policy",
                "description": "Customer data deletion requests must be fulfilled within 30 days. Deletion includes all copies, backups (after retention period), and derived data. Deletion certificate provided. Some data retained for legal/compliance as documented. Automated deletion workflows required.",
                "category": "data_privacy",
                "severity": "critical",
                "responsible_type": "group",
                "compliance_frameworks": ["GDPR", "CCPA", "PIPEDA"]
            },
            {
                "id": "policy_14",
                "name": "Data Breach Notification Policy",
                "description": "Confirmed breaches notified to affected customers within 72 hours. Notifications include scope, impact, remediation steps, and recommendations. Regulatory notifications as required by jurisdiction. Public disclosure for significant breaches. Breach response team activation procedures.",
                "category": "security",
                "severity": "critical",
                "responsible_type": "group",
                "compliance_frameworks": ["GDPR", "CCPA", "SOC2"]
            },
            {
                "id": "policy_15",
                "name": "Third-party Data Processor Policy",
                "description": "All third-party processors vetted for security and compliance. Contracts require equivalent data protection. Annual audits of critical processors. Processor list maintained and available to customers. Change notifications 30 days in advance. Data localization requirements respected.",
                "category": "vendor_management",
                "severity": "high",
                "responsible_type": "group",
                "compliance_frameworks": ["GDPR", "SOC2", "ISO27001"]
            },
            {
                "id": "policy_16",
                "name": "CI/CD Security Policy",
                "description": "All code deployments via automated CI/CD pipelines. Security scanning (SAST/DAST) required before production. No direct production access - all changes via pipeline. Deployment approvals for critical systems. Rollback capabilities required. Container scanning for vulnerabilities.",
                "category": "development",
                "severity": "high",
                "responsible_type": "team",
                "compliance_frameworks": ["SOC2", "ISO27001", "NIST"]
            },
            {
                "id": "policy_17",
                "name": "Disaster Recovery Policy",
                "description": "RPO: 1 hour for critical data, 4 hours for standard. RTO: 4 hours for critical systems, 24 hours for standard. DR testing quarterly with full failover annually. Geo-redundant backups in 3+ regions. Automated failover for critical services. Customer data recovery guarantees.",
                "category": "operations",
                "severity": "critical",
                "responsible_type": "group",
                "compliance_frameworks": ["SOC2", "ISO22301", "Internal"]
            },
            {
                "id": "policy_18",
                "name": "Change Management Policy",
                "description": "All production changes require approval based on risk level. High-risk changes need CAB approval and rollback plan. Change freeze during peak periods. Post-implementation reviews for major changes. Emergency change procedures defined. Customer notification for impacting changes.",
                "category": "operations",
                "severity": "high",
                "responsible_type": "group",
                "compliance_frameworks": ["SOC2", "ITIL", "Internal"]
            },
            {
                "id": "policy_19",
                "name": "Performance Monitoring Policy",
                "description": "All services monitored for availability, latency, and error rates. SLIs/SLOs defined per service. Alerting thresholds at 80% of SLO. Performance baselines established and anomaly detection enabled. Monthly performance reviews and optimization. Customer-facing performance metrics published.",
                "category": "operations",
                "severity": "medium",
                "responsible_type": "team",
                "compliance_frameworks": ["SOC2", "Internal"]
            },
            {
                "id": "policy_20",
                "name": "Data Retention and Deletion Policy",
                "description": "Customer data retained per contractual agreements. Default retention: operational data 90 days, analytical results 1 year, audit logs 2 years. Automated deletion workflows with verification. Legal hold procedures for investigations. Data destruction certificates provided on request.",
                "category": "data_governance",
                "severity": "high",
                "responsible_type": "group",
                "compliance_frameworks": ["GDPR", "CCPA", "SOC2"]
            }
        ]
        
        return policies


class ComplianceFrameworksGenerator(BaseGenerator):
    """Generate compliance framework data"""
    
    def generate(self) -> List[Dict[str, Any]]:
        compliance_frameworks = [
            # Data Privacy Regulations
            {
                "id": "comp_gdpr",
                "framework": "GDPR",
                "version": "2016/679",
                "jurisdiction": "European Union",
                "geographic_scope": ["EU", "EEA"],
                "type": "data_privacy",
                "requirements": {
                    "lawful_basis": ["consent", "contract", "legal_obligation", "vital_interests", "public_task", "legitimate_interests"],
                    "data_subject_rights": ["access", "rectification", "erasure", "portability", "object", "restrict_processing"],
                    "breach_notification": "72 hours",
                    "dpo_required": True,
                    "privacy_by_design": True,
                    "data_protection_impact_assessment": True
                },
                "penalties": {
                    "max_fine_percentage": 4,
                    "max_fine_amount": "20M EUR",
                    "enforcement_body": "Data Protection Authorities"
                },
                "effective_date": "2018-05-25",
                "last_updated": "2023-01-01",
                "status": "active"
            },
            {
                "id": "comp_ccpa",
                "framework": "CCPA",
                "version": "2018 with 2023 amendments",
                "jurisdiction": "California, USA",
                "geographic_scope": ["CA", "US"],
                "type": "data_privacy",
                "requirements": {
                    "consumer_rights": ["know", "delete", "opt-out", "non-discrimination"],
                    "revenue_threshold": 25000000,
                    "consumer_threshold": 50000,
                    "data_categories": ["personal", "commercial", "biometric", "internet_activity", "geolocation"],
                    "breach_notification": "without unreasonable delay",
                    "privacy_policy_required": True
                },
                "penalties": {
                    "per_violation": 2500,
                    "per_intentional_violation": 7500,
                    "enforcement_body": "California Attorney General"
                },
                "effective_date": "2020-01-01",
                "last_updated": "2023-01-01",
                "status": "active"
            },
            # Security Standards
            {
                "id": "comp_soc2",
                "framework": "SOC2",
                "version": "Type II",
                "jurisdiction": "United States",
                "geographic_scope": ["US", "Global"],
                "type": "security",
                "requirements": {
                    "trust_principles": ["security", "availability", "processing_integrity", "confidentiality", "privacy"],
                    "audit_frequency": "annual",
                    "continuous_monitoring": True,
                    "vendor_management": True,
                    "incident_response": True,
                    "access_controls": True
                },
                "penalties": {
                    "certification_loss": True,
                    "client_contract_breach": True,
                    "reputational_damage": "high"
                },
                "effective_date": "2017-05-01",
                "last_updated": "2023-04-15",
                "status": "active"
            },
            # Industry Specific
            {
                "id": "comp_hipaa",
                "framework": "HIPAA",
                "version": "2013 Omnibus",
                "jurisdiction": "United States",
                "geographic_scope": ["US"],
                "type": "data_privacy",
                "requirements": {
                    "safeguards": ["administrative", "physical", "technical"],
                    "phi_handling": True,
                    "business_associate_agreements": True,
                    "breach_notification": "60 days",
                    "risk_assessments": "annual",
                    "employee_training": True
                },
                "penalties": {
                    "tier1_min": 100,
                    "tier1_max": 50000,
                    "tier4_min": 1500000,
                    "tier4_max": 1500000,
                    "enforcement_body": "OCR/HHS"
                },
                "effective_date": "2013-09-23",
                "last_updated": "2022-10-20",
                "status": "active"
            },
            {
                "id": "comp_pci_dss",
                "framework": "PCI-DSS",
                "version": "4.0",
                "jurisdiction": "Global",
                "geographic_scope": ["Global"],
                "type": "financial",
                "requirements": {
                    "network_security": True,
                    "cardholder_data_protection": True,
                    "vulnerability_management": True,
                    "access_control": True,
                    "monitoring_testing": True,
                    "security_policy": True,
                    "customized_approach": True
                },
                "penalties": {
                    "monthly_fines": "5000-100000",
                    "card_brand_fines": True,
                    "processing_suspension": True
                },
                "effective_date": "2022-03-31",
                "last_updated": "2024-01-01",
                "status": "active"
            },
            # Regional Regulations
            {
                "id": "comp_lgpd",
                "framework": "LGPD",
                "version": "2020",
                "jurisdiction": "Brazil",
                "geographic_scope": ["BR"],
                "type": "data_privacy",
                "requirements": {
                    "legal_basis": ["consent", "legal_obligation", "public_policy", "research", "contract", "legitimate_interest"],
                    "data_subject_rights": ["access", "correction", "deletion", "portability", "information"],
                    "dpo_required": True,
                    "impact_assessment": True
                },
                "penalties": {
                    "max_fine_percentage": 2,
                    "max_fine_amount": "50M BRL",
                    "enforcement_body": "ANPD"
                },
                "effective_date": "2020-09-18",
                "last_updated": "2023-07-01",
                "status": "active"
            },
            {
                "id": "comp_pipeda",
                "framework": "PIPEDA",
                "version": "2019",
                "jurisdiction": "Canada",
                "geographic_scope": ["CA"],
                "type": "data_privacy",
                "requirements": {
                    "privacy_principles": ["accountability", "consent", "limiting_collection", "limiting_use", "accuracy", "safeguards", "openness", "access", "challenging_compliance"],
                    "breach_notification": "without unreasonable delay",
                    "privacy_policy": True
                },
                "penalties": {
                    "max_fine": 100000,
                    "currency": "CAD",
                    "enforcement_body": "Privacy Commissioner"
                },
                "effective_date": "2019-11-01",
                "last_updated": "2023-03-15",
                "status": "active"
            },
            {
                "id": "comp_appi",
                "framework": "APPI",
                "version": "2022",
                "jurisdiction": "Japan",
                "geographic_scope": ["JP"],
                "type": "data_privacy",
                "requirements": {
                    "purpose_limitation": True,
                    "data_minimization": True,
                    "consent_requirements": "opt-in",
                    "cross_border_transfer": "adequacy or consent",
                    "security_measures": True,
                    "breach_notification": True
                },
                "penalties": {
                    "corporate_fine": 100000000,
                    "individual_fine": 1000000,
                    "currency": "JPY",
                    "enforcement_body": "PPC"
                },
                "effective_date": "2022-04-01",
                "last_updated": "2023-06-01",
                "status": "active"
            }
        ]
        
        return compliance_frameworks


class DataResidencyGenerator(BaseGenerator):
    """Generate data residency zone information"""
    
    def generate(self) -> List[Dict[str, Any]]:
        data_residency_zones = [
            {
                "id": "dr_us",
                "zone": "US",
                "countries": ["United States", "Canada", "Mexico"],
                "regulations": ["CCPA", "PIPEDA", "COPPA", "FERPA"],
                "storage_locations": ["us-east-1", "us-west-2", "us-central1", "ca-central-1"],
                "transfer_restrictions": {
                    "to_eu": "standard_contractual_clauses",
                    "to_apac": "consent_required",
                    "to_other": "case_by_case"
                },
                "encryption_required": True
            },
            {
                "id": "dr_eu",
                "zone": "EU",
                "countries": ["Germany", "France", "Netherlands", "Belgium", "Italy", "Spain", "Poland", "Ireland", "Sweden", "Denmark"],
                "regulations": ["GDPR", "ePrivacy", "NIS2", "DMA", "DSA"],
                "storage_locations": ["eu-west-1", "eu-central-1", "eu-north-1", "europe-west1", "europe-west4"],
                "transfer_restrictions": {
                    "to_us": "adequacy_decision_or_scc",
                    "to_apac": "adequacy_or_appropriate_safeguards",
                    "to_other": "gdpr_compliant_only"
                },
                "encryption_required": True
            },
            {
                "id": "dr_uk",
                "zone": "UK",
                "countries": ["United Kingdom"],
                "regulations": ["UK-GDPR", "DPA-2018"],
                "storage_locations": ["eu-west-2", "europe-west2"],
                "transfer_restrictions": {
                    "to_eu": "adequacy_decision",
                    "to_us": "appropriate_safeguards",
                    "to_apac": "case_by_case"
                },
                "encryption_required": True
            },
            {
                "id": "dr_apac",
                "zone": "APAC",
                "countries": ["Japan", "Singapore", "Australia", "New Zealand", "Hong Kong", "South Korea"],
                "regulations": ["APPI", "PDPA", "Privacy Act", "PIPA"],
                "storage_locations": ["ap-northeast-1", "ap-southeast-1", "ap-southeast-2", "asia-northeast1", "asia-southeast1"],
                "transfer_restrictions": {
                    "to_us": "consent_or_contract",
                    "to_eu": "appropriate_safeguards",
                    "within_apac": "country_specific"
                },
                "encryption_required": True
            },
            {
                "id": "dr_china",
                "zone": "China",
                "countries": ["China"],
                "regulations": ["PIPL", "CSL", "DSL"],
                "storage_locations": ["cn-north-1", "cn-northwest-1"],
                "transfer_restrictions": {
                    "to_any": "security_assessment_required",
                    "data_export": "government_approval",
                    "critical_data": "localization_required"
                },
                "encryption_required": True
            },
            {
                "id": "dr_india",
                "zone": "India",
                "countries": ["India"],
                "regulations": ["DPDP", "IT Act"],
                "storage_locations": ["ap-south-1", "asia-south1"],
                "transfer_restrictions": {
                    "to_us": "contract_required",
                    "to_eu": "consent_required",
                    "sensitive_data": "localization_required"
                },
                "encryption_required": True
            },
            {
                "id": "dr_latam",
                "zone": "LATAM",
                "countries": ["Brazil", "Argentina", "Chile", "Colombia"],
                "regulations": ["LGPD", "LPDP"],
                "storage_locations": ["sa-east-1", "southamerica-east1"],
                "transfer_restrictions": {
                    "to_us": "standard_clauses",
                    "to_eu": "adequacy_or_clauses",
                    "within_latam": "minimal_restrictions"
                },
                "encryption_required": True
            }
        ]
        
        return data_residency_zones


class HolidaysGenerator(BaseGenerator):
    """Generate holiday data for 2024-2025"""
    
    def generate(self) -> List[Dict[str, Any]]:
        holidays = []
        holiday_id = 1
        
        # US holidays
        us_holidays_2024 = [
            {"name": "New Year's Day", "date": "2024-01-01", "offices": ["office_1", "office_2"]},
            {"name": "Martin Luther King Jr. Day", "date": "2024-01-15", "offices": ["office_1", "office_2"]},
            {"name": "Presidents Day", "date": "2024-02-19", "offices": ["office_1", "office_2"]},
            {"name": "Memorial Day", "date": "2024-05-27", "offices": ["office_1", "office_2"]},
            {"name": "Independence Day", "date": "2024-07-04", "offices": ["office_1", "office_2"]},
            {"name": "Labor Day", "date": "2024-09-02", "offices": ["office_1", "office_2"]},
            {"name": "Thanksgiving", "date": "2024-11-28", "offices": ["office_1", "office_2"]},
            {"name": "Day after Thanksgiving", "date": "2024-11-29", "offices": ["office_1", "office_2"]},
            {"name": "Christmas Day", "date": "2024-12-25", "offices": ["office_1", "office_2"]}
        ]
        
        # UK holidays
        uk_holidays_2024 = [
            {"name": "New Year's Day", "date": "2024-01-01", "offices": ["office_3"]},
            {"name": "Good Friday", "date": "2024-03-29", "offices": ["office_3"]},
            {"name": "Easter Monday", "date": "2024-04-01", "offices": ["office_3"]},
            {"name": "Early May Bank Holiday", "date": "2024-05-06", "offices": ["office_3"]},
            {"name": "Spring Bank Holiday", "date": "2024-05-27", "offices": ["office_3"]},
            {"name": "Summer Bank Holiday", "date": "2024-08-26", "offices": ["office_3"]},
            {"name": "Christmas Day", "date": "2024-12-25", "offices": ["office_3"]},
            {"name": "Boxing Day", "date": "2024-12-26", "offices": ["office_3"]}
        ]
        
        # German holidays
        de_holidays_2024 = [
            {"name": "New Year's Day", "date": "2024-01-01", "offices": ["office_4"]},
            {"name": "Good Friday", "date": "2024-03-29", "offices": ["office_4"]},
            {"name": "Easter Monday", "date": "2024-04-01", "offices": ["office_4"]},
            {"name": "Labour Day", "date": "2024-05-01", "offices": ["office_4"]},
            {"name": "Ascension Day", "date": "2024-05-09", "offices": ["office_4"]},
            {"name": "Whit Monday", "date": "2024-05-20", "offices": ["office_4"]},
            {"name": "German Unity Day", "date": "2024-10-03", "offices": ["office_4"]},
            {"name": "Christmas Day", "date": "2024-12-25", "offices": ["office_4"]},
            {"name": "Boxing Day", "date": "2024-12-26", "offices": ["office_4"]}
        ]
        
        # French holidays
        fr_holidays_2024 = [
            {"name": "New Year's Day", "date": "2024-01-01", "offices": ["office_5"]},
            {"name": "Easter Monday", "date": "2024-04-01", "offices": ["office_5"]},
            {"name": "Labour Day", "date": "2024-05-01", "offices": ["office_5"]},
            {"name": "Victory in Europe Day", "date": "2024-05-08", "offices": ["office_5"]},
            {"name": "Ascension Day", "date": "2024-05-09", "offices": ["office_5"]},
            {"name": "Whit Monday", "date": "2024-05-20", "offices": ["office_5"]},
            {"name": "Bastille Day", "date": "2024-07-14", "offices": ["office_5"]},
            {"name": "Assumption Day", "date": "2024-08-15", "offices": ["office_5"]},
            {"name": "All Saints' Day", "date": "2024-11-01", "offices": ["office_5"]},
            {"name": "Armistice Day", "date": "2024-11-11", "offices": ["office_5"]},
            {"name": "Christmas Day", "date": "2024-12-25", "offices": ["office_5"]}
        ]
        
        # Japanese holidays
        jp_holidays_2024 = [
            {"name": "New Year's Day", "date": "2024-01-01", "offices": ["office_6"]},
            {"name": "Coming of Age Day", "date": "2024-01-08", "offices": ["office_6"]},
            {"name": "National Foundation Day", "date": "2024-02-11", "offices": ["office_6"]},
            {"name": "Emperor's Birthday", "date": "2024-02-23", "offices": ["office_6"]},
            {"name": "Vernal Equinox Day", "date": "2024-03-20", "offices": ["office_6"]},
            {"name": "Showa Day", "date": "2024-04-29", "offices": ["office_6"]},
            {"name": "Constitution Memorial Day", "date": "2024-05-03", "offices": ["office_6"]},
            {"name": "Greenery Day", "date": "2024-05-04", "offices": ["office_6"]},
            {"name": "Children's Day", "date": "2024-05-05", "offices": ["office_6"]},
            {"name": "Marine Day", "date": "2024-07-15", "offices": ["office_6"]},
            {"name": "Mountain Day", "date": "2024-08-11", "offices": ["office_6"]},
            {"name": "Respect for the Aged Day", "date": "2024-09-16", "offices": ["office_6"]},
            {"name": "Autumnal Equinox Day", "date": "2024-09-22", "offices": ["office_6"]},
            {"name": "Health and Sports Day", "date": "2024-10-14", "offices": ["office_6"]},
            {"name": "Culture Day", "date": "2024-11-03", "offices": ["office_6"]},
            {"name": "Labour Thanksgiving Day", "date": "2024-11-23", "offices": ["office_6"]}
        ]
        
        # HK holidays
        hk_holidays_2024 = [
            {"name": "New Year's Day", "date": "2024-01-01", "offices": ["office_7"]},
            {"name": "Lunar New Year's Day", "date": "2024-02-10", "offices": ["office_7"]},
            {"name": "Lunar New Year's Day 2", "date": "2024-02-11", "offices": ["office_7"]},
            {"name": "Lunar New Year's Day 3", "date": "2024-02-12", "offices": ["office_7"]},
            {"name": "Good Friday", "date": "2024-03-29", "offices": ["office_7"]},
            {"name": "Easter Monday", "date": "2024-04-01", "offices": ["office_7"]},
            {"name": "Ching Ming Festival", "date": "2024-04-04", "offices": ["office_7"]},
            {"name": "Labour Day", "date": "2024-05-01", "offices": ["office_7"]},
            {"name": "Buddha's Birthday", "date": "2024-05-15", "offices": ["office_7"]},
            {"name": "Tuen Ng Festival", "date": "2024-06-10", "offices": ["office_7"]},
            {"name": "Hong Kong SAR Establishment Day", "date": "2024-07-01", "offices": ["office_7"]},
            {"name": "Mid-Autumn Festival", "date": "2024-09-18", "offices": ["office_7"]},
            {"name": "National Day", "date": "2024-10-01", "offices": ["office_7"]},
            {"name": "Chung Yeung Festival", "date": "2024-10-11", "offices": ["office_7"]},
            {"name": "Christmas Day", "date": "2024-12-25", "offices": ["office_7"]},
            {"name": "Boxing Day", "date": "2024-12-26", "offices": ["office_7"]}
        ]
        
        # Australian holidays
        au_holidays_2024 = [
            {"name": "New Year's Day", "date": "2024-01-01", "offices": ["office_8"]},
            {"name": "Australia Day", "date": "2024-01-26", "offices": ["office_8"]},
            {"name": "Good Friday", "date": "2024-03-29", "offices": ["office_8"]},
            {"name": "Easter Saturday", "date": "2024-03-30", "offices": ["office_8"]},
            {"name": "Easter Monday", "date": "2024-04-01", "offices": ["office_8"]},
            {"name": "ANZAC Day", "date": "2024-04-25", "offices": ["office_8"]},
            {"name": "Queen's Birthday", "date": "2024-06-10", "offices": ["office_8"]},
            {"name": "Bank Holiday", "date": "2024-08-05", "offices": ["office_8"]},
            {"name": "Labour Day", "date": "2024-10-07", "offices": ["office_8"]},
            {"name": "Christmas Day", "date": "2024-12-25", "offices": ["office_8"]},
            {"name": "Boxing Day", "date": "2024-12-26", "offices": ["office_8"]}
        ]
        
        # Combine all holidays and add metadata
        all_holidays = (
            us_holidays_2024 + uk_holidays_2024 + de_holidays_2024 + 
            fr_holidays_2024 + jp_holidays_2024 + hk_holidays_2024 + au_holidays_2024
        )
        
        for holiday_data in all_holidays:
            holiday = {
                "id": f"holiday_{holiday_id}",
                "name": holiday_data["name"],
                "date": holiday_data["date"],
                "type": "public" if "Bank" not in holiday_data["name"] else "bank",
                "recurring": True,
                "offices": holiday_data["offices"],
                "impact": "office_closed",
                "coverage_required": "24/7" in holiday_data["name"] or "Christmas" in holiday_data["name"]
            }
            holidays.append(holiday)
            holiday_id += 1
        
        # Add 2025 holidays (subset for continuity)
        holidays_2025 = [
            {"id": f"holiday_{holiday_id}", "name": "New Year's Day", "date": "2025-01-01", "type": "public", "recurring": True, 
             "offices": ["office_1", "office_2", "office_3", "office_4", "office_5", "office_6", "office_7", "office_8"], 
             "impact": "office_closed", "coverage_required": True},
            # Add more as needed...
        ]
        holidays.extend(holidays_2025)
        
        return holidays
