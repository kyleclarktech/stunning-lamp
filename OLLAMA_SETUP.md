# Ollama Integration

This application supports using a locally hosted Ollama model instead of Claude for AI processing. This provides a self-hosted alternative for organizations that prefer to keep AI processing local.

## Configuration

To enable Ollama, set the following environment variables:

```bash
# Enable Ollama (required)
USE_OLLAMA=true

# Ollama server configuration
OLLAMA_HOST=http://localhost:11434  # Default Ollama host
OLLAMA_MODEL=llama2                 # Model to use

# Keep Claude key for fallback (optional)
ANTHROPIC_API_KEY=your_key_here
```

## Docker Setup

### Option 1: Using Docker Compose (Recommended)

1. Uncomment the Ollama service in `docker-compose.yml`:

```yaml
ollama:
  image: ollama/ollama:latest
  ports:
    - "11434:11434"
  volumes:
    - ollama_data:/root/.ollama
  environment:
    - OLLAMA_HOST=0.0.0.0
  restart: unless-stopped
```

2. Add the volume:

```yaml
volumes:
  falkor_data:
  ollama_data:  # Uncomment this line
```

3. Set environment variables in your `.env` file:

```bash
USE_OLLAMA=true
OLLAMA_HOST=http://ollama:11434
OLLAMA_MODEL=llama2
```

4. Start the services:

```bash
docker-compose up -d
```

### Option 2: External Ollama Instance

If you have Ollama running elsewhere:

1. Set environment variables in your `.env` file:

```bash
USE_OLLAMA=true
OLLAMA_HOST=http://your-ollama-host:11434
OLLAMA_MODEL=your-preferred-model
```

2. Start the application:

```bash
docker-compose up -d api frontend falkordb
```

## Supported Models

Common models that work well with this application:

- `llama2` - Good general purpose model
- `llama2:7b` - Smaller, faster version
- `llama2:13b` - Larger, more capable version
- `mistral` - Alternative model
- `codellama` - Optimized for code understanding

## Model Management

The application will automatically:
- Check if the specified model is available
- Pull the model if it's not found locally
- Fall back to the first available model if the specified one isn't found
- Test the model connection on startup

## Performance Considerations

- **Model Size**: Larger models provide better responses but require more resources
- **Hardware**: GPU acceleration significantly improves performance
- **Memory**: Ensure sufficient RAM for the model size
- **Startup Time**: Initial model download and loading can take several minutes

## GPU Support

To enable GPU acceleration with Docker:

1. Install NVIDIA Container Toolkit
2. Uncomment the GPU configuration in `docker-compose.yml`:

```yaml
runtime: nvidia
environment:
  - NVIDIA_VISIBLE_DEVICES=all
```

## Troubleshooting

### Connection Issues

If you see `🔌 Local AI service is not available`:

1. Check if Ollama is running: `curl http://localhost:11434/api/tags`
2. Verify the `OLLAMA_HOST` environment variable
3. Check Docker logs: `docker logs agent-poc-ollama-1`

### Model Issues

If models aren't working properly:

1. List available models: `docker exec agent-poc-ollama-1 ollama list`
2. Pull a model manually: `docker exec agent-poc-ollama-1 ollama pull llama2`
3. Check model compatibility with your hardware

### Performance Issues

- Use smaller models for faster responses
- Enable GPU acceleration if available
- Increase timeout values for slower hardware
- Monitor memory usage

## Switching Back to Claude

To switch back to Claude:

1. Set `USE_OLLAMA=false` or remove the variable
2. Ensure `ANTHROPIC_API_KEY` is set
3. Restart the application

The application will automatically detect the change and use Claude instead.