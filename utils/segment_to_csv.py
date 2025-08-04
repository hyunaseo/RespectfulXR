import sys
import json
import csv
import os

if len(sys.argv) < 2:
    print("Usage: python segment_to_csv.py <transcript_json_path>")
    sys.exit(1)

json_path = sys.argv[1]
csv_path = os.path.splitext(json_path)[0] + ".csv"

with open(json_path, "r", encoding="utf-8") as f:
    segments = json.load(f)

with open(csv_path, "w", encoding="utf-8", newline='') as f:
    writer = csv.writer(f)
    writer.writerow(["id", "sentence"])
    for seg in segments:
        writer.writerow([seg.get("id", ""), seg.get("text", "")])

print(f"CSV saved to {csv_path}")