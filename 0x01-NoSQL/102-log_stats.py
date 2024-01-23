#!/usr/bin/env python3
''' Log stats
'''
from pymongo import MongoClient


if __name__ == "__main__":
    '''if name is main'''
    client = MongoClient('mongodb://127.0.0.1:27017')
    db = client.logs
    nginx = db.nginx
    print(f"{nginx.count_documents({})} logs")
    print("Methods:")
    methods = ["GET", "POST", "PUT", "PATCH", "DELETE"]
    for method in methods:
        count = nginx.count_documents({"method": method})
        print(f"\tmethod {method}: {count}")
    count = nginx.count_documents({"method": "GET", "path": "/status"})
    print(f"{count} status check")
    print("IPs:")
    docs = nginx.aggregate([
        {
            "$group": {
                "_id": "$ip",
                "count": {
                    "$sum": 1
                    }
                }
        },
        {
            "$sort" : {
                "count": -1
            }
        }]
        )
    for doc in docs:
        ip = doc.get('_id')
        count = doc.get('count')
        print(f"\t{ip}: {count}")
