# AI Inference Platform

Production-grade AI inference service with observability, rate limiting, caching, and auto-scaling capabilities.

## 🚀 Features

- **FastAPI-based REST API** - High-performance async API framework
- **Redis Caching** - Intelligent response caching (60s TTL) for faster responses
- **Rate Limiting** - Configurable per-IP rate limits (10 requests/minute default)
- **OpenTelemetry Tracing** - Distributed tracing for request monitoring
- **Prometheus Metrics** - Comprehensive metrics collection and export
- **Health Checks** - Kubernetes-ready health and readiness probes
- **Docker Containerization** - Multi-stage builds for optimized images
- **Docker Compose** - Local development and testing setup
- **Kubernetes Deployment** - Production-ready K8s manifests with auto-scaling
- **Automated Testing** - Comprehensive test suite (13 tests)
- **CI/CD Pipeline** - GitHub Actions for automated testing and builds

## 📋 Table of Contents

- [Quick Start](#quick-start)
- [Architecture](#architecture)
- [API Endpoints](#api-endpoints)
- [Docker Compose Setup](#docker-compose-setup)
- [Kubernetes Deployment](#kubernetes-deployment)
- [Local Development](#local-development)
- [Testing](#testing)
- [CI/CD](#cicd)
- [Configuration](#configuration)
- [Project Structure](#project-structure)
- [Troubleshooting](#troubleshooting)

## 🏃 Quick Start

### Option 1: Docker Compose (Recommended for Local)

```bash
# Start all services (app + Redis)
docker-compose up -d

# Check status
docker-compose ps

# View logs
docker-compose logs -f app

# Stop services
docker-compose down
```

Access the API at: http://localhost:8000

### Option 2: Kubernetes (Production)

```bash
# Build Docker image
docker build -t ai-inference-platform:latest .

# Deploy to Kubernetes
kubectl apply -f deploy/k8s/

# Check deployment
kubectl get pods
kubectl get services

# Port forward to access locally
kubectl port-forward service/ai-inference-platform 8000:80
```

## 🏗️ Architecture

```
┌─────────────────────────────────────────┐
│         FastAPI Application             │
│  ┌──────────┐  ┌──────────┐            │
│  │   API    │  │  Cache   │            │
│  │  Routes  │  │ Service  │            │
│  └────┬─────┘  └────┬─────┘            │
│       │             │                   │
│  ┌────▼─────────────▼─────┐            │
│  │  Rate Limiting         │            │
│  │  Metrics & Tracing     │            │
│  └────┬───────────────────┘            │
│       │                                 │
│  ┌────▼─────┐                           │
│  │   Redis  │  ← Caching + Rate Limiting│
│  └──────────┘                           │
└─────────────────────────────────────────┘
```

### Components

- **API Layer**: FastAPI routes handling HTTP requests
- **Model Service**: AI inference processing
- **Cache Service**: Redis-based response caching
- **Rate Limiter**: Per-IP request throttling
- **Metrics**: Prometheus metrics collection
- **Tracing**: OpenTelemetry distributed tracing

## 📡 API Endpoints

### Core Endpoints

- `GET /` - Service information
- `GET /health` - Health check (returns `{"status": "healthy"}`)
- `GET /metrics` - Prometheus metrics endpoint
- `GET /docs` - Interactive API documentation (Swagger UI)

### API v1 Endpoints

- `POST /api/v1/infer` - AI inference endpoint
  ```json
  {
    "prompt": "What is AI?",
    "max_tokens": 100,
    "temperature": 0.7
  }
  ```
  
- `GET /api/v1/model` - Get model information
  ```json
  {
    "model_name": "default-model",
    "model_version": "1.0.0",
    "status": "ready",
    "description": "..."
  }
  ```

## 🐳 Docker Compose Setup

### Start Services

```bash
# Build and start
docker-compose up -d --build

# View logs
docker-compose logs -f

# Stop services
docker-compose down

# Stop and remove volumes (clears Redis data)
docker-compose down -v
```

### Services

- **app**: FastAPI application (port 8000)
- **redis**: Redis cache (port 6379)

### Configuration

Edit `docker-compose.yml` to customize:
- Port mappings
- Environment variables
- Resource limits

## ☸️ Kubernetes Deployment

### Prerequisites

- Kubernetes cluster (local: Minikube, kind, or Docker Desktop)
- `kubectl` installed
- Docker image built and available

### Quick Deploy

```bash
# 1. Build and tag image (replace with your registry)
docker build -t your-registry/ai-inference-platform:latest .

# 2. Update deployment.yaml with your image
# Edit: deploy/k8s/deployment.yaml
# Change: image: your-registry/ai-inference-platform:latest

# 3. Deploy to Kubernetes
kubectl apply -f deploy/k8s/

# 4. Verify deployment
kubectl get pods
kubectl get services
kubectl get deployments
```

### Kubernetes Manifests

- `deployment.yaml` - Application deployment (2 replicas, resources, health checks)
- `service.yaml` - ClusterIP service for internal access
- `configmap.yaml` - Configuration values
- `hpa.yaml` - Horizontal Pod Autoscaler (auto-scales 2-10 pods)
- `ingress.yaml` - External access configuration
- `redis-deployment.yaml` - Redis deployment (optional, can use managed Redis)

### Accessing the Application

**Option 1: Port Forward (Local Testing)**
```bash
kubectl port-forward service/ai-inference-platform 8000:80
# Access at http://localhost:8000
```

**Option 2: Ingress (Production)**
- Update `ingress.yaml` with your domain
- Install Ingress Controller (e.g., NGINX)
- Access via domain name

**Option 3: LoadBalancer (Cloud)**
- Change `service.yaml` type to `LoadBalancer`
- Get external IP: `kubectl get service ai-inference-platform`

### Auto-Scaling

The HPA automatically scales based on CPU (70%) and memory (80%):
- **Min replicas**: 2
- **Max replicas**: 10
- Scales up/down automatically based on load

Check HPA status:
```bash
kubectl get hpa
```

## 💻 Local Development

### Setup

1. **Create virtual environment:**
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Start Redis (using Docker):**
   ```bash
   docker run -d -p 6379:6379 redis:7-alpine
   ```

4. **Run application:**
   ```bash
   uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
   ```

### Environment Variables

Create a `.env` file (optional):
```env
REDIS_URL=redis://localhost:6379/0
ENVIRONMENT=development
LOG_LEVEL=DEBUG
RATE_LIMIT_ENABLED=true
OTEL_ENABLED=false
```

## 🧪 Testing

### Run Tests

```bash
# Run all tests
pytest

# Run with verbose output
pytest -v

# Run specific test file
pytest app/tests/test_health.py

# Run specific test
pytest app/tests/test_health.py::test_health_endpoint
```

### Test Coverage

- **13 tests** covering:
  - Health endpoint
  - Model info endpoint
  - Inference endpoint (validation, caching)
  - Rate limiting

### Test Structure

```
app/tests/
├── conftest.py          # Shared fixtures (test client, mocks)
├── test_health.py       # Health endpoint tests
├── test_model_info.py  # Model info tests
├── test_inference.py   # Inference endpoint tests
└── test_rate_limit.py  # Rate limiting tests
```

## 🔄 CI/CD

### GitHub Actions Workflow

Automated pipeline runs on every push:
1. **Test Job**: Runs pytest tests
2. **Build Job**: Builds Docker image (only if tests pass)

### Workflow File

`.github/workflows/ci.yml`

### View CI/CD Status

1. Go to: https://github.com/prudhvi-marpina/ai-inference-platform/actions
2. Click on latest workflow run
3. View test and build results

### Manual Trigger

GitHub repo → Actions → "CI/CD Pipeline" → "Run workflow"

## ⚙️ Configuration

### Environment Variables

Key configuration options (see `app/core/config.py`):

| Variable | Default | Description |
|----------|---------|-------------|
| `REDIS_URL` | `redis://127.0.0.1:6379/0` | Redis connection string |
| `ENVIRONMENT` | `development` | Environment (dev/staging/prod) |
| `LOG_LEVEL` | `INFO` | Logging level (DEBUG/INFO/WARNING/ERROR) |
| `RATE_LIMIT_ENABLED` | `true` | Enable/disable rate limiting |
| `RATE_LIMIT_PER_MINUTE` | `10` | Requests per minute per IP |
| `OTEL_ENABLED` | `true` | Enable OpenTelemetry tracing |
| `OTEL_EXPORTER_OTLP_ENDPOINT` | `None` | OTLP exporter endpoint |

### Configuration Priority

1. Environment variables (highest priority)
2. `.env` file
3. Default values (lowest priority)

## 📁 Project Structure

```
.
├── app/
│   ├── api/
│   │   └── v1/
│   │       └── routes.py          # API endpoints
│   ├── core/
│   │   └── config.py              # Configuration management
│   ├── observability/
│   │   ├── metrics.py             # Prometheus metrics
│   │   └── tracing.py             # OpenTelemetry tracing
│   ├── services/
│   │   ├── cache.py               # Redis caching service
│   │   ├── model.py               # AI model service
│   │   └── rate_limit.py          # Rate limiting service
│   ├── tests/                     # Test suite
│   │   ├── conftest.py            # Test fixtures
│   │   ├── test_health.py
│   │   ├── test_inference.py
│   │   ├── test_model_info.py
│   │   └── test_rate_limit.py
│   └── main.py                    # Application entrypoint
├── deploy/
│   └── k8s/                       # Kubernetes manifests
│       ├── deployment.yaml
│       ├── service.yaml
│       ├── configmap.yaml
│       ├── hpa.yaml
│       ├── ingress.yaml
│       └── redis-deployment.yaml
├── .github/
│   └── workflows/
│       └── ci.yml                 # CI/CD pipeline
├── Dockerfile                     # Docker image definition
├── docker-compose.yml             # Docker Compose configuration
├── requirements.txt               # Python dependencies
├── pytest.ini                     # Pytest configuration
└── README.md                      # This file
```

## 🔍 Key Features Explained

### Caching

- **What**: Redis caches inference responses
- **TTL**: 60 seconds
- **Benefit**: Repeated requests return instantly (10-20ms vs 200ms)
- **Cache Key**: Hash of prompt + parameters

### Rate Limiting

- **What**: Limits requests per IP address
- **Default**: 10 requests per minute
- **Benefit**: Prevents abuse and DoS attacks
- **Response**: 429 Too Many Requests when exceeded

### Metrics

- **What**: Prometheus metrics for monitoring
- **Metrics**: Request count, latency, cache hits/misses, errors
- **Endpoint**: `/metrics`
- **Use**: Monitor performance, set up alerts

### Tracing

- **What**: OpenTelemetry distributed tracing
- **Benefit**: Track requests across services
- **Export**: OTLP endpoint (configurable)
- **Use**: Debug performance issues

### Auto-Scaling (Kubernetes)

- **What**: Automatically scales pods based on load
- **Min**: 2 pods (high availability)
- **Max**: 10 pods (handles traffic spikes)
- **Triggers**: CPU > 70% or Memory > 80%

## 🐛 Troubleshooting

### Port Already in Use

**Docker Compose:**
```yaml
# Change port in docker-compose.yml
ports:
  - "8001:8000"  # Use port 8001
```

**Kubernetes:**
```bash
# Use different port for port-forward
kubectl port-forward service/ai-inference-platform 8001:80
```

### Redis Connection Issues

**Docker Compose:**
- Check Redis is running: `docker-compose ps`
- Check logs: `docker-compose logs redis`
- Verify `REDIS_URL` in `docker-compose.yml`

**Kubernetes:**
- Check Redis pod: `kubectl get pods | grep redis`
- Check Redis service: `kubectl get svc ai-inference-redis`
- Verify ConfigMap: `kubectl get configmap ai-inference-config -o yaml`

### Health Check Failing

- Wait 30-60 seconds for app to fully start
- Check logs: `docker-compose logs app` or `kubectl logs <pod-name>`
- Verify app is listening on port 8000

### Tests Failing in CI

- Tests use mocked Redis (no real Redis needed)
- Check GitHub Actions logs for specific errors
- Verify all dependencies in `requirements.txt`

### Kubernetes Pods Not Starting

```bash
# Check pod status
kubectl get pods

# Describe pod for details
kubectl describe pod <pod-name>

# Check logs
kubectl logs <pod-name>

# Check events
kubectl get events --sort-by='.lastTimestamp'
```

## 📊 Performance

### Caching Impact

- **Cache Miss**: ~200ms (calls model)
- **Cache Hit**: ~10-20ms (returns cached result)
- **Speed Improvement**: ~10x faster for repeated requests

### Resource Usage

**Docker Compose:**
- App: ~200-500MB RAM
- Redis: ~50-100MB RAM

**Kubernetes:**
- App Pod: 512Mi-1Gi RAM, 200m-1000m CPU
- Redis Pod: 256Mi-512Mi RAM, 100m-500m CPU

## 🚀 Production Deployment

### Recommended Setup

1. **Use Managed Redis** (AWS ElastiCache, Google Memorystore, Azure Cache)
2. **Deploy to Kubernetes** (EKS, GKE, AKS)
3. **Set up Monitoring** (Prometheus + Grafana)
4. **Configure Ingress** with TLS/SSL
5. **Set up CI/CD** for automated deployments

### Security Considerations

- Use Kubernetes Secrets for sensitive data
- Enable TLS/SSL for ingress
- Configure network policies
- Use non-root containers (already configured)
- Set resource limits (already configured)

## 📚 Technology Stack

- **FastAPI** - Web framework
- **Uvicorn** - ASGI server
- **Redis** - Caching and rate limiting
- **Prometheus** - Metrics collection
- **OpenTelemetry** - Distributed tracing
- **Docker** - Containerization
- **Kubernetes** - Orchestration
- **Pytest** - Testing framework
- **GitHub Actions** - CI/CD

## 📝 License

This project is open source and available for educational purposes.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Run tests: `pytest`
5. Submit a pull request

## 📞 Support

For issues or questions:
- Check [Troubleshooting](#troubleshooting) section
- Review GitHub Actions logs for CI/CD issues
- Check Kubernetes logs for deployment issues

---

**Built with ❤️ for production AI inference workloads**
