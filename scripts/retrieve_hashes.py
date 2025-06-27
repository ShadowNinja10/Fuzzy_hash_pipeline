#!/usr/bin/env python3
import subprocess
import re
import json
from typing import List

def get_ssdeep_hashes(malware_set: List[str], limit: int = 500) -> List[str]:
    all_hashes = []
    for strain in malware_set:
        cmd = ["vt", "search", strain, "--limit", str(limit)]
        proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, text=True)
        out, _ = proc.communicate()
        hashes = re.findall(r'ssdeep:\s*"([^"]+)"', out)
        print(f"[+] {strain}: {len(hashes)} hashes")
        all_hashes.extend(hashes)
    return all_hashes

if __name__ == "__main__":
    strains = ["neptunerat", "sodinokibi", "ryuk", "darkside", "lockbit"]
    hashes = get_ssdeep_hashes(strains, limit=500)
    # cap at 1000
    hashes = hashes[:1000]
    with open("hashes.json", "w") as f:
        json.dump(hashes, f)
    print(f"[+] Retrieved {len(hashes)} total hashes → hashes.json")
