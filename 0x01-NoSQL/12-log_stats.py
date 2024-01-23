#!/usr/bin/env python3
''' Log stats
'''
from pymongo import MongoClient


client = MongoClient("localhost", 27017)
db = client.logs
nginx = db.nginx

print(f"{nginx.count_documents({})} logs")
print("Methods:")
methods = ["GET", "POST", "PUT", "PATCH", "DELETE"]
for method in methods:
    count = nginx.count_documents({"method": method})
    print(f"\tmethod {count}")
count = nginx.count_documents({"method": "GET", "path": "/status"})
print(f"{count} status check")
