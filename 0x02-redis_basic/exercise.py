#!/usr/bin/env python3
'''Writing strings to Redis
'''
import redis
import uuid


class Cache:
    '''class cache
    '''
    def __init__(self):
        '''constructor
        '''
        self._redis = redis.Redis()
        self._redis.flushdb()

    def store(self, data: any) -> str:
        '''takes data argument and returns a string
        '''
        key = str(uuid.uuid4())
        self._redis.set(key, data)
        return key
