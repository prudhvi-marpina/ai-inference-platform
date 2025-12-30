"""
API v1 Routes

This module contains all v1 API endpoints for the AI Inference Platform.
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from typing import Optional

from app.services.model import model_service
from app.services.cache import cache_service
from app.services.rate_limit import limiter
from app.core.config import settings
from app.observability.metrics import metrics
from app.observability.tracing import get_tracer
from opentelemetry import trace
from starlette.requests import Request
import time

tracer = get_tracer(__name__)

router = APIRouter()


# Request/Response Models (Pydantic)
class InferenceRequest(BaseModel):
    """Request model for inference endpoint."""
    prompt: str = Field(..., description="Input text for AI inference", min_length=1)
    max_tokens: Optional[int] = Field(default=100, description="Maximum tokens to generate", ge=1, le=1000)
    temperature: Optional[float] = Field(default=0.7, description="Sampling temperature", ge=0.0, le=2.0)


class InferenceResponse(BaseModel):
    """Response model for inference endpoint."""
    output: str = Field(..., description="Generated output from the model")
    tokens_used: int = Field(..., description="Number of tokens used")
    model_version: str = Field(..., description="Version of the model used")


class ModelInfoResponse(BaseModel):
    """Response model for model info endpoint."""
    model_name: str
    model_version: str
    status: str
    description: str


@router.post("/infer", response_model=InferenceResponse)
@limiter.limit(f"{settings.rate_limit_per_minute}/minute")
async def inference(request: Request, inference_request: InferenceRequest):
    """
    Perform AI inference on the given prompt.
    
    This endpoint accepts a text prompt and returns AI-generated output.
    Uses caching to improve performance for repeated requests.
    Rate limited to prevent abuse.
    
    Args:
        request: FastAPI Request object (needed for rate limiting)
        inference_request: InferenceRequest containing prompt and optional parameters
        
    Returns:
        InferenceResponse with generated output and metadata
    """
    start_time = time.time()
    metrics.increment_active_requests()
    
    # Create a trace span for the entire inference request
    with tracer.start_as_current_span("inference_request") as span:
        span.set_attribute("prompt.length", len(inference_request.prompt))
        span.set_attribute("max_tokens", inference_request.max_tokens or model_service.max_tokens)
        span.set_attribute("temperature", inference_request.temperature or model_service.temperature)
        
        try:
            # Check cache first
            with tracer.start_as_current_span("cache.get") as cache_span:
                cached_result = await cache_service.get(
                    prompt=inference_request.prompt,
                    max_tokens=inference_request.max_tokens,
                    temperature=inference_request.temperature
                )
                cache_span.set_attribute("cache.hit", cached_result is not None)
            
            if cached_result:
                # Cache hit - return cached result (much faster!)
                metrics.record_cache_hit("inference")
                span.set_attribute("cache.result", "hit")
                duration = time.time() - start_time
                
                # Record metrics
                metrics.record_request("POST", "/api/v1/infer", 200, duration)
                metrics.record_inference(
                    model_name=model_service.model_name,
                    model_version=cached_result.get("model_version", "unknown"),
                    duration=duration,
                    tokens_used=cached_result["tokens_used"]
                )
                
                span.set_attribute("tokens_used", cached_result["tokens_used"])
                span.set_status(trace.Status(trace.StatusCode.OK))
                
                metrics.decrement_active_requests()
                return InferenceResponse(
                    output=cached_result["output"],
                    tokens_used=cached_result["tokens_used"],
                    model_version=cached_result["model_version"]
                )
            
            # Cache miss - call model service
            metrics.record_cache_miss("inference")
            span.set_attribute("cache.result", "miss")
            inference_start = time.time()
            
            # Create span for model inference
            with tracer.start_as_current_span("model.predict") as model_span:
                model_span.set_attribute("model.name", model_service.model_name)
                model_span.set_attribute("model.version", model_service.model_version)
                
                result = await model_service.predict(
                    prompt=inference_request.prompt,
                    max_tokens=inference_request.max_tokens,
                    temperature=inference_request.temperature
                )
                
                model_span.set_attribute("tokens_used", result["tokens_used"])
            
            inference_duration = time.time() - inference_start
            
            # Cache the result for future requests
            with tracer.start_as_current_span("cache.set") as cache_set_span:
                await cache_service.set(
                    prompt=inference_request.prompt,
                    result=result,
                    max_tokens=inference_request.max_tokens,
                    temperature=inference_request.temperature
                )
        
            total_duration = time.time() - start_time
            
            # Record metrics
            metrics.record_request("POST", "/api/v1/infer", 200, total_duration)
            metrics.record_inference(
                model_name=model_service.model_name,
                model_version=result.get("model_version", "unknown"),
                duration=inference_duration,
                tokens_used=result["tokens_used"]
            )
            
            span.set_attribute("tokens_used", result["tokens_used"])
            span.set_status(trace.Status(trace.StatusCode.OK))
            
            metrics.decrement_active_requests()
            return InferenceResponse(
                output=result["output"],
                tokens_used=result["tokens_used"],
                model_version=result["model_version"]
            )
            
        except Exception as e:
            # Record error in trace
            span.set_status(trace.Status(trace.StatusCode.ERROR, str(e)))
            span.record_exception(e)
            
            # Record error metrics
            metrics.record_error(str(type(e).__name__), "unknown")
            duration = time.time() - start_time
            metrics.record_request("POST", "/api/v1/infer", 500, duration)
            metrics.decrement_active_requests()
            raise


@router.get("/model", response_model=ModelInfoResponse)
async def get_model_info(request: Request):
    """
    Get information about the current model.
    
    Returns metadata about the model being used for inference.
    Useful for clients to know which model version they're interacting with.
    
    Returns:
        ModelInfoResponse with model details
    """
    start_time = time.time()
    metrics.increment_active_requests()
    
    try:
        # Get model info from model service
        info = model_service.get_info()
        
        duration = time.time() - start_time
        metrics.record_request("GET", "/api/v1/model", 200, duration)
        metrics.decrement_active_requests()
        
        return ModelInfoResponse(
            model_name=info["model_name"],
            model_version=info["model_version"],
            status=info["status"],
            description=info["description"]
        )
    except Exception as e:
        duration = time.time() - start_time
        metrics.record_request("GET", "/api/v1/model", 500, duration)
        metrics.decrement_active_requests()
        raise
