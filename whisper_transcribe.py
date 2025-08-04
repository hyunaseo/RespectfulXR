import whisper
import sys
import json
import os

# Check if video file path is provided
if len(sys.argv) < 2:
    print("Usage: python transcribe_video_with_whisper.py <video_file_path>")
    sys.exit(1)

# Get video file path from command-line argument
video_path = sys.argv[1]

# Extract base filename without path and extension
video_name = os.path.splitext(os.path.basename(video_path))[0]

# Create output directory if not exists
os.makedirs("transcripts", exist_ok=True)

# Define output file paths
txt_path = f"transcripts/{video_name}_transcript.txt"
json_path = f"transcripts/{video_name}_transcript.json"

print(f"Video file found: {video_path}")

# Load the Whisper model
model = whisper.load_model("base")  # Options: tiny, base, small, medium, large
print("Model loaded.")

# Transcribe speech from the video file
print("\n===== 1. Transcribing Steps =====\n")
print("Transcribing audio...")
result = model.transcribe(video_path)
print("Transcription completed.")

# Save full transcript text (optional)
with open(txt_path, "w", encoding="utf-8") as f:
    f.write(result["text"])

# Save segmented transcript as JSON
with open(json_path, "w", encoding="utf-8") as f:
    json.dump(result["segments"], f, ensure_ascii=False, indent=2)

print("Transcription json is saved.")