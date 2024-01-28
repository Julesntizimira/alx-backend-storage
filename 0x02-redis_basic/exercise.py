#!/usr/bin/env python3
'''Writing strings to Redis
'''
import redis
import uuid
from functools import wraps
from typing import Union, Callable, Any


def replay(method: Callable) -> None:
    ''' display the history of calls of a particular function
    '''
    r = redis.Redis()
    key = method.__qualname__
    input_key = key + ":inputs"
    output_key = key + ":outputs"
    calls = r.get(key)
    inputs = r.lrange(input_key, 0, -1)
    outputs = r.lrange(output_key, 0, -1)
    print(f"{key} was called {calls} times:")
    for i in range(len(inputs)):
        first = inputs[i].decode('utf-8')
        last = outputs[i].decode('utf-8')
        print(f"{key}(*{first}) -> {last}")


def call_history(method: Callable) -> Callable:
    """
    Counts the number of times a function is called
    Args:
        method: The function to be decorated
    Returns:
        The decorated function
    """
    key = method.__qualname__
    inputs = key + ":inputs"
    outputs = key + ":outputs"

    @wraps(method)
    def wrapper(self, *args, **kwargs):
        """
        Wrapper function for the decorated function
        Args:
            self: The object instance
            *args: The arguments passed to the function
            **kwargs: The keyword arguments passed to the function
        Returns:
            The return value of the decorated function
        """
        self._redis.rpush(inputs, str(args))
        data = method(self, *args, **kwargs)
        self._redis.rpush(outputs, str(data))
        return data

    return wrapper


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
