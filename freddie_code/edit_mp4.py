import os
import pandas as pd
from moviepy.editor import VideoFileClip, concatenate_videoclips
from moviepy.video.fx.fadein import fadein
from moviepy.video.fx.fadeout import fadeout

def extract_and_merge_clips(input_video, intervals, output_file, padding=1.5, max_duration=480):
    """
    Extracts video clips based on provided intervals and merges them into one final file.
    Limits total merged video duration to `max_duration` seconds.
    """
    input_video = os.path.abspath(input_video.strip('"'))

    try:
        video = VideoFileClip(input_video)
    except Exception as e:
        print(f"\u274c Error loading video: {e}")
        return

    total_duration = video.duration
    print(f"\ud83c\udfa5 Video duration: {total_duration:.2f}s")

    # Ensure intervals are sorted by start time
    intervals = intervals.sort_values(by='start').reset_index(drop=True)

    clips = []
    current_total = 0.0

    for idx, row in intervals.iterrows():
        start = max(0, row['start'] - padding)
        end = min(total_duration, row['end'] + padding)

        if start >= total_duration:
            print(f"Skipping clip {idx}: start time ({start:.2f}s) >= video duration.")
            continue

        duration = end - start
        if current_total + duration > max_duration:
            continue

        try:
            clip = video.subclip(start, end)
            clips.append(clip)
            current_total += duration
        except Exception as e:
            print(f"Error processing clip {idx}: {e}")
            continue

        if current_total >= max_duration:
            break

    if not clips:
        print("\u26a0\ufe0f No valid clips to merge.")
        return

    try:
        final_clip = concatenate_videoclips(clips)
        final_clip.write_videofile(output_file, codec='libx264', audio_codec='aac')
        print(f"\u2705 Final highlight saved to: {output_file}")
    except Exception as e:
        print(f"\u274c Error during merging: {e}")
    finally:
        video.close()

if __name__ == "__main__":
    import sys

    input_video = input("Enter path to MP4 file: ").strip('"')
    output_file = input("Enter full path and name for the final merged highlight (e.g. highlights.mp4): ").strip('"')

    try:
        intervals = pd.read_csv("highlight_intervals.csv")
    except Exception as e:
        print("\u274c Failed to load intervals:", e)
        sys.exit(1)

    extract_and_merge_clips(input_video, intervals, output_file)
