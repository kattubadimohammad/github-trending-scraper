CACHE = {}

def get_cache(key):
    if key in CACHE and (time() - CACHE[key]["timestamp"]) < 600:  # Cache expiry time: 10 minutes
        return CACHE[key]["data"]
    return None

def set_cache(key, data):
    CACHE[key] = {"data": data, "timestamp": time()}
