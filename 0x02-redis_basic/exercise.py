#!/usr/bin/env python3
'''Writing strings to Redis
'''
import redis
import uuid
from functools import wraps
from typing import Union, Callable, Any


def call_history(method: Callable) -> Callable:
    '''decorator function
       to log history
    '''
    key = method.__qualname__
    input = key + ":inputs"
    output = key + ":outputs"

    @wraps(method)
    def wrapper_function_history(self, *args, **kwargs) -> None:
        '''wrapper function
           for call history
        '''
        self._redis.rpush(input, str(*args))
        result = method(self, *args, **kwargs)
        self._redis.rpush(output, result)
        return result
    return wrapper_function_history


def count_calls(method: Callable) -> Callable:
    '''decorator function
       to count number of calls
    '''

    @wraps(method)
    def wrapper_function(self, *args, **kwargs) -> None:
        '''wrapper method
        '''
        key = method.__qualname__
        self._redis.incr(key)
        return method(self, *args, **kwargs)
    return wrapper_function


class Cache:
    '''class cache
    '''
    def __init__(self):
        '''constructor
        '''
        self._redis = redis.Redis()
        self._redis.flushdb()

    @count_calls
    @call_history
    def store(self, data: Union[str, bytes, int, float]) -> str:
        '''takes data argument and returns a string
        '''
        key = str(uuid.uuid4())
        self._redis.set(key, data)
        return key

    def get(self, key: str, fn: Callable[[bytes], Any] = None) -> Any:
        '''convert the data back to the desired format
        '''
        data = self._redis.get(key)
        if fn:
            return fn(data)
        else:
            return data

    def get_str(self, data: bytes) -> str:
        '''convert bytes to str'''
        result = data.decode('utf-8')
        return result

    def get_int(self, data: bytes) -> int:
        '''convert bytes to int'''
        integer_value = int.from_bytes(data, byteorder='little')
        return integer_value
