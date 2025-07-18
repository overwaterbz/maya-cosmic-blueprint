#!/usr/bin/env python3
"""
Cosmic Cache System - Phase 2 Scale Optimization
Implements efficient caching for cosmic elements and personalization templates
"""

import json
import hashlib
import time
from datetime import datetime, timedelta
from typing import Dict, Any, Optional, List
import redis
import os
from dataclasses import dataclass
from functools import wraps

@dataclass
class CacheEntry:
    """Represents a cached cosmic element entry"""
    key: str
    value: Any
    timestamp: float
    ttl: int
    user_id: str
    element_type: str

class CosmicCacheSystem:
    """Advanced caching system for cosmic elements and personalization"""
    
    def __init__(self):
        # Initialize Redis connection with fallback to in-memory cache
        self.redis_client = self._init_redis()
        self.memory_cache = {}  # Fallback for local development
        self.cache_stats = {
            'hits': 0,
            'misses': 0,
            'sets': 0,
            'invalidations': 0
        }
        
        # Cache TTL settings (in seconds)
        self.ttl_settings = {
            'cosmic_elements': 3600,  # 1 hour
            'personalized_explanations': 1800,  # 30 minutes
            'user_profiles': 900,  # 15 minutes
            'maya_calculations': 86400,  # 24 hours (birth data doesn't change)
            'ai_responses': 600,  # 10 minutes
            'templates': 7200,  # 2 hours
        }
    
    def _init_redis(self) -> Optional[redis.Redis]:
        """Initialize Redis connection with error handling"""
        try:
            redis_url = os.environ.get('REDIS_URL')
            if redis_url:
                return redis.from_url(redis_url, decode_responses=True)
            else:
                # Local Redis instance
                return redis.Redis(host='localhost', port=6379, decode_responses=True, db=0)
        except Exception as e:
            print(f"Redis connection failed, using memory cache: {e}")
            return None
    
    def _generate_cache_key(self, prefix: str, user_id: str, element_type: str, 
                          additional_params: Dict = None) -> str:
        """Generate consistent cache key"""
        key_parts = [prefix, user_id, element_type]
        
        if additional_params:
            # Sort for consistent key generation
            sorted_params = sorted(additional_params.items())
            param_str = "_".join([f"{k}:{v}" for k, v in sorted_params])
            key_parts.append(param_str)
        
        return ":".join(key_parts)
    
    def _get_from_cache(self, key: str) -> Optional[Any]:
        """Get value from cache with fallback"""
        try:
            if self.redis_client:
                value = self.redis_client.get(key)
                if value:
                    self.cache_stats['hits'] += 1
                    return json.loads(value)
            else:
                # Memory cache fallback
                if key in self.memory_cache:
                    entry = self.memory_cache[key]
                    if time.time() - entry['timestamp'] < entry['ttl']:
                        self.cache_stats['hits'] += 1
                        return entry['value']
                    else:
                        del self.memory_cache[key]
            
            self.cache_stats['misses'] += 1
            return None
        except Exception as e:
            print(f"Cache get error: {e}")
            self.cache_stats['misses'] += 1
            return None
    
    def _set_to_cache(self, key: str, value: Any, ttl: int):
        """Set value to cache with fallback"""
        try:
            if self.redis_client:
                self.redis_client.setex(key, ttl, json.dumps(value))
            else:
                # Memory cache fallback
                self.memory_cache[key] = {
                    'value': value,
                    'timestamp': time.time(),
                    'ttl': ttl
                }
            
            self.cache_stats['sets'] += 1
        except Exception as e:
            print(f"Cache set error: {e}")
    
    def get_cosmic_element(self, user_id: str, element_type: str, 
                          calculation_params: Dict = None) -> Optional[Dict]:
        """Get cached cosmic element calculation"""
        key = self._generate_cache_key("cosmic_element", user_id, element_type, calculation_params)
        return self._get_from_cache(key)
    
    def cache_cosmic_element(self, user_id: str, element_type: str, 
                           element_data: Dict, calculation_params: Dict = None):
        """Cache cosmic element calculation"""
        key = self._generate_cache_key("cosmic_element", user_id, element_type, calculation_params)
        ttl = self.ttl_settings.get('cosmic_elements', 3600)
        
        # Add metadata to cached entry
        cache_entry = {
            'data': element_data,
            'cached_at': datetime.now().isoformat(),
            'user_id': user_id,
            'element_type': element_type,
            'calculation_params': calculation_params or {}
        }
        
        self._set_to_cache(key, cache_entry, ttl)
    
    def get_personalized_explanation(self, user_id: str, element_type: str, 
                                   element_value: str) -> Optional[str]:
        """Get cached personalized explanation"""
        params = {'element_value': element_value}
        key = self._generate_cache_key("explanation", user_id, element_type, params)
        cached = self._get_from_cache(key)
        return cached.get('explanation') if cached else None
    
    def cache_personalized_explanation(self, user_id: str, element_type: str, 
                                     element_value: str, explanation: str):
        """Cache personalized explanation"""
        params = {'element_value': element_value}
        key = self._generate_cache_key("explanation", user_id, element_type, params)
        ttl = self.ttl_settings.get('personalized_explanations', 1800)
        
        cache_entry = {
            'explanation': explanation,
            'cached_at': datetime.now().isoformat(),
            'user_id': user_id,
            'element_type': element_type,
            'element_value': element_value
        }
        
        self._set_to_cache(key, cache_entry, ttl)
    
    def get_user_profile(self, user_id: str) -> Optional[Dict]:
        """Get cached user profile"""
        key = self._generate_cache_key("profile", user_id, "full")
        return self._get_from_cache(key)
    
    def cache_user_profile(self, user_id: str, profile_data: Dict):
        """Cache user profile"""
        key = self._generate_cache_key("profile", user_id, "full")
        ttl = self.ttl_settings.get('user_profiles', 900)
        
        cache_entry = {
            'profile': profile_data,
            'cached_at': datetime.now().isoformat(),
            'user_id': user_id
        }
        
        self._set_to_cache(key, cache_entry, ttl)
    
    def get_maya_calculation(self, birth_date: str, birth_time: str = None, 
                           birth_location: str = None) -> Optional[Dict]:
        """Get cached Maya calculation"""
        params = {
            'birth_date': birth_date,
            'birth_time': birth_time or "12:00",
            'birth_location': birth_location or "Unknown"
        }
        key = self._generate_cache_key("maya_calc", "global", "calculation", params)
        return self._get_from_cache(key)
    
    def cache_maya_calculation(self, birth_date: str, calculation_result: Dict, 
                             birth_time: str = None, birth_location: str = None):
        """Cache Maya calculation (long TTL since birth data doesn't change)"""
        params = {
            'birth_date': birth_date,
            'birth_time': birth_time or "12:00",
            'birth_location': birth_location or "Unknown"
        }
        key = self._generate_cache_key("maya_calc", "global", "calculation", params)
        ttl = self.ttl_settings.get('maya_calculations', 86400)
        
        cache_entry = {
            'calculation': calculation_result,
            'cached_at': datetime.now().isoformat(),
            'birth_params': params
        }
        
        self._set_to_cache(key, cache_entry, ttl)
    
    def invalidate_user_cache(self, user_id: str):
        """Invalidate all cache entries for a user"""
        if self.redis_client:
            # Use Redis pattern matching to find all user keys
            pattern = f"*:{user_id}:*"
            keys = self.redis_client.keys(pattern)
            if keys:
                self.redis_client.delete(*keys)
                self.cache_stats['invalidations'] += len(keys)
        else:
            # Memory cache invalidation
            keys_to_delete = [k for k in self.memory_cache.keys() if f":{user_id}:" in k]
            for key in keys_to_delete:
                del self.memory_cache[key]
            self.cache_stats['invalidations'] += len(keys_to_delete)
    
    def get_cache_stats(self) -> Dict:
        """Get cache performance statistics"""
        total_requests = self.cache_stats['hits'] + self.cache_stats['misses']
        hit_rate = (self.cache_stats['hits'] / total_requests * 100) if total_requests > 0 else 0
        
        return {
            'hits': self.cache_stats['hits'],
            'misses': self.cache_stats['misses'],
            'sets': self.cache_stats['sets'],
            'invalidations': self.cache_stats['invalidations'],
            'hit_rate': f"{hit_rate:.1f}%",
            'total_requests': total_requests,
            'cache_backend': 'Redis' if self.redis_client else 'Memory'
        }
    
    def cleanup_expired_cache(self):
        """Clean up expired cache entries (for memory cache)"""
        if not self.redis_client:
            current_time = time.time()
            expired_keys = []
            
            for key, entry in self.memory_cache.items():
                if current_time - entry['timestamp'] >= entry['ttl']:
                    expired_keys.append(key)
            
            for key in expired_keys:
                del self.memory_cache[key]
            
            return len(expired_keys)
        return 0

# Cache decorator for automatic caching
def cache_cosmic_result(cache_type: str, ttl: int = 3600):
    """Decorator for automatic caching of cosmic calculations"""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            # Generate cache key based on function arguments
            cache_key = f"{func.__name__}:{hashlib.md5(str(args + tuple(kwargs.items())).encode()).hexdigest()}"
            
            # Try to get from cache first
            cached_result = cosmic_cache._get_from_cache(cache_key)
            if cached_result:
                return cached_result.get('result')
            
            # Execute function and cache result
            result = func(*args, **kwargs)
            if result:
                cosmic_cache._set_to_cache(cache_key, {'result': result}, ttl)
            
            return result
        return wrapper
    return decorator

# Global cache instance
cosmic_cache = CosmicCacheSystem()

# Example usage functions
@cache_cosmic_result('maya_calculation', 86400)
def cached_maya_calculation(birth_date: str, birth_time: str = "12:00", birth_location: str = "Unknown"):
    """Example cached Maya calculation function"""
    from enhanced_maya_calculator import calculate_enhanced_maya_blueprint
    return calculate_enhanced_maya_blueprint(birth_date, birth_time, birth_location)

@cache_cosmic_result('personalized_content', 1800)
def cached_personalized_content(user_id: str, element_type: str, element_value: str):
    """Example cached personalized content function"""
    from personalized_content_engine import generate_personalized_content
    return generate_personalized_content(user_id, element_type, element_value)

if __name__ == "__main__":
    # Test cache system
    print("Testing Cosmic Cache System...")
    
    # Test basic caching
    cosmic_cache.cache_cosmic_element("test_user", "day_sign", {"name": "Ahau", "element": "Fire"})
    result = cosmic_cache.get_cosmic_element("test_user", "day_sign")
    print(f"Cache test result: {result}")
    
    # Test cache stats
    stats = cosmic_cache.get_cache_stats()
    print(f"Cache stats: {stats}")
    
    print("Cache system ready for production!")