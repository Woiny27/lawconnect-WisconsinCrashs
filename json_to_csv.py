import json
import csv
import sys

"""
Usage:
    python json_to_csv.py findings.json findings.csv

This script converts a findings.json file (with a 'findings' array) to a CSV file.
"""

def json_to_csv(json_path, csv_path):
    with open(json_path, 'r') as jf:
        data = json.load(jf)
    findings = data.get('findings', [])
    if not findings:
        print("No findings to export.")
        return
    # Get all unique keys for CSV header
    keys = set()
    for f in findings:
        keys.update(f.keys())
    keys = list(keys)
    with open(csv_path, 'w', newline='') as cf:
        writer = csv.DictWriter(cf, fieldnames=keys)
        writer.writeheader()
        for row in findings:
            writer.writerow(row)
    print(f"Exported {len(findings)} findings to {csv_path}")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python json_to_csv.py findings.json findings.csv")
        sys.exit(1)
    json_to_csv(sys.argv[1], sys.argv[2])
