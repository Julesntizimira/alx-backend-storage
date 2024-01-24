#!/usr/bin/env python3
""" module for the class Cache """
import redis
from uuid import uuid4
from typing import Union, Callable, Any
from functools import wraps


def count_calls(method: Callable) -> Callable:
    """Decorator to count the number of calls to a class method."""
    key = method.__qualname__

    @wraps(method)
    def wrapper(self: Any, *args: Any, **kwargs: Any) -> Any:
        """Wrapper function that increments a key in Redis for Cache.store"""
        self._redis.incr(key)
        return method(self, *args, **kwargs)

    return wrapper


def call_history(method: Callable) -> Callable:
    """Decorator to track method calls and their inputs/outputs in Redis"""
    input_key = method.__qualname__ + ":inputs"
    output_key = method.__qualname__ + ":outputs"

    @wraps(method)
    def wrapper(self: Any, *args: Any, **kwargs: Any) -> Any:
        """Wrapper that records input and output data in Redis lists."""
        input_data = str(args)
        self._redis.rpush(input_key, input_data)
        output_data = method(self, *args)
        self._redis.rpush(output_key, output_data)
        return output_data

    return wrapper


def replay(method: Callable) -> None:
    """function to display the history of calls of a particular function."""
    client = redis.Redis()

    in_key = method.__qualname__ + ":inputs"
    out_key = method.__qualname__ + ":outputs"

    in_data = client.lrange(in_key, 0, -1)
    out_data = client.lrange(out_key, 0, -1)
    zippy = list(zip(in_data, out_data))

    print("{} was called {} times:".format(method.__qualname__, len(zippy)))

    for value, r_id in zippy:
        print("{}(*{}) -> {}".format(
            method.__qualname__,
            value.decode("utf-8"),
            r_id.decode("utf-8")))


class Cache:
    """class Cache"""

    def __init__(self):
        """Initialize a Cache instance using Redis"""
        self._redis = redis.Redis()
        self._redis.flushdb()

    @count_calls
    @call_history
    def store(self, data: Union[str, bytes, int, float]) -> str:
        """Store data in the cache."""
        key = str(uuid4())
        self._redis.set(key, data)
        return key

    def get(self, key: str,
            fn: Callable = None) -> Union[str, bytes, int, float]:
        """Retrieve data from the cache using the specified key."""
        if fn:
            return fn(self._redis.get(key))
        return self._redis.get(key)

    def get_str(self, key: str) -> str:
        """Retrieve a string from the cache using the specified key."""
        return str(self._redis.get(key))

    def get_int(self, key: str) -> int:
        """Retrieve an integer from the cache using the specified key."""
        return int(self._redis.get(key))
