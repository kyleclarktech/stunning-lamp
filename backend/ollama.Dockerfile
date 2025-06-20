FROM ollama/ollama:latest

RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*

# Copy the Modelfile for creating custom model
COPY Modelfile /app/Modelfile
