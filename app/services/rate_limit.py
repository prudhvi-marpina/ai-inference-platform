"""
Rate Limiting Service

This module handles rate limiting using slowapi.
Rate limiting prevents abuse by limiting requests per time period.
"""

from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from app.core.config import settings

# Create a global limiter instance
limiter = Limiter(
    key_func=get_remote_address,  # Use client IP address to identify users
    default_limits=[f"{settings.rate_limit_per_minute}/minute"] if settings.rate_limit_enabled else []
)

# This will be used to handle rate limit errors
rate_limit_exceeded_handler = _rate_limit_exceeded_handler

