"""
OpenTelemetry Tracing

This module sets up distributed tracing using OpenTelemetry.
Tracing helps track requests as they flow through the system.
"""

from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.sdk.resources import Resource
from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from opentelemetry.instrumentation.requests import RequestsInstrumentor
from app.core.config import settings
import logging

logger = logging.getLogger(__name__)


def setup_tracing(app=None):
    """
    Set up OpenTelemetry tracing.
    
    This function initializes tracing and instruments FastAPI and requests.
    If OTLP endpoint is not configured, tracing is set up but traces won't be exported.
    
    Args:
        app: FastAPI application instance (optional, for instrumentation)
    """
    if not settings.otel_enabled:
        logger.info("OpenTelemetry tracing is disabled")
        return
    
    try:
        # Create resource with service information
        resource = Resource.create({
            "service.name": settings.otel_service_name,
            "service.version": settings.service_version,
            "service.namespace": settings.environment,
        })
        
        # Create tracer provider
        tracer_provider = TracerProvider(resource=resource)
        trace.set_tracer_provider(tracer_provider)
        
        # Set up OTLP exporter if endpoint is configured
        if settings.otel_exporter_otlp_endpoint:
            otlp_exporter = OTLPSpanExporter(
                endpoint=settings.otel_exporter_otlp_endpoint,
            )
            span_processor = BatchSpanProcessor(otlp_exporter)
            tracer_provider.add_span_processor(span_processor)
            logger.info(f"OpenTelemetry tracing enabled with OTLP endpoint: {settings.otel_exporter_otlp_endpoint}")
        else:
            logger.info("OpenTelemetry tracing enabled (no OTLP endpoint configured - traces not exported)")
        
        # Instrument FastAPI if app is provided
        if app:
            FastAPIInstrumentor.instrument_app(app)
            logger.info("FastAPI instrumentation enabled")
        
        # Instrument requests library
        RequestsInstrumentor().instrument()
        logger.info("Requests library instrumentation enabled")
        
    except Exception as e:
        logger.warning(f"Failed to set up OpenTelemetry tracing: {e}. Tracing disabled.")


def get_tracer(name: str = None):
    """
    Get a tracer instance for creating spans.
    
    Args:
        name: Name of the tracer (usually module name)
        
    Returns:
        Tracer instance
    """
    if not settings.otel_enabled:
        # Return a no-op tracer if tracing is disabled
        return trace.NoOpTracer()
    
    return trace.get_tracer(name or __name__)

