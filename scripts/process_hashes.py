#!/usr/bin/env python3
import json
import ppdeep
import pymongo
import re

def parse_blocksize(ssdeep_str: str) -> int:
    return int(ssdeep_str.split(":", 1)[0])

if __name__ == "__main__":
    # load the 1,000 hashes
    with open("hashes.json") as f:
        hashes = json.load(f)

    client = pymongo.MongoClient("mongodb://localhost:27017")
    db     = client["fuzzyhashdb"]
    unique = db.unique_hashes
    trash  = db.trash_hashes

    dup_count = 0
    for h in hashes:
        blk = parse_blocksize(h)
        # fetch only same‐blocksize candidates
        for doc in unique.find({"blocksize": blk}, {"hash":1}):
            if ppdeep.compare(h, doc["hash"]) > 0:
                trash.insert_one({"hash": h, "blocksize": blk})
                dup_count += 1
                break
        else:
            # no break → truly unique
            try:
                unique.insert_one({"hash": h, "blocksize": blk})
            except pymongo.errors.DuplicateKeyError:
                # already present
                dup_count += 1

    total = len(hashes)
    print(f"[+] Processed {total}: {total-dup_count} unique, {dup_count} duplicates")
