"""
Redis Cache Service

This module handles caching of inference responses using Redis.
Caching improves performance by storing results of previous requests.
"""

from app.core.config import settings
from typing import Optional, Dict, Any
import redis.asyncio as redis
import hashlib
import json
import logging

logger = logging.getLogger(__name__)


class CacheService:
    """
    Service for caching inference responses in Redis.
    
    Caches responses by creating a hash of the input (prompt + parameters).
    This allows us to return cached results for identical requests.
    """
    
    def __init__(self):
        """Initialize the cache service with Redis connection."""
        self.redis_url = settings.redis_url
        self.ttl = settings.redis_ttl  # Time To Live in seconds
        self.redis_client: Optional[redis.Redis] = None
        self._connected = False
    
    async def connect(self):
        """
        Establish connection to Redis.
        
        This should be called once at application startup.
        """
        import asyncio
        
        max_retries = 3
        retry_delay = 2  # seconds
        
        for attempt in range(max_retries):
            try:
                # Use simple connection parameters to avoid recursion issues
                self.redis_client = redis.from_url(
                    self.redis_url,
                    encoding="utf-8",
                    decode_responses=True,
                    socket_connect_timeout=5
                )
                # Test connection
                await self.redis_client.ping()
                self._connected = True
                logger.info(f"Connected to Redis at {self.redis_url}")
                return
            except Exception as e:
                if attempt < max_retries - 1:
                    logger.warning(f"Failed to connect to Redis (attempt {attempt + 1}/{max_retries}): {e}. Retrying in {retry_delay}s...")
                    await asyncio.sleep(retry_delay)
                else:
                    logger.warning(f"Failed to connect to Redis after {max_retries} attempts: {e}. Caching disabled.")
                    self._connected = False
    
    async def disconnect(self):
        """Close Redis connection."""
        if self.redis_client:
            await self.redis_client.close()
            self._connected = False
            logger.info("Disconnected from Redis")
    
    def _generate_cache_key(self, prompt: str, max_tokens: int = None, temperature: float = None) -> str:
        """
        Generate a unique cache key from the input parameters.
        
        Uses SHA256 hash to create a unique key for each unique input combination.
        
        Args:
            prompt: Input text
            max_tokens: Maximum tokens parameter
            temperature: Temperature parameter
            
        Returns:
            Cache key string (e.g., "inference:abc123...")
        """
        # Create a dictionary with all parameters
        cache_data = {
            "prompt": prompt,
            "max_tokens": max_tokens,
            "temperature": temperature
        }
        
        # Convert to JSON string (consistent format)
        cache_string = json.dumps(cache_data, sort_keys=True)
        
        # Generate SHA256 hash
        hash_object = hashlib.sha256(cache_string.encode())
        hash_hex = hash_object.hexdigest()
        
        # Return cache key with prefix
        return f"inference:{hash_hex}"
    
    async def get(self, prompt: str, max_tokens: int = None, temperature: float = None) -> Optional[Dict[str, Any]]:
        """
        Retrieve cached inference result.
        
        Args:
            prompt: Input text
            max_tokens: Maximum tokens parameter
            temperature: Temperature parameter
            
        Returns:
            Cached result dictionary if found, None otherwise
        """
        if not self._connected:
            return None
        
        try:
            cache_key = self._generate_cache_key(prompt, max_tokens, temperature)
            cached_value = await self.redis_client.get(cache_key)
            
            if cached_value:
                # Deserialize JSON string back to dictionary
                result = json.loads(cached_value)
                logger.info(f"Cache HIT for key: {cache_key[:20]}...")
                return result
            else:
                logger.info(f"Cache MISS for key: {cache_key[:20]}...")
                return None
                
        except Exception as e:
            logger.error(f"Error reading from cache: {e}")
            return None
    
    async def set(self, prompt: str, result: Dict[str, Any], max_tokens: int = None, temperature: float = None):
        """
        Store inference result in cache.
        
        Args:
            prompt: Input text
            result: Inference result dictionary to cache
            max_tokens: Maximum tokens parameter
            temperature: Temperature parameter
        """
        if not self._connected:
            return
        
        try:
            cache_key = self._generate_cache_key(prompt, max_tokens, temperature)
            # Serialize dictionary to JSON string
            cache_value = json.dumps(result)
            
            # Store in Redis with TTL (Time To Live)
            await self.redis_client.setex(
                cache_key,
                self.ttl,  # Expire after TTL seconds
                cache_value
            )
            logger.info(f"Cached result for key: {cache_key[:20]}... (TTL: {self.ttl}s)")
            
        except Exception as e:
            logger.error(f"Error writing to cache: {e}")


# Create a global cache service instance
cache_service = CacheService()

