#!/usr/bin/env python3
import pymongo



client = pymongo.MongoClient("mongodb://localhost:27017")
db     = client["fuzzyhashdb"]

# Drop existing collections (for a clean demo)
db.unique_hashes.drop()
db.trash_hashes.drop()

# Recreate with indexes
unique = db.unique_hashes
trash  = db.trash_hashes

unique.create_index([("blocksize", 1)])
unique.create_index([("hash", 1)], unique=True)
trash.create_index([("blocksize", 1)])
trash.create_index([("hash", 1)], unique=True)

print("[+] MongoDB initialized: collections `unique_hashes` & `trash_hashes` with indexes")
