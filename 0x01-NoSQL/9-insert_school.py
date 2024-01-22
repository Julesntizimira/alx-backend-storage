#!/usr/bin/env python3
'''a Python function that inserts a new document
   in a collection based on kwargs
'''


def insert_school(mongo_collection, **kwargs):
    mongo_collection.insert_one(kwargs)
    key = list(kwargs.keys())[0]
    val = kwargs.get(key)
    return mongo_collection.find_one({key: val}).get('_id')
