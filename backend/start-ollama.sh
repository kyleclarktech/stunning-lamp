#!/bin/bash

# Exit on error
set -e

# Start Ollama server in the background
/bin/ollama serve &

# Get the process ID of the server
pid=$!

# Wait for the server to be available
echo "Waiting for Ollama server to start..."
while ! curl -s -f http://localhost:11434/ > /dev/null; do
    sleep 1
done
echo "Ollama server is up."

# Pull the base model first
echo "Pulling base granite3.3:8b model..."
ollama pull granite3.3:8b

# Create custom granite model with large context window
echo "Creating custom granite3.3:8b-largectx model with 8192 context window..."
ollama create granite3.3:8b-largectx -f /app/Modelfile

echo "Custom model created."

# Bring the server process to the foreground
wait $pid
