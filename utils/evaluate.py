import sys
import csv
import json
import os

if len(sys.argv) < 3:
    print("Usage: python evaluate.py <csv_path> <classified_json_path>")
    sys.exit(1)

csv_path = sys.argv[1]
json_path = sys.argv[2]

# Load JSON: build a mapping from sentence text to type
with open(json_path, "r", encoding="utf-8") as f:
    segments = json.load(f)

# Build mapping: text -> type
text_to_type = {}
for seg in segments:
    text_to_type[seg["text"].strip()] = seg["type"].strip()

# Mapping for type to numbered label
type_to_label = {
    "Greeting": "1. Greeting",
    "Overview": "2. Overview",
    "Method": "3. Method",
    "Supplementary": "4. Supplementary",
    "Explanation": "5. Explanation",
    "Description": "6. Description",
    "Conclusion": "7. Conclusion",
    "Miscellaneous": "8. Miscellaneous"
}

def map_type_to_label(type_str):
    for key, label in type_to_label.items():
        if key in type_str:
            return label
    return ""

# Read CSV and add new column
rows = []
with open(csv_path, "r", encoding="utf-8") as f:
    reader = csv.reader(f)
    header = next(reader)
    header.append("taxonomy_pred")
    for row in reader:
        sentence = row[1].strip()
        type_label = ""
        if sentence in text_to_type:
            type_label = map_type_to_label(text_to_type[sentence])
        else:
            for k in text_to_type:
                if sentence.lower() == k.lower():
                    type_label = map_type_to_label(text_to_type[k])
                    break
        row.append(type_label)
        rows.append(row)

# Overwrite the original CSV file
with open(csv_path, "w", encoding="utf-8", newline='') as f:
    writer = csv.writer(f)
    writer.writerow(header)
    writer.writerows(rows)

print(f"Taxonomy prediction column added to {csv_path}")