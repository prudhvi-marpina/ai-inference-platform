"""
Prometheus Metrics

This module defines and manages Prometheus metrics for observability.
Metrics track request counts, latency, cache performance, and errors.
"""

from prometheus_client import Counter, Histogram, Gauge
from typing import Optional
import time

# Request Metrics
request_count = Counter(
    'http_requests_total',
    'Total number of HTTP requests',
    ['method', 'endpoint', 'status_code']
)

request_duration = Histogram(
    'http_request_duration_seconds',
    'HTTP request duration in seconds',
    ['method', 'endpoint'],
    buckets=[0.001, 0.005, 0.01, 0.025, 0.05, 0.1, 0.25, 0.5, 1.0, 2.5, 5.0, 10.0]
)

# Cache Metrics
cache_hits = Counter(
    'cache_hits_total',
    'Total number of cache hits',
    ['cache_type']
)

cache_misses = Counter(
    'cache_misses_total',
    'Total number of cache misses',
    ['cache_type']
)

# Inference Metrics
inference_requests = Counter(
    'inference_requests_total',
    'Total number of inference requests',
    ['model_name', 'model_version']
)

inference_duration = Histogram(
    'inference_duration_seconds',
    'Inference processing duration in seconds',
    ['model_name'],
    buckets=[0.01, 0.05, 0.1, 0.25, 0.5, 1.0, 2.5, 5.0, 10.0]
)

inference_tokens = Histogram(
    'inference_tokens_total',
    'Total tokens used for inference',
    ['model_name'],
    buckets=[10, 50, 100, 500, 1000, 5000, 10000]
)

# Error Metrics
inference_errors = Counter(
    'inference_errors_total',
    'Total number of inference errors',
    ['error_type', 'model_name']
)

# Active Connections Gauge
active_requests = Gauge(
    'active_requests',
    'Number of currently active requests'
)


class MetricsCollector:
    """
    Helper class for collecting metrics.
    Provides convenient methods to track metrics.
    """
    
    @staticmethod
    def record_request(method: str, endpoint: str, status_code: int, duration: float):
        """
        Record HTTP request metrics.
        
        Args:
            method: HTTP method (GET, POST, etc.)
            endpoint: API endpoint path
            status_code: HTTP status code
            duration: Request duration in seconds
        """
        request_count.labels(method=method, endpoint=endpoint, status_code=status_code).inc()
        request_duration.labels(method=method, endpoint=endpoint).observe(duration)
    
    @staticmethod
    def record_cache_hit(cache_type: str = "inference"):
        """Record a cache hit."""
        cache_hits.labels(cache_type=cache_type).inc()
    
    @staticmethod
    def record_cache_miss(cache_type: str = "inference"):
        """Record a cache miss."""
        cache_misses.labels(cache_type=cache_type).inc()
    
    @staticmethod
    def record_inference(
        model_name: str,
        model_version: str,
        duration: float,
        tokens_used: int
    ):
        """
        Record inference metrics.
        
        Args:
            model_name: Name of the model used
            model_version: Version of the model
            duration: Inference duration in seconds
            tokens_used: Number of tokens used
        """
        inference_requests.labels(model_name=model_name, model_version=model_version).inc()
        inference_duration.labels(model_name=model_name).observe(duration)
        inference_tokens.labels(model_name=model_name).observe(tokens_used)
    
    @staticmethod
    def record_error(error_type: str, model_name: str = "unknown"):
        """Record an inference error."""
        inference_errors.labels(error_type=error_type, model_name=model_name).inc()
    
    @staticmethod
    def increment_active_requests():
        """Increment active requests counter."""
        active_requests.inc()
    
    @staticmethod
    def decrement_active_requests():
        """Decrement active requests counter."""
        active_requests.dec()


# Create a global metrics collector instance
metrics = MetricsCollector()

