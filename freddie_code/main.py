import os
import sys
import pandas as pd

# Step 1: Download YouTube Video
from download_yt_video import ask_for_url, download_youtube_as_mp4, download_youtube_as_mp3

url, video_output_path, audio_output_path, output_folder = ask_for_url()

download_youtube_as_mp4(url, video_output_path)
download_youtube_as_mp3(url, audio_output_path)


# Step 2: Detect Loud Sections from Audio
from loud_sections_from_mp3 import load_audio, get_loud_sections

# 🔍 Automatically detect the MP3 file instead of assuming a fixed name
mp3_files = [f for f in os.listdir(output_folder) if f.lower().endswith(".mp3")]
if not mp3_files:
    print(f"❌ No .mp3 file found in folder: {output_folder}")
    sys.exit(1)

mp3_path = os.path.join(output_folder, mp3_files[0])
print(f"📥 Using MP3 file: {mp3_path}")

try:
    audio = load_audio(mp3_path)
    raw_intervals = get_loud_sections(audio)

    if not raw_intervals:
        print("⚠️ No loud intervals found. Exiting.")
        sys.exit(1)

    # Save intervals to CSV for debugging or reuse
    intervals = pd.DataFrame(raw_intervals, columns=["start", "end"])
    intervals.to_csv(os.path.join(output_folder, "highlight_intervals.csv"), index=False)
except Exception as e:
    print(f"❌ Error during loud section detection: {e}")
    sys.exit(1)
from speech_detection import detect_goal_speech

# Get intervals from loudness
loud_intervals = get_loud_sections(audio)

# Get intervals from speech
speech_intervals = detect_goal_speech(mp3_path)

# Combine and deduplicate
all_intervals = loud_intervals + speech_intervals
all_intervals = sorted(all_intervals, key=lambda x: x[0])  # sort by start time

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

# Save intervals
intervals_df = pd.DataFrame(final_intervals, columns=["start", "end"])
intervals_df.to_csv(os.path.join(output_folder, "highlight_intervals.csv"), index=False)

# Step 3: Extract & Merge Highlights from MP4
from edit_mp4 import extract_and_merge_clips

# 🔍 Automatically detect the MP4 file
mp4_files = [f for f in os.listdir(output_folder) if f.lower().endswith(".mp4")]
if not mp4_files:
    print(f"⚠️ No MP4 files found to merge in: {output_folder}")
    sys.exit(1)

mp4_path = os.path.join(output_folder, mp4_files[0])
print(f"🎥 Using MP4 file: {mp4_path}")

output_dir = input("📂 Enter a folder to save individual highlight clips: ").strip('"')
merged_dir = output_folder  # merged video will go back to same folder

if output_dir == merged_dir:
    print("❌ Output directory and merged directory must be different. Exiting.")
    sys.exit(1)

# Clean & validate paths
output_dir = os.path.abspath(output_dir)
merged_dir = os.path.abspath(merged_dir)
os.makedirs(output_dir, exist_ok=True)
# Define final output path

output_file = os.path.join(output_folder, "highlights_final.mp4")

# Run extraction and merging
extract_and_merge_clips(mp4_path, intervals, output_file)
