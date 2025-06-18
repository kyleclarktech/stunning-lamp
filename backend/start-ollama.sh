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

# Pull the model
echo "Pulling model granite3.3:8b..."
ollama pull granite3.3:8b

echo "Model pulled."

# Bring the server process to the foreground
wait $pid
