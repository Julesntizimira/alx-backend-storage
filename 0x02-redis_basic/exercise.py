#!/usr/bin/env python3
'''Writing strings to Redis
'''
import redis
import uuid
from typing import Union, Callable, Any


class Cache:
    '''class cache
    '''
    def __init__(self):
        '''constructor
        '''
        self._redis = redis.Redis()
        self._redis.flushdb()

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
