"""
FastAPI Application Entrypoint

This is the main entry point for the AI Inference Platform.
It initializes the FastAPI app, wires routers, and sets up middleware.
"""

import logging
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from prometheus_client import generate_latest, CONTENT_TYPE_LATEST
from starlette.responses import Response

from app.api.v1 import routes as v1_routes
from app.services.cache import cache_service
from app.services.rate_limit import limiter, rate_limit_exceeded_handler
from app.observability.tracing import setup_tracing
from app.core.config import settings
from slowapi.errors import RateLimitExceeded

# Configure logging
logging.basicConfig(
    level=getattr(logging, settings.log_level.upper()),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

# Initialize FastAPI app
app = FastAPI(
    title="AI Inference Platform",
    description="Production-grade AI inference service with observability",
    version="1.0.0",
)

# Set up OpenTelemetry tracing
setup_tracing(app)

# Add rate limiter to the app
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, rate_limit_exceeded_handler)

# Include API routers
app.include_router(v1_routes.router, prefix="/api/v1", tags=["v1"])


@app.on_event("startup")
async def startup_event():
    """Initialize services on application startup."""
    # Connect to Redis
    await cache_service.connect()


@app.on_event("shutdown")
async def shutdown_event():
    """Cleanup on application shutdown."""
    # Disconnect from Redis
    await cache_service.disconnect()


@app.get("/health")
async def health_check():
    """
    Health check endpoint for Kubernetes liveness/readiness probes.
    
    Returns:
        JSON response with status "healthy"
    """
    return JSONResponse(content={"status": "healthy"})


@app.get("/metrics")
async def metrics():
    """
    Prometheus metrics endpoint.
    
    Kubernetes scrapes this endpoint to collect metrics.
    Returns metrics in Prometheus text format.
    """
    return Response(
        content=generate_latest(),
        media_type=CONTENT_TYPE_LATEST
    )


@app.get("/")
async def root():
    """Root endpoint with API information."""
    return {
        "service": "AI Inference Platform",
        "version": "1.0.0",
        "docs": "/docs"
    }

