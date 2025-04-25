from cachetools import TTLCache

# --- Configuration ---
CACHE_TTL = 3600  # seconds (1 hour)
_cache = TTLCache(maxsize=128, ttl=CACHE_TTL)

def get_cache():
    return _cache
