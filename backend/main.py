import asyncio
import json
import os
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
import falkordb
import re
import anthropic
import ollama
from jinja2 import Template
from pathlib import Path
from dotenv import load_dotenv
from seed_data import seed_database

# Load environment variables from .env file
load_dotenv()

app = FastAPI()

# Add CORS middleware to allow frontend connections
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def startup_event():
    """Ensure database is seeded on application startup"""
    print("🚀 Starting application and checking database...")
    try:
        ensure_database_seeded()
        print("✅ Database initialization completed")
    except Exception as e:
        print(f"❌ Database initialization failed: {e}")
        # Don't raise to prevent app from failing to start

def get_ai_provider():
    """Determine which AI provider to use based on environment variables"""
    use_ollama = os.getenv('USE_OLLAMA', '').lower() in ('true', '1', 'yes')
    return 'ollama' if use_ollama else 'claude'

def get_claude_client():
    api_key = os.getenv('ANTHROPIC_API_KEY')
    if not api_key:
        raise ValueError("ANTHROPIC_API_KEY environment variable not set")
    return anthropic.Anthropic(api_key=api_key)

def get_ollama_client():
    """Get Ollama client and configuration"""
    host = os.getenv('OLLAMA_HOST', 'http://localhost:11434')
    model = os.getenv('OLLAMA_MODEL', 'llama2')
    
    client = ollama.Client(host=host)
    
    # Test connection by trying to list models
    try:
        models = client.list()
        available_models = [m['name'] for m in models['models']]
        if model not in available_models:
            print(f"Warning: Model '{model}' not found. Available models: {available_models}")
            if available_models:
                model = available_models[0]
                print(f"Using first available model: {model}")
    except Exception as e:
        print(f"Warning: Could not connect to Ollama at {host}: {e}")
    
    return client, model

def get_falkor_client():
    host = os.getenv('FALKOR_HOST', 'falkordb')  # Use Docker service name
    port = int(os.getenv('FALKOR_PORT', 6379))
    
    try:
        # Add connection timeout to prevent hanging
        falkor_client = falkordb.FalkorDB(host=host, port=port, socket_connect_timeout=10, socket_timeout=10)
        
        # Test connection
        db = falkor_client.select_graph("agent_poc")
        
        return falkor_client
        
    except Exception as e:
        print(f"Failed to connect to FalkorDB at {host}:{port} - {str(e)}")
        print("Make sure FalkorDB is running and accessible")
        raise e

def ensure_database_seeded():
    """Ensure database is seeded on startup"""
    try:
        falkor_client = get_falkor_client()
        db = falkor_client.select_graph("agent_poc")
        
        # Check if database needs seeding
        try:
            result = db.query("MATCH (s:SeedStats) RETURN s.people_count, s.teams_count")
            if not result.result_set:
                print("Database is empty, seeding with test data...")
                seed_database(falkor_client)
            else:
                stats = result.result_set[0]
                print(f"Database already seeded with {stats[0]} people, {stats[1]} teams")
        except Exception as e:
            print(f"Error checking seed status: {e}")
            print("Attempting to seed database...")
            try:
                seed_database(falkor_client)
            except Exception as seed_error:
                print(f"Error seeding database: {seed_error}")
                
    except Exception as e:
        print(f"Failed to ensure database seeded: {e}")

def to_pig_latin(text):
    """Convert text to pig latin"""
    words = text.split()
    pig_latin_words = []
    
    for word in words:
        # Handle punctuation
        punctuation = ""
        clean_word = word
        if word and not word[-1].isalpha():
            punctuation = word[-1]
            clean_word = word[:-1]
        
        if not clean_word:
            pig_latin_words.append(word)
            continue
            
        # Convert to lowercase for processing, preserve original case
        original_case = clean_word
        word_lower = clean_word.lower()
        
        # Check if word starts with vowel
        if word_lower[0] in 'aeiou':
            pig_latin = word_lower + '-way'
        else:
            # Find first vowel
            vowel_index = 0
            for i, char in enumerate(word_lower):
                if char in 'aeiou':
                    vowel_index = i
                    break
            else:
                vowel_index = len(word_lower)
            
            consonant_cluster = word_lower[:vowel_index]
            rest = word_lower[vowel_index:]
            pig_latin = rest + '-' + consonant_cluster + 'ay'
        
        # Preserve original capitalization
        if original_case[0].isupper():
            pig_latin = pig_latin.capitalize()
        if original_case.isupper():
            pig_latin = pig_latin.upper()
            
        pig_latin_words.append(pig_latin + punctuation)
    
    return ' '.join(pig_latin_words)

def load_prompt(prompt_name, **kwargs):
    """Load and interpolate a prompt file"""
    prompt_path = Path(f"prompts/{prompt_name}.txt")
    if not prompt_path.exists():
        raise FileNotFoundError(f"Prompt file not found: {prompt_path}")
    
    with open(prompt_path, 'r') as f:
        template_content = f.read()
    
    template = Template(template_content)
    rendered = template.render(**kwargs)
    return rendered

async def call_ai_model(prompt_text, websocket=None, timeout=30):
    """Call AI model (Claude or Ollama) with the given prompt"""
    provider = get_ai_provider()
    
    try:
        if websocket:
            # Determine message based on prompt content
            if "generate_query" in prompt_text:
                # Extract user message from generate_query prompt for detailed reasoning
                user_message = None
                if 'User request: "' in prompt_text:
                    start = prompt_text.find('User request: "') + len('User request: "')
                    end = prompt_text.find('"', start)
                    if end > start:
                        user_message = prompt_text[start:end]
                
                if user_message:
                    reasoning, policy = analyze_query_reasoning(user_message)
                    message = f"Generating database query based on: {reasoning}"
                    if policy:
                        message += f" (applying policy: {policy})"
                    message += "..."
                else:
                    message = "Preparing database query..."
                    
                await websocket.send_text(json.dumps({
                    "type": "info",
                    "message": message
                }))
            elif "analyze_message" in prompt_text:
                await websocket.send_text(json.dumps({
                    "type": "info",
                    "message": "Analyzing request to determine the most appropriate response approach..."
                }))
            elif "format_results" in prompt_text:
                await websocket.send_text(json.dumps({
                    "type": "info", 
                    "message": "Processing and formatting query results for display..."
                }))
        
        if provider == 'ollama':
            return await call_ollama(prompt_text, timeout)
        else:
            return await call_claude(prompt_text, timeout)
            
    except asyncio.TimeoutError:
        # Timeout errors are handled by caller
        raise Exception(f"AI model timeout after {timeout} seconds")
    except Exception as e:
        # Check for specific API errors
        error_message = str(e)
        
        # Handle 529 Overloaded response (Claude)
        if "529" in error_message or "overloaded" in error_message.lower():
            raise Exception("🚦 AI service is experiencing high demand right now. Please try again in a few moments.")
        
        # Handle rate limiting
        if "429" in error_message or "rate limit" in error_message.lower():
            raise Exception("⏳ Too many requests. Please wait a moment before trying again.")
        
        # Handle authentication errors
        if "401" in error_message or "unauthorized" in error_message.lower():
            raise Exception("🔑 Authentication issue with AI service. Please contact support.")
        
        # Handle quota/billing errors
        if "402" in error_message or "quota" in error_message.lower() or "billing" in error_message.lower():
            raise Exception("💳 AI service quota exceeded. Please contact support.")
        
        # Handle connection errors (Ollama)
        if "connection" in error_message.lower() or "refused" in error_message.lower():
            if provider == 'ollama':
                raise Exception("🔌 Local AI service is not available. Please ensure Ollama is running.")
            else:
                raise Exception("🌐 AI service temporarily unavailable. Please try again in a moment.")
        
        # Handle generic API errors
        if "api" in error_message.lower() or "http" in error_message.lower():
            raise Exception("🌐 AI service temporarily unavailable. Please try again in a moment.")
        
        # For unknown errors, pass through
        raise e

async def call_claude(prompt_text, timeout=30):
    """Call Claude API with the given prompt"""
    client = get_claude_client()
    
    # Wrap the synchronous call in asyncio.wait_for for timeout
    response = await asyncio.wait_for(
        asyncio.get_event_loop().run_in_executor(
            None,
            lambda: client.messages.create(
                model="claude-sonnet-4-20250514", #"claude-3-5-haiku-20241022",
                max_tokens=1000,
                messages=[
                    {"role": "user", "content": prompt_text}
                ]
            )
        ),
        timeout=timeout
    )
    
    response_text = response.content[0].text
    return response_text

async def call_ollama(prompt_text, timeout=30):
    """Call Ollama API with the given prompt"""
    client, model = get_ollama_client()
    
    # Wrap the synchronous call in asyncio.wait_for for timeout
    response = await asyncio.wait_for(
        asyncio.get_event_loop().run_in_executor(
            None,
            lambda: client.chat(
                model=model,
                messages=[
                    {"role": "user", "content": prompt_text}
                ]
            )
        ),
        timeout=timeout
    )
    
    return response['message']['content']

async def get_database_context():
    """Get sample data from the database to provide context"""
    try:
        
        # Wrap database operations in executor with timeout
        def get_db_connection():
            falkor = get_falkor_client()
            return falkor.select_graph("agent_poc")
        
        db = await asyncio.wait_for(
            asyncio.get_event_loop().run_in_executor(None, get_db_connection),
            timeout=10
        )
        
        # Get sample counts and structure
        context = {
            "people_count": 0,
            "teams_count": 0,
            "groups_count": 0,
            "policies_count": 0,
            "sample_departments": [],
            "sample_teams": [],
            "sample_groups": []
        }
        
        # Helper function to run database queries with timeout
        async def run_query(query_desc, query):
            try:
                result = await asyncio.wait_for(
                    asyncio.get_event_loop().run_in_executor(
                        None, lambda: db.query(query)
                    ),
                    timeout=5
                )
                return result
            except asyncio.TimeoutError:
                print(f"Database query timeout for {query_desc}: {query}")
                return None
            except Exception as e:
                print(f"Database query error for {query_desc}: {str(e)} - Query: {query}")
                return None

        # Get counts
        result = await run_query("person count", "MATCH (p:Person) RETURN count(p) as count")
        if result and result.result_set:
            context["people_count"] = result.result_set[0][0]
            
        result = await run_query("team count", "MATCH (t:Team) RETURN count(t) as count")
        if result and result.result_set:
            context["teams_count"] = result.result_set[0][0]
            
        result = await run_query("group count", "MATCH (g:Group) RETURN count(g) as count")
        if result and result.result_set:
            context["groups_count"] = result.result_set[0][0]
            
        result = await run_query("policy count", "MATCH (p:Policy) RETURN count(p) as count")
        if result and result.result_set:
            context["policies_count"] = result.result_set[0][0]
        
        # Get sample departments
        result = await run_query("sample departments", "MATCH (p:Person) RETURN DISTINCT p.department LIMIT 5")
        if result and result.result_set:
            context["sample_departments"] = [row[0] for row in result.result_set]
            
        # Get sample teams
        result = await run_query("sample teams", "MATCH (t:Team) RETURN t.name, t.department LIMIT 3")
        if result and result.result_set:
            context["sample_teams"] = [{"name": row[0], "department": row[1]} for row in result.result_set]
            
        # Get sample groups
        result = await run_query("sample groups", "MATCH (g:Group) RETURN g.name, g.type LIMIT 3")
        if result and result.result_set:
            context["sample_groups"] = [{"name": row[0], "type": row[1]} for row in result.result_set]
        
        return context
    except Exception as e:
        return {
            "people_count": 0,
            "teams_count": 0,
            "groups_count": 0,
            "policies_count": 0,
            "sample_departments": [],
            "sample_teams": [],
            "sample_groups": [],
            "error": str(e)
        }

async def search_database(query, websocket=None):
    """Search the database for corporate data and messages"""
    try:
        # Search operation happens quickly, no need for info message
        
        def get_search_db():
            falkor = get_falkor_client()
            return falkor.select_graph("agent_poc")
        
        db = await asyncio.wait_for(
            asyncio.get_event_loop().run_in_executor(None, get_search_db),
            timeout=10
        )
        
        search_results = {
            "people": [],
            "teams": [],
            "groups": [],
            "policies": [],
            "messages": []
        }
        
        query_lower = query.lower()
        
        # Helper function for executing search queries with timeout
        async def execute_search_query(query_desc, cypher_query):
            try:
                result = await asyncio.wait_for(
                    asyncio.get_event_loop().run_in_executor(
                        None, lambda: db.query(cypher_query)
                    ),
                    timeout=8
                )
                return result
            except asyncio.TimeoutError:
                if websocket:
                    await websocket.send_text(json.dumps({
                        "type": "error",
                        "message": f"Search query timeout for {query_desc}: {cypher_query}"
                    }))
                print(f"Search query timeout for {query_desc}: {cypher_query}")
                return None
            except Exception as e:
                if websocket:
                    await websocket.send_text(json.dumps({
                        "type": "error", 
                        "message": f"Search query error for {query_desc}: {str(e)} - Query: {cypher_query}"
                    }))
                print(f"Search query error for {query_desc}: {str(e)} - Query: {cypher_query}")
                return None
        
        # Helper function for executing parameterized search queries with timeout
        async def execute_search_query_with_params(query_desc, cypher_query, params):
            try:
                result = await asyncio.wait_for(
                    asyncio.get_event_loop().run_in_executor(
                        None, lambda: db.query(cypher_query, params)
                    ),
                    timeout=8
                )
                return result
            except asyncio.TimeoutError:
                if websocket:
                    await websocket.send_text(json.dumps({
                        "type": "error",
                        "message": f"Search query timeout for {query_desc}: {cypher_query}"
                    }))
                print(f"Search query timeout for {query_desc}: {cypher_query}")
                return None
            except Exception as e:
                if websocket:
                    await websocket.send_text(json.dumps({
                        "type": "error", 
                        "message": f"Search query error for {query_desc}: {str(e)} - Query: {cypher_query}"
                    }))
                print(f"Search query error for {query_desc}: {str(e)} - Query: {cypher_query}")
                return None
        
        # Search people
        try:
            cypher_query = "MATCH (p:Person) WHERE toLower(p.name) CONTAINS $query OR toLower(p.role) CONTAINS $query OR toLower(p.department) CONTAINS $query RETURN p.name, p.role, p.department, p.email LIMIT 5"
            result = await execute_search_query_with_params("people", cypher_query, {"query": query_lower})
            if result and result.result_set:
                for record in result.result_set:
                    search_results["people"].append({
                        "name": record[0],
                        "role": record[1],
                        "department": record[2],
                        "email": record[3]
                    })
        except Exception as e:
            if websocket:
                await websocket.send_text(json.dumps({
                    "type": "error",
                    "message": f"People search error: {str(e)}"
                }))
            print(f"People search error: {str(e)}")
        
        # Search teams
        try:
            cypher_query = "MATCH (t:Team) WHERE toLower(t.name) CONTAINS $query OR toLower(t.department) CONTAINS $query OR toLower(t.focus) CONTAINS $query RETURN t.name, t.department, t.focus LIMIT 5"
            result = await execute_search_query_with_params("teams", cypher_query, {"query": query_lower})
            if result and result.result_set:
                for record in result.result_set:
                    search_results["teams"].append({
                        "name": record[0],
                        "department": record[1],
                        "focus": record[2]
                    })
        except Exception as e:
            if websocket:
                await websocket.send_text(json.dumps({
                    "type": "error",
                    "message": f"Teams search error: {str(e)}"
                }))
            print(f"Teams search error: {str(e)}")
        
        # Search groups
        try:
            cypher_query = "MATCH (g:Group) WHERE toLower(g.name) CONTAINS $query OR toLower(g.description) CONTAINS $query OR toLower(g.type) CONTAINS $query RETURN g.name, g.type, g.description LIMIT 5"
            result = await execute_search_query_with_params("groups", cypher_query, {"query": query_lower})
            if result and result.result_set:
                for record in result.result_set:
                    search_results["groups"].append({
                        "name": record[0],
                        "type": record[1],
                        "description": record[2]
                    })
        except Exception as e:
            if websocket:
                await websocket.send_text(json.dumps({
                    "type": "error",
                    "message": f"Groups search error: {str(e)}"
                }))
            print(f"Groups search error: {str(e)}")
        
        # Search policies
        try:
            cypher_query = "MATCH (p:Policy) WHERE toLower(p.name) CONTAINS $query OR toLower(p.description) CONTAINS $query OR toLower(p.category) CONTAINS $query RETURN p.name, p.category, p.severity, p.description LIMIT 5"
            result = await execute_search_query_with_params("policies", cypher_query, {"query": query_lower})
            if result and result.result_set:
                for record in result.result_set:
                    search_results["policies"].append({
                        "name": record[0],
                        "category": record[1],
                        "severity": record[2],
                        "description": record[3]
                    })
        except Exception as e:
            if websocket:
                await websocket.send_text(json.dumps({
                    "type": "error",
                    "message": f"Policies search error: {str(e)}"
                }))
            print(f"Policies search error: {str(e)}")
        
        # Search messages
        try:
            cypher_query = "MATCH (m:Message) WHERE toLower(m.original) CONTAINS $query RETURN m.original, m.pig_latin ORDER BY m.timestamp DESC LIMIT 5"
            result = await execute_search_query_with_params("messages", cypher_query, {"query": query_lower})
            if result and result.result_set:
                for record in result.result_set:
                    search_results["messages"].append({
                        "original": record[0],
                        "pig_latin": record[1]
                    })
        except Exception as e:
            if websocket:
                await websocket.send_text(json.dumps({
                    "type": "error",
                    "message": f"Messages search error: {str(e)}"
                }))
            print(f"Messages search error: {str(e)}")
        
        total_results = sum(len(results) for results in search_results.values())
        return search_results
    except Exception as e:
        if websocket:
            await websocket.send_text(json.dumps({
                "type": "info",
                "message": "⚠️ Search temporarily unavailable"
            }))
        return {
            "people": [],
            "teams": [],
            "groups": [],
            "policies": [],
            "messages": []
        }

def log_query_results(cypher_query, result, websocket=None):
    """Log query results in a formatted table similar to how the query is displayed"""
    try:
        if not result.result_set:
            table_output = "**Query Results:** No results returned"
        else:
            # Get column headers
            columns = [col[1] for col in result.header] if result.header else []
            if not columns:
                # Fallback for queries without headers
                columns = [f"col_{i}" for i in range(len(result.result_set[0]))]
            
            # Calculate column widths
            col_widths = [len(col) for col in columns]
            for row in result.result_set:
                for i, cell in enumerate(row):
                    if i < len(col_widths):
                        cell_str = str(cell) if cell is not None else "NULL"
                        col_widths[i] = max(col_widths[i], len(cell_str))
            
            # Limit column width for readability
            max_width = 50
            col_widths = [min(w, max_width) for w in col_widths]
            
            # Build table
            lines = []
            
            # Header row
            header_row = "| " + " | ".join(col.ljust(col_widths[i]) for i, col in enumerate(columns)) + " |"
            lines.append(header_row)
            
            # Separator row
            separator = "|" + "|".join("-" * (w + 2) for w in col_widths) + "|"
            lines.append(separator)
            
            # Data rows
            for row in result.result_set:
                row_cells = []
                for i, cell in enumerate(row):
                    if i < len(col_widths):
                        cell_str = str(cell) if cell is not None else "NULL"
                        # Truncate if too long
                        if len(cell_str) > max_width:
                            cell_str = cell_str[:max_width-3] + "..."
                        row_cells.append(cell_str.ljust(col_widths[i]))
                data_row = "| " + " | ".join(row_cells) + " |"
                lines.append(data_row)
            
            table_output = f"**Query Results:** ({len(result.result_set)} rows)\n\n```\n" + "\n".join(lines) + "\n```"
        
        # Log to console
        print(f"\n=== QUERY RESULTS ===")
        print(f"Query: {cypher_query}")
        print(table_output.replace("**Query Results:**", "Results:").replace("```", ""))
        print("=" * 50)
        
        # Send to websocket if available
        if websocket:
            import asyncio
            import json
            # Schedule sending the table output
            asyncio.create_task(websocket.send_text(json.dumps({
                "type": "results",
                "message": table_output
            })))
            
    except Exception as e:
        error_msg = f"Error formatting query results: {str(e)}"
        print(error_msg)
        if websocket:
            import asyncio
            import json
            asyncio.create_task(websocket.send_text(json.dumps({
                "type": "error", 
                "message": error_msg
            })))

def analyze_query_reasoning(user_message):
    """Analyze user message to determine query reasoning and applicable policies"""
    message_lower = user_message.lower()
    
    # Policy discovery patterns
    policy_keywords = {
        'security': 'Security Policy Framework',
        'data protection': 'Data Privacy Policy',
        'privacy': 'Data Privacy Policy', 
        'compliance': 'Compliance Management Policy',
        'access': 'Identity & Access Management Policy',
        'encryption': 'Data Encryption Policy',
        'incident': 'Security Incident Response Policy',
        'code review': 'Code Review Policy',
        'change management': 'Change Management Policy',
        'third party': 'Third Party Risk Management Policy'
    }
    
    # Reasoning patterns
    reasoning_patterns = {
        'who owns': 'Finding policy ownership and responsible parties',
        'who manages': 'Identifying management hierarchy and reporting structure', 
        'who leads': 'Locating team leads and organizational leadership',
        'who is responsible': 'Determining accountability chains and ownership',
        'approval': 'Mapping approval workflows and stakeholder chains',
        'implement': 'Identifying key contacts for implementation support',
        'team': 'Analyzing team structure and membership',
        'policy': 'Applying policy discovery and ownership patterns',
        'department': 'Using departmental organizational analysis',
        'manager': 'Leveraging management hierarchy patterns',
        'compliance': 'Applying compliance and regulatory frameworks'
    }
    
    # Find applicable policy
    applicable_policy = None
    for keyword, policy in policy_keywords.items():
        if keyword in message_lower:
            applicable_policy = policy
            break
    
    # Find reasoning pattern
    reasoning = "Query pattern matching and organizational analysis"
    for pattern, description in reasoning_patterns.items():
        if pattern in message_lower:
            reasoning = description
            break
    
    return reasoning, applicable_policy

async def execute_custom_query(user_message, websocket=None):
    """Generate and execute a custom Cypher query based on user request"""
    try:
        if websocket:
            reasoning, policy = analyze_query_reasoning(user_message)
            
            message = f"🔍 Crafting database query using {reasoning}"
            if policy:
                message += f" (citing {policy})"
            message += "..."
            
            await websocket.send_text(json.dumps({
                "type": "info",
                "message": message
            }))
        
        # Get AI model to generate the Cypher query
        prompt = load_prompt("generate_query", user_message=user_message)
        cypher_query = await call_ai_model(prompt, websocket)
        
        # Clean up the query (remove any extra text)
        cypher_query = cypher_query.strip()
        if "```" in cypher_query:
            # Extract query from code blocks
            start = cypher_query.find("```")
            if start >= 0:
                start = cypher_query.find("\n", start) + 1
                end = cypher_query.find("```", start)
                if end > start:
                    cypher_query = cypher_query[start:end].strip()
        
        if websocket:
            await websocket.send_text(json.dumps({
                "type": "query", 
                "message": f"**Database Query:** `{cypher_query}`"
            }))
        
        # Execute the query
        
        def execute_query():
            falkor = get_falkor_client()
            db = falkor.select_graph("agent_poc")
            return db.query(cypher_query)
        
        try:
            result = await asyncio.wait_for(
                asyncio.get_event_loop().run_in_executor(None, execute_query),
                timeout=15
            )
        except asyncio.TimeoutError:
            error_msg = f"Database query timeout after 15 seconds: {cypher_query}"
            if websocket:
                await websocket.send_text(json.dumps({
                    "type": "error",
                    "message": error_msg
                }))
            raise Exception(error_msg)
        except Exception as e:
            error_msg = f"Database query error: {str(e)} - Query: {cypher_query}"
            if websocket:
                await websocket.send_text(json.dumps({
                    "type": "error",
                    "message": error_msg
                }))
            raise Exception(error_msg)
        
        # Format results
        results = []
        if result.result_set:
            columns = [col[1] for col in result.header] if result.header else []
            for row in result.result_set:
                if len(columns) > 0:
                    row_data = dict(zip(columns, row))
                else:
                    row_data = {"result": row[0] if len(row) == 1 else row}
                results.append(row_data)
        
        # Log results in tabular form
        log_query_results(cypher_query, result, websocket)
        
        return {
            "query": cypher_query,
            "results": results,
            "count": len(results)
        }
        
    except Exception as e:
        # Error already sent to websocket in inner exception handlers
        # Re-raise to stop further processing
        raise e

async def execute_tools(tools, user_message, websocket):
    """Execute the specified tools based on Claude's recommendations"""
    results = {}
    
    for tool in tools:
        # Tool execution details not needed for user
        
        if tool == "search_database":
            search_results = await search_database(user_message, websocket)
            results["search_results"] = search_results
            
        elif tool == "custom_query":
            try:
                custom_results = await execute_custom_query(user_message, websocket)
                results["custom_results"] = custom_results
            except Exception as e:
                # Error already sent to websocket, re-raise to stop processing
                raise e
            
        elif tool == "pig_latin" or tool == "convert_pig_latin":
            pig_latin = to_pig_latin(user_message)
            results["pig_latin"] = pig_latin
            
        elif tool == "store_message":
            try:
                
                def store_message_in_db():
                    falkor = get_falkor_client()
                    db = falkor.select_graph("agent_poc")
                    pig_latin = results.get("pig_latin", to_pig_latin(user_message))
                    
                    # Create message node with timestamp
                    from datetime import datetime
                    timestamp = datetime.now().isoformat()
                    
                    # Use parameterized query to avoid escaping issues
                    cypher_query = "CREATE (m:Message {original: $original, pig_latin: $pig_latin, timestamp: $timestamp})"
                    params = {
                        "original": user_message,
                        "pig_latin": pig_latin,
                        "timestamp": timestamp
                    }
                    return db.query(cypher_query, params)
                
                await asyncio.wait_for(
                    asyncio.get_event_loop().run_in_executor(None, store_message_in_db),
                    timeout=10
                )
                
                results["stored"] = True
                # Message storage confirmation not needed for user
            except Exception as e:
                results["stored"] = False
                if websocket:
                    await websocket.send_text(json.dumps({
                        "type": "error",
                        "message": f"Message storage error: {str(e)}"
                    }))
                print(f"Message storage error: {str(e)}")
    
    return results

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    
    try:
        while True:
            data = await websocket.receive_text()
            
            # Message received, begin processing
            
            try:
                
                # Wrap the entire processing pipeline in a timeout
                async def process_message():
                    # Get database context with timeout
                    db_context = await asyncio.wait_for(get_database_context(), timeout=20)
                    
                    # Load and call AI model to analyze the message
                    prompt = load_prompt("analyze_message", user_message=data, database_context=db_context)
                    ai_response = await call_ai_model(prompt, websocket)
                    return ai_response
                
                # Apply timeout to the entire processing pipeline
                ai_response = await asyncio.wait_for(process_message(), timeout=60)
                
                # Parse AI model's response
                try:
                    # Try to extract JSON from AI model's response
                    # AI model might wrap JSON in markdown code blocks or add extra text
                    response_text = ai_response.strip()
                    
                    # Remove common prefixes
                    prefixes_to_remove = [
                        "Here's the JSON response:",
                        "Here is the JSON:",
                        "Response:",
                        "JSON:",
                    ]
                    for prefix in prefixes_to_remove:
                        if response_text.startswith(prefix):
                            response_text = response_text[len(prefix):].strip()
                    
                    # Look for JSON in markdown code blocks
                    if "```json" in response_text:
                        start = response_text.find("```json") + 7
                        end = response_text.find("```", start)
                        if end > start:
                            response_text = response_text[start:end].strip()
                    elif "```" in response_text:
                        start = response_text.find("```") + 3
                        end = response_text.find("```", start)
                        if end > start:
                            response_text = response_text[start:end].strip()
                    
                    # Try to find JSON within the response
                    if not response_text.startswith("{"):
                        # Look for the first { and last }
                        start = response_text.find("{")
                        end = response_text.rfind("}") + 1
                        if start >= 0 and end > start:
                            response_text = response_text[start:end]
                    
                    # Clean up any trailing text after the JSON
                    if response_text.endswith("}") and response_text.count("}") > response_text.count("{"):
                        # Find the last complete JSON object
                        brace_count = 0
                        last_valid_pos = -1
                        for i, char in enumerate(response_text):
                            if char == "{":
                                brace_count += 1
                            elif char == "}":
                                brace_count -= 1
                                if brace_count == 0:
                                    last_valid_pos = i + 1
                                    break
                        if last_valid_pos > 0:
                            response_text = response_text[:last_valid_pos]
                    
                    analysis = json.loads(response_text)
                    tools_to_execute = analysis.get("tools", [])
                    response_type = analysis.get("response_type", "pig_latin")
                    reasoning = analysis.get("reasoning", "No reasoning provided")
                    
                    # Claude analysis details not needed for user
                    
                except (json.JSONDecodeError, ValueError) as e:
                    # Log the actual response for debugging and try to extract JSON more aggressively
                    # Trying alternative JSON extraction
                    
                    # Try more aggressive JSON extraction
                    try:
                        import re
                        # Look for JSON pattern with regex
                        json_pattern = r'\{[^{}]*(?:"reasoning"[^{}]*"tools"[^{}]*"response_type"[^{}]*)\}'
                        match = re.search(json_pattern, ai_response, re.DOTALL)
                        if match:
                            json_text = match.group(0)
                            analysis = json.loads(json_text)
                            tools_to_execute = analysis.get("tools", [])
                            response_type = analysis.get("response_type", "pig_latin")
                            reasoning = analysis.get("reasoning", "Extracted from response")
                            
                            # JSON extraction successful
                        else:
                            raise ValueError("No JSON pattern found")
                            
                    except Exception as fallback_error:
                        # Final fallback - log the full response and use defaults
                        # Falling back to default pig latin behavior
                        tools_to_execute = ["pig_latin", "store_message"]
                        response_type = "pig_latin"
                
                # Execute the tools Claude recommended
                try:
                    results = await execute_tools(tools_to_execute, data, websocket)
                except Exception as tool_error:
                    # Tool execution failed (e.g., query error), error already sent
                    # Don't send any additional response
                    continue
                
                # Prepare final response based on response type
                final_response = ""
                if response_type == "pig_latin" and "pig_latin" in results:
                    # Format pig latin response in markdown
                    final_response = f"**Pig Latin Translation:**\n\n{results['pig_latin']}"
                elif response_type == "search" and "search_results" in results:
                    # Use AI model to format search results
                    # Formatting search results
                    format_prompt = load_prompt("format_results", 
                                              user_message=data, 
                                              results=results["search_results"])
                    final_response = await call_ai_model(format_prompt, websocket)
                elif response_type == "custom" and "custom_results" in results:
                    # Use AI model to format custom query results
                    custom_data = results["custom_results"]
                    if custom_data.get("error"):
                        final_response = f"Query error: {custom_data['error']}"
                    elif custom_data.get("results") or custom_data.get("count") == 0:
                        # Formatting results
                        # Include query context for better formatting
                        result_context = {
                            "query": custom_data.get("query", ""),
                            "count": custom_data.get("count", 0),
                            "results": custom_data.get("results", [])
                        }
                        format_prompt = load_prompt("format_results", 
                                                  user_message=data, 
                                                  results=result_context)
                        final_response = await call_ai_model(format_prompt, websocket)
                    else:
                        final_response = "An error occurred while executing the query."
                else:
                    # Check if we have any database results to format
                    has_db_results = (
                        ("search_results" in results and any(results["search_results"].values())) or
                        ("custom_results" in results and results["custom_results"].get("results"))
                    )
                    
                    if has_db_results:
                        # Format any database results we have
                        # Formatting results
                        
                        # Combine all available results
                        all_results = {}
                        if "search_results" in results:
                            all_results.update(results["search_results"])
                        if "custom_results" in results:
                            all_results["custom_query"] = results["custom_results"]
                        
                        format_prompt = load_prompt("format_results", 
                                                  user_message=data, 
                                                  results=all_results)
                        final_response = await call_ai_model(format_prompt, websocket)
                    else:
                        # Default to pig latin if no database results
                        pig_latin_text = to_pig_latin(data)
                        final_response = f"**Pig Latin Translation:**\n\n{pig_latin_text}"
                
                # Send final response
                await websocket.send_text(final_response)
                
            except asyncio.TimeoutError:
                await websocket.send_text(json.dumps({
                    "type": "error",
                    "message": "⏱️ AI processing is taking longer than usual. Please try a simpler query or try again in a moment."
                }))
                
                # Fallback to pig latin on timeout
                pig_latin_response = to_pig_latin(data)
                final_response = f"**Pig Latin Translation (timeout fallback):**\n\n{pig_latin_response}"
                await websocket.send_text(final_response)
                
            except Exception as e:
                error_msg = str(e)
                print(f"Websocket error: {error_msg}")
                import traceback
                traceback.print_exc()
                
                # Send user-friendly error message
                if "🚦" in error_msg or "🌐" in error_msg or "⏳" in error_msg or "🔑" in error_msg or "💳" in error_msg:
                    # This is already a user-friendly error message
                    await websocket.send_text(json.dumps({
                        "type": "error",
                        "message": error_msg
                    }))
                else:
                    # Generic error - provide fallback message
                    await websocket.send_text(json.dumps({
                        "type": "error",
                        "message": "💥 Something went wrong. Please try again."
                    }))
                
                # Fallback to original pig latin behavior
                pig_latin_response = to_pig_latin(data)
                final_response = f"**Pig Latin Translation (error fallback):**\n\n{pig_latin_response}"
                await websocket.send_text(final_response)
            
    except WebSocketDisconnect:
        print("Client disconnected")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)