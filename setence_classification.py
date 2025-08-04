import os
import sys
import json
from openai import OpenAI

# 1. Load API key
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# 2. Load taxonomy prompt
with open("taxonomy_prompt.txt", "r", encoding="utf-8") as f:
    base_prompt = f.read()

# 3. Load transcript file
if len(sys.argv) < 2:
    print("Usage: python setence_classification.py <transcript_json_path>")
    sys.exit(1)

json_path = sys.argv[1]
with open(json_path, "r", encoding="utf-8") as f:
    segments = json.load(f)

print("\n===== 2. Classification Steps =====\n")
print(f"Loaded {len(segments)} segments from {json_path}\n")

# 4. Classify each sentence with a taxonomy label
classified_segments = []
for i, seg in enumerate(segments):
    sentence = seg["text"]
    full_prompt = f"{base_prompt.strip()}\n\nSentence: {sentence}\nCategory:"
    
    response = client.chat.completions.create(
        # model = "gpt-4o",  # or "gpt-3.5-turbo"
        # model="gpt-3.5-turbo",
        model = "gpt-4-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant that classifies how-to video narration."},
            {"role": "user", "content": full_prompt}
        ],
        temperature=0,
    )
    
    category = response.choices[0].message.content.strip()
    seg["type"] = category  # Add new field
    classified_segments.append(seg)
    
    print(f"[{i+1}/{len(segments)}] \"{sentence}\" → {category}")

# 5. Save classified transcript
base_name = os.path.splitext(os.path.basename(json_path))[0]

if base_name.endswith("_transcript"):
    base_name = base_name[:-len("_transcript")]

output_filename = base_name + "_classified.json"
output_path = os.path.join("classified", output_filename)

with open(output_path, "w", encoding="utf-8") as f:
    json.dump(classified_segments, f, ensure_ascii=False, indent=2)

print(f"\nSaved classified transcript to {output_path}")
