import os
import sys
import pandas as pd

# Step 1: Download YouTube Video
output_folder = input("enter video folder path: ")
# Step 2: Detect Loud Sections from Audio
from loud_sections_from_mp3 import load_audio, get_loud_sections
from speech_detection import detect_goal_speech

# 🔍 Automatically detect the MP3 file instead of assuming a fixed name
mp3_files = [f for f in os.listdir(output_folder) if f.lower().endswith(".mp3")]
if not mp3_files:
    print(f"❌ No .mp3 file found in folder: {output_folder}")
    sys.exit(1)

mp3_path = os.path.join(output_folder, mp3_files[0])
print(f"📥 Using MP3 file: {mp3_path}")

try:
    audio = load_audio(mp3_path)
    loud_intervals = get_loud_sections(audio)  # list of [start, end]

    if not loud_intervals:
        print("⚠️ No loud intervals found. Exiting.")
        sys.exit(1)

    # Save loud-only intervals to CSV for debugging
    pd.DataFrame(loud_intervals, columns=["start", "end"]).to_csv(
        os.path.join(output_folder, "loud_intervals.csv"), index=False
    )
except Exception as e:
    print(f"❌ Error during loud section detection: {e}")
    sys.exit(1)


# Step 2b: Speech detection
speech_intervals = detect_goal_speech(mp3_path)  # list of [start, end]

# Combine and sort intervals
all_intervals = loud_intervals + speech_intervals
all_intervals = sorted(all_intervals, key=lambda x: x[0])

# Merge overlapping intervals
def merge_intervals(intervals, gap=1.0):
    merged = []
    for start, end in intervals:
        if not merged or start > merged[-1][1] + gap:
            merged.append([start, end])
        else:
            merged[-1][1] = max(merged[-1][1], end)
    return merged

final_intervals = merge_intervals(all_intervals)

# Save merged intervals
pd.DataFrame(final_intervals, columns=["start", "end"]).to_csv(
    os.path.join(output_folder, "highlight_intervals.csv"), index=False
)


# Step 3: Extract & Merge Highlights from MP4
from edit_mp4 import extract_and_merge_clips

# 🔍 Automatically detect the MP4 file
mp4_files = [f for f in os.listdir(output_folder) if f.lower().endswith(".mp4")]
if not mp4_files:
    print(f"⚠️ No MP4 files found to merge in: {output_folder}")
    sys.exit(1)

mp4_path = os.path.join(output_folder, mp4_files[0])
print(f"🎥 Using MP4 file: {mp4_path}")


# Define final output path
output_file = os.path.join(output_folder, "highlights_final.mp4")

# Run extraction and merging
extract_and_merge_clips(mp4_path, final_intervals, output_file)
