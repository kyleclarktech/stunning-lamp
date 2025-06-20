#!/usr/bin/env python3
"""
Data validation tool to ensure database is properly seeded and consistent.
Checks for data integrity, relationship consistency, and common issues.
"""

import falkordb
import os
import sys
import json
from datetime import datetime
from typing import Dict, List, Any, Tuple
from dotenv import load_dotenv
from collections import defaultdict

# Load environment variables
load_dotenv()


class DataValidator:
    """Validates FalkorDB data integrity and consistency"""
    
    def __init__(self):
        self.falkor_client = None
        self.db = None
        self.issues = []
        self.warnings = []
        self.stats = {}
        self._setup_database()
    
    def _setup_database(self):
        """Setup database connection"""
        try:
            host = os.getenv('FALKOR_HOST', 'localhost')
            port = int(os.getenv('FALKOR_PORT', 6379))
            self.falkor_client = falkordb.FalkorDB(host=host, port=port)
            self.db = self.falkor_client.select_graph("agent_poc")
            print(f"✅ Connected to FalkorDB at {host}:{port}")
        except Exception as e:
            print(f"❌ Failed to connect to FalkorDB: {e}")
            sys.exit(1)
    
    def validate_all(self) -> Dict[str, Any]:
        """Run all validation checks"""
        print("\n🔍 Starting comprehensive data validation...")
        
        # Reset state
        self.issues = []
        self.warnings = []
        self.stats = {}
        
        # Run validations
        self._validate_node_counts()
        self._validate_node_properties()
        self._validate_relationships()
        self._validate_data_consistency()
        self._validate_business_rules()
        self._check_orphaned_entities()
        self._validate_hierarchies()
        self._check_data_distribution()
        
        # Generate summary
        summary = {
            "timestamp": datetime.now().isoformat(),
            "stats": self.stats,
            "issues": self.issues,
            "warnings": self.warnings,
            "issue_count": len(self.issues),
            "warning_count": len(self.warnings),
            "valid": len(self.issues) == 0
        }
        
        return summary
    
    def _validate_node_counts(self):
        """Validate expected node counts"""
        print("\n📊 Validating node counts...")
        
        expected_ranges = {
            "Person": (400, 600),  # ~500 expected
            "Team": (30, 40),      # ~35 expected
            "Group": (10, 20),     # ~15 expected
            "Policy": (15, 25),    # ~20 expected
            "Message": (0, None),  # Any number is valid
        }
        
        for node_type, (min_count, max_count) in expected_ranges.items():
            result = self.db.query(f"MATCH (n:{node_type}) RETURN count(n) as count")
            count = result.result_set[0][0] if result.result_set else 0
            
            self.stats[f"{node_type.lower()}_count"] = count
            
            if min_count and count < min_count:
                self.issues.append(f"Too few {node_type} nodes: {count} (expected at least {min_count})")
            elif max_count and count > max_count:
                self.issues.append(f"Too many {node_type} nodes: {count} (expected at most {max_count})")
            
            print(f"  {node_type}: {count} nodes")
    
    def _validate_node_properties(self):
        """Validate required properties exist and are non-null"""
        print("\n🏷️  Validating node properties...")
        
        required_properties = {
            "Person": ["id", "name", "email", "department", "role"],
            "Team": ["id", "name", "department"],
            "Group": ["id", "name", "type"],
            "Policy": ["id", "name", "category", "severity"]
        }
        
        for node_type, properties in required_properties.items():
            for prop in properties:
                # Check for null values
                result = self.db.query(
                    f"MATCH (n:{node_type}) WHERE n.{prop} IS NULL RETURN count(n) as count"
                )
                null_count = result.result_set[0][0] if result.result_set else 0
                
                if null_count > 0:
                    self.issues.append(
                        f"{null_count} {node_type} nodes have null {prop}"
                    )
                
                # Check for empty strings
                result = self.db.query(
                    f"MATCH (n:{node_type}) WHERE n.{prop} = '' RETURN count(n) as count"
                )
                empty_count = result.result_set[0][0] if result.result_set else 0
                
                if empty_count > 0:
                    self.issues.append(
                        f"{empty_count} {node_type} nodes have empty {prop}"
                    )
    
    def _validate_relationships(self):
        """Validate relationship counts and consistency"""
        print("\n🔗 Validating relationships...")
        
        relationship_checks = [
            ("Person", "MEMBER_OF", "Team", True),  # Required
            ("Person", "MEMBER_OF", "Group", False),  # Optional
            ("Person", "REPORTS_TO", "Person", False),  # Optional
            ("Team", "RESPONSIBLE_FOR", "Policy", False),  # Optional
            ("Group", "RESPONSIBLE_FOR", "Policy", False),  # Optional
        ]
        
        for from_type, rel_type, to_type, required in relationship_checks:
            # Count relationships
            result = self.db.query(
                f"MATCH (:{from_type})-[r:{rel_type}]->(:{to_type}) RETURN count(r) as count"
            )
            count = result.result_set[0][0] if result.result_set else 0
            
            stat_key = f"{from_type.lower()}_{rel_type.lower()}_{to_type.lower()}"
            self.stats[stat_key] = count
            
            print(f"  {from_type}-[{rel_type}]->{to_type}: {count}")
            
            if required and count == 0:
                self.issues.append(f"No {rel_type} relationships between {from_type} and {to_type}")
    
    def _validate_data_consistency(self):
        """Check for data consistency issues"""
        print("\n🔄 Validating data consistency...")
        
        # Check for duplicate IDs within each node type
        node_types = ["Person", "Team", "Group", "Policy"]
        for node_type in node_types:
            result = self.db.query(
                f"MATCH (n:{node_type}) WITH n.id as id, count(n) as count "
                f"WHERE count > 1 RETURN id, count"
            )
            
            if result.result_set:
                for row in result.result_set:
                    self.issues.append(
                        f"Duplicate {node_type} ID: {row[0]} appears {row[1]} times"
                    )
        
        # Check email uniqueness
        result = self.db.query(
            "MATCH (p:Person) WITH p.email as email, count(p) as count "
            "WHERE count > 1 RETURN email, count"
        )
        
        if result.result_set:
            for row in result.result_set:
                self.warnings.append(
                    f"Duplicate email: {row[0]} used by {row[1]} people"
                )
        
        # Check that managers exist
        result = self.db.query(
            "MATCH (p:Person) WHERE p.manager_id IS NOT NULL AND p.manager_id <> '' "
            "AND NOT EXISTS((p)-[:REPORTS_TO]->(:Person)) "
            "RETURN count(p) as count"
        )
        orphan_count = result.result_set[0][0] if result.result_set else 0
        
        if orphan_count > 0:
            self.issues.append(
                f"{orphan_count} people have manager_id but no REPORTS_TO relationship"
            )
    
    def _validate_business_rules(self):
        """Validate business logic rules"""
        print("\n📋 Validating business rules...")
        
        # Check that each person belongs to exactly one team
        result = self.db.query(
            "MATCH (p:Person) "
            "WITH p, count((p)-[:MEMBER_OF]->(:Team)) as team_count "
            "WHERE team_count = 0 "
            "RETURN count(p) as count"
        )
        no_team_count = result.result_set[0][0] if result.result_set else 0
        
        if no_team_count > 0:
            self.issues.append(f"{no_team_count} people don't belong to any team")
        
        result = self.db.query(
            "MATCH (p:Person) "
            "WITH p, count((p)-[:MEMBER_OF]->(:Team)) as team_count "
            "WHERE team_count > 1 "
            "RETURN count(p) as count"
        )
        multi_team_count = result.result_set[0][0] if result.result_set else 0
        
        if multi_team_count > 0:
            self.warnings.append(f"{multi_team_count} people belong to multiple teams")
        
        # Check that teams and people are in matching departments
        result = self.db.query(
            "MATCH (p:Person)-[:MEMBER_OF]->(t:Team) "
            "WHERE p.department <> t.department "
            "RETURN count(p) as count"
        )
        mismatch_count = result.result_set[0][0] if result.result_set else 0
        
        if mismatch_count > 0:
            self.warnings.append(
                f"{mismatch_count} people in teams from different departments"
            )
        
        # Check that all policies have at least one owner
        result = self.db.query(
            "MATCH (p:Policy) WHERE NOT (()-[:RESPONSIBLE_FOR]->(p)) "
            "RETURN count(p) as count"
        )
        orphan_policy_count = result.result_set[0][0] if result.result_set else 0
        
        if orphan_policy_count > 0:
            self.issues.append(f"{orphan_policy_count} policies have no owners")
        
        # Check critical policies have owners
        result = self.db.query(
            "MATCH (p:Policy) WHERE p.severity = 'critical' "
            "AND NOT (()-[:RESPONSIBLE_FOR]->(p)) "
            "RETURN p.name"
        )
        
        if result.result_set:
            for row in result.result_set:
                self.issues.append(f"Critical policy '{row[0]}' has no owner")
    
    def _check_orphaned_entities(self):
        """Check for orphaned entities"""
        print("\n🔍 Checking for orphaned entities...")
        
        # Teams with no members
        result = self.db.query(
            "MATCH (t:Team) WHERE NOT ((:Person)-[:MEMBER_OF]->(t)) "
            "RETURN t.name"
        )
        
        if result.result_set:
            for row in result.result_set:
                self.warnings.append(f"Team '{row[0]}' has no members")
        
        # Groups with no members
        result = self.db.query(
            "MATCH (g:Group) WHERE NOT ((:Person)-[:MEMBER_OF]->(g)) "
            "RETURN g.name"
        )
        
        if result.result_set:
            for row in result.result_set:
                self.warnings.append(f"Group '{row[0]}' has no members")
    
    def _validate_hierarchies(self):
        """Validate management hierarchies"""
        print("\n👥 Validating hierarchies...")
        
        # Check for circular reporting relationships
        result = self.db.query(
            "MATCH path = (p:Person)-[:REPORTS_TO*]->(p) "
            "RETURN p.name"
        )
        
        if result.result_set:
            for row in result.result_set:
                self.issues.append(f"Circular reporting: {row[0]} reports to themselves")
        
        # Check reporting depth
        result = self.db.query(
            "MATCH path = (p:Person)-[:REPORTS_TO*]->(m:Person) "
            "WHERE NOT (m)-[:REPORTS_TO]->() "
            "WITH p, length(path) as depth "
            "WHERE depth > 5 "
            "RETURN p.name, depth"
        )
        
        if result.result_set:
            for row in result.result_set:
                self.warnings.append(
                    f"Deep hierarchy: {row[0]} is {row[1]} levels from top"
                )
    
    def _check_data_distribution(self):
        """Check data distribution for anomalies"""
        print("\n📈 Checking data distribution...")
        
        # Department distribution
        result = self.db.query(
            "MATCH (p:Person) "
            "RETURN p.department, count(p) as count "
            "ORDER BY count DESC"
        )
        
        if result.result_set:
            dept_counts = [(row[0], row[1]) for row in result.result_set]
            total = sum(count for _, count in dept_counts)
            
            print("  Department distribution:")
            for dept, count in dept_counts[:5]:
                percentage = (count / total * 100) if total > 0 else 0
                print(f"    {dept}: {count} ({percentage:.1f}%)")
            
            # Check for severely unbalanced departments
            for dept, count in dept_counts:
                percentage = (count / total * 100) if total > 0 else 0
                if percentage > 40:
                    self.warnings.append(
                        f"Department '{dept}' has {percentage:.1f}% of all people"
                    )
                elif percentage < 1 and count > 0:
                    self.warnings.append(
                        f"Department '{dept}' has only {count} people"
                    )
        
        # Team size distribution
        result = self.db.query(
            "MATCH (p:Person)-[:MEMBER_OF]->(t:Team) "
            "WITH t, count(p) as size "
            "RETURN min(size) as min_size, max(size) as max_size, "
            "avg(size) as avg_size"
        )
        
        if result.result_set:
            row = result.result_set[0]
            min_size, max_size, avg_size = row[0], row[1], row[2]
            
            print(f"  Team sizes: min={min_size}, max={max_size}, avg={avg_size:.1f}")
            
            if max_size > avg_size * 3:
                self.warnings.append(
                    f"Some teams are very large (max: {max_size}, avg: {avg_size:.1f})"
                )
            if min_size < 2:
                self.warnings.append("Some teams have fewer than 2 members")
    
    def generate_fix_script(self) -> str:
        """Generate Cypher queries to fix identified issues"""
        fixes = []
        
        for issue in self.issues:
            if "don't belong to any team" in issue:
                fixes.append(
                    "// Fix: Assign orphaned people to teams\n"
                    "MATCH (p:Person) WHERE NOT (p)-[:MEMBER_OF]->(:Team)\n"
                    "MATCH (t:Team) WHERE t.department = p.department\n"
                    "WITH p, t ORDER BY rand() LIMIT 1\n"
                    "CREATE (p)-[:MEMBER_OF {role: p.role, is_lead: false}]->(t)"
                )
            
            elif "policies have no owners" in issue:
                fixes.append(
                    "// Fix: Assign orphaned policies to groups\n"
                    "MATCH (p:Policy) WHERE NOT (()-[:RESPONSIBLE_FOR]->(p))\n"
                    "MATCH (g:Group) WHERE g.type = 'governance'\n"
                    "WITH p, g ORDER BY rand() LIMIT 1\n"
                    "CREATE (g)-[:RESPONSIBLE_FOR {responsibility_type: 'owner', "
                    "assigned_date: date().year + '-' + date().month + '-' + date().day}]->(p)"
                )
        
        return "\n\n".join(fixes) if fixes else "// No automatic fixes available"


def main():
    """Main entry point"""
    print("🏥 FalkorDB Data Validation Tool")
    print("=" * 60)
    
    validator = DataValidator()
    summary = validator.validate_all()
    
    # Print results
    print("\n" + "=" * 60)
    print("VALIDATION SUMMARY")
    print("=" * 60)
    
    print(f"\n📊 Statistics:")
    for key, value in summary["stats"].items():
        print(f"  {key}: {value}")
    
    if summary["issues"]:
        print(f"\n❌ Issues Found ({len(summary['issues'])}):")
        for issue in summary["issues"]:
            print(f"  - {issue}")
    
    if summary["warnings"]:
        print(f"\n⚠️  Warnings ({len(summary['warnings'])}):")
        for warning in summary["warnings"]:
            print(f"  - {warning}")
    
    if summary["valid"]:
        print("\n✅ Database validation PASSED")
    else:
        print("\n❌ Database validation FAILED")
        
        # Generate fixes
        print("\n🔧 Suggested fixes:")
        fix_script = validator.generate_fix_script()
        print(fix_script)
    
    # Save detailed report
    report_file = f"validation_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(report_file, 'w') as f:
        json.dump(summary, f, indent=2)
    
    print(f"\n📄 Detailed report saved to: {report_file}")
    
    # Exit with appropriate code
    sys.exit(0 if summary["valid"] else 1)


if __name__ == "__main__":
    main()