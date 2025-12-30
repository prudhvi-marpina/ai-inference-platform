# AI Inference Platform

Production-grade AI inference service with observability, rate limiting, and caching.

## Features

- FastAPI-based REST API
- Redis caching
- Rate limiting
- OpenTelemetry tracing
- Prometheus metrics
- Health checks
- Docker containerization

## Prerequisites

- Docker and Docker Compose installed
- Python 3.11+ (for local development)

## Quick Start with Docker

### 1. Build and Run with Docker Compose

```bash
# Build and start all services (app + Redis)
docker-compose up --build

# Or run in detached mode
docker-compose up -d --build
```

The application will be available at:
- API: http://localhost:8000
- API Docs: http://localhost:8000/docs
- Health Check: http://localhost:8000/health
- Metrics: http://localhost:8000/metrics

### 2. View Logs

```bash
# View all logs
docker-compose logs -f

# View only app logs
docker-compose logs -f app

# View only Redis logs
docker-compose logs -f redis
```

### 3. Stop Services

```bash
# Stop services
docker-compose down

# Stop and remove volumes (clears Redis data)
docker-compose down -v
```

## Building the Docker Image

### Build the image:

```bash
docker build -t ai-inference-platform:latest .
```

### Run the container:

```bash
# Make sure Redis is running first
docker run -p 8000:8000 \
  -e REDIS_URL=redis://host.docker.internal:6379/0 \
  ai-inference-platform:latest
```

## Local Development (Without Docker)

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Start Redis (if not using Docker):
```bash
# Using Docker for Redis only
docker run -d -p 6379:6379 redis:7-alpine
```

3. Create a `.env` file (copy from `.env.example` if available)

4. Run the application:
```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

## Environment Variables

Key environment variables (see `app/core/config.py` for full list):

- `REDIS_URL`: Redis connection string
- `ENVIRONMENT`: deployment environment (development/staging/production)
- `LOG_LEVEL`: logging level (DEBUG/INFO/WARNING/ERROR)
- `RATE_LIMIT_ENABLED`: enable/disable rate limiting
- `OTEL_ENABLED`: enable/disable OpenTelemetry tracing

## API Endpoints

- `GET /`: Root endpoint with service info
- `GET /health`: Health check endpoint
- `GET /metrics`: Prometheus metrics
- `GET /docs`: Interactive API documentation
- `GET /api/v1/*`: API v1 endpoints

## Project Structure

```
.
├── app/
│   ├── api/v1/          # API routes
│   ├── core/            # Configuration
│   ├── observability/   # Metrics and tracing
│   ├── services/        # Business logic
│   └── main.py          # Application entrypoint
├── deploy/k8s/          # Kubernetes manifests
├── Dockerfile           # Docker image definition
├── docker-compose.yml   # Docker Compose configuration
└── requirements.txt     # Python dependencies
```

## Next Steps

After setting up Docker:

1. **Test the API**: Visit http://localhost:8000/docs to test endpoints
2. **Configure Environment**: Adjust environment variables in `docker-compose.yml` or `.env`
3. **Kubernetes Deployment**: Add manifests to `deploy/k8s/` for production deployment
4. **CI/CD**: Set up build and deployment pipelines

## Troubleshooting

### Port Already in Use
If port 8000 is already in use, change it in `docker-compose.yml`:
```yaml
ports:
  - "8001:8000"  # Use port 8001 on host
```

### Redis Connection Issues
Ensure Redis is running and accessible. Check the `REDIS_URL` environment variable.

### Health Check Failing
The health check may take a few seconds on first startup. Wait for the container to fully initialize.

