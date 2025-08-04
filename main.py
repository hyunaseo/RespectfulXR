import sys
import os
import subprocess

if len(sys.argv) < 2:
    print("Usage: python main.py <video_file_path>")
    sys.exit(1)

video_path = sys.argv[1]
video_name = os.path.splitext(os.path.basename(video_path))[0]
json_path = f"transcripts/{video_name}_transcript.json"

# 1. Run whisper_transcribe.py
ret = subprocess.run(
    ["python", "whisper_transcribe.py", video_path],
    cwd=os.path.dirname(os.path.abspath(__file__))
)
if ret.returncode != 0:
    print("Whisper transcription failed.")
    sys.exit(1)

if not os.path.exists(json_path):
    print(f"Transcript JSON not found: {json_path}")
    sys.exit(1)

# 2. Run setence_classification.py
ret = subprocess.run(
    ["python", "setence_classification.py", json_path],
    cwd=os.path.dirname(os.path.abspath(__file__))
)
if ret.returncode != 0:
    print("Sentence classification failed.")
    sys.exit(1)

print("\nAll steps completed successfully.")