from cachetools import TTLCache
import time  # Import the time module

# --- Configuration ---
CACHE_TTL = 3600  # seconds (1 hour)
_cache = TTLCache(maxsize=128, ttl=CACHE_TTL)

def get_cache():
    return _cache
