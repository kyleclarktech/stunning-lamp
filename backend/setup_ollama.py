#!/usr/bin/env python3
"""
Optional setup script for Ollama integration.
This script helps set up Ollama models if USE_OLLAMA is enabled.
"""

import os
import time
import ollama
from dotenv import load_dotenv

def setup_ollama():
    """Setup Ollama model if needed"""
    load_dotenv()
    
    use_ollama = os.getenv('USE_OLLAMA', '').lower() in ('true', '1', 'yes')
    if not use_ollama:
        print("Ollama not enabled (USE_OLLAMA not set to true)")
        return
    
    host = os.getenv('OLLAMA_HOST', 'http://localhost:11434')
    model = os.getenv('OLLAMA_MODEL', 'llama2')
    
    print(f"Setting up Ollama at {host} with model {model}")
    
    try:
        client = ollama.Client(host=host)
        
        # Wait for Ollama to be ready
        max_retries = 30
        for attempt in range(max_retries):
            try:
                client.list()
                print("✅ Ollama is ready!")
                break
            except Exception as e:
                print(f"⏳ Waiting for Ollama... ({attempt + 1}/{max_retries})")
                time.sleep(2)
        else:
            print("❌ Ollama failed to become ready")
            return
        
        # Check if model exists
        models = client.list()
        available_models = [m['name'] for m in models['models']]
        
        if model not in available_models:
            print(f"📥 Pulling model {model}...")
            client.pull(model)
            print(f"✅ Model {model} ready!")
        else:
            print(f"✅ Model {model} already available")
            
        # Test the model
        print("🧪 Testing model...")
        response = client.chat(
            model=model,
            messages=[
                {"role": "user", "content": "Hello! Please respond with just 'OK' to confirm you're working."}
            ]
        )
        print(f"✅ Model test response: {response['message']['content']}")
        
    except Exception as e:
        print(f"❌ Error setting up Ollama: {e}")

if __name__ == "__main__":
    setup_ollama()