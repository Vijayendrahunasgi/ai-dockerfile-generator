# AI Dockerfile Generator

A lightweight FastAPI service that generates Dockerfiles from code snippets using simple AI-driven language detection.

## Run locally
```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8080
```

## Build & run with Docker
```bash
docker build -t ai-dockerfile-generator .
docker run -p 8080:8080 ai-dockerfile-generator
```

## API Usage
```bash
curl -X POST http://localhost:8080/generate-dockerfile \\
    -H "Content-Type: application/json" \\
    -d '{"code": "import flask"}'
```
