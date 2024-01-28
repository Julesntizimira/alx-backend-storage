#!/usr/bin/env python3
''' Implementing an expiring web cache and tracker
'''
import requests
from cachetools import cached, TTLCache
from functools import wraps


# Create a cache with a 10-second TTL (time to live)
cache = TTLCache(maxsize=100, ttl=10)

@cached(cache)
def get_page(url: str) -> str:
    """Fetches the HTML content of a URL with caching and counting."""
    # Increment the count for the URL
    increment_url_count(url)

    # Fetch the HTML content using requests
    response = requests.get(url)
    
    # Check if the request was successful
    if response.status_code == 200:
        return response.text
    else:
        return f"Error: {response.status_code}"

def increment_url_count(url: str) -> None:
    """Increments the count for a specific URL."""
    key = f"count:{url}"
    count = cache.get(key, 0)
    cache[key] = count + 1
