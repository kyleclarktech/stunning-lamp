#!/usr/bin/env python3
"""
Database initialization script that can be run standalone to seed the database.
This ensures the database is seeded when containers start up.
"""

import os
import time
import sys
from dotenv import load_dotenv
from seed_data import seed_database
import falkordb

def wait_for_falkordb(host, port, max_retries=30, delay=2):
    """Wait for FalkorDB to be ready"""
    print(f"⏳ Waiting for FalkorDB at {host}:{port}...")
    
    for attempt in range(max_retries):
        try:
            falkor_client = falkordb.FalkorDB(host=host, port=port, socket_connect_timeout=5, socket_timeout=5)
            db = falkor_client.select_graph("test_connection")
            db.query("RETURN 1")
            print("✅ FalkorDB is ready!")
            return True
        except Exception as e:
            print(f"⏳ Attempt {attempt + 1}/{max_retries}: FalkorDB not ready yet ({e})")
            time.sleep(delay)
    
    print("❌ FalkorDB failed to become ready")
    return False

def setup_ai_service():
    """Setup AI service if Ollama is enabled"""
    use_ollama = os.getenv('USE_OLLAMA', '').lower() in ('true', '1', 'yes')
    if use_ollama:
        print("🤖 Ollama enabled, checking setup...")
        try:
            from setup_ollama import setup_ollama
            setup_ollama()
        except Exception as e:
            print(f"⚠️  Ollama setup failed: {e}")
            print("Continuing with database initialization...")
    else:
        print("🧠 Using Claude AI service")

def main():
    # Load environment variables
    load_dotenv()
    
    # Setup AI service
    setup_ai_service()
    
    # Get FalkorDB connection details
    host = os.getenv('FALKOR_HOST', 'falkordb')
    port = int(os.getenv('FALKOR_PORT', 6379))
    
    # Wait for FalkorDB to be ready
    if not wait_for_falkordb(host, port):
        print("❌ Failed to connect to FalkorDB, exiting...")
        sys.exit(1)
    
    try:
        # Connect to FalkorDB
        falkor_client = falkordb.FalkorDB(host=host, port=port)
        db = falkor_client.select_graph('agent_poc')
        
        # Check if database is already seeded
        try:
            result = db.query('MATCH (s:SeedStats) RETURN s.people_count, s.teams_count')
            if result.result_set:
                stats = result.result_set[0]
                print(f'✅ Database already seeded with {stats[0]} people, {stats[1]} teams')
                return
        except Exception:
            pass  # Database might not exist yet, continue with seeding
        
        # Seed the database
        print('🌱 Database is empty, seeding now...')
        seed_database(falkor_client)
        print('✅ Database seeding completed successfully!')
        
    except Exception as e:
        print(f'❌ Error during database initialization: {e}')
        sys.exit(1)

if __name__ == "__main__":
    main()