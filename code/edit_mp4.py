import os
from moviepy.editor import VideoFileClip, concatenate_videoclips

def extract_and_merge_clips(input_video, intervals, output_file, padding=1.5, max_duration=480):
    """
    Extracts video clips based on provided intervals (list of [start, end])
    and merges them into one final file.
    Limits total merged video duration to `max_duration` seconds.
    """
    input_video = os.path.abspath(input_video.strip('"'))

    try:
        video = VideoFileClip(input_video)
    except Exception as e:
        print(f"❌ Error loading video: {e}")
        return

    total_duration = video.duration
    print(f"🎥 Video duration: {total_duration:.2f}s")

    # Sort intervals by start time
    intervals = sorted(intervals, key=lambda x: x[0])

    clips = []
    current_total = 0.0

    for idx, (start, end) in enumerate(intervals):
        start = max(0, start - padding)
        end = min(total_duration, end + padding)

        if start >= total_duration:
            print(f"⚠️ Skipping clip {idx}: start time ({start:.2f}s) >= video duration.")
            continue

        duration = end - start
        if current_total + duration > max_duration:
            # stop adding clips if total duration would exceed max_duration
            break

        try:
            clip = video.subclip(start, end)
            clips.append(clip)
            current_total += duration
        except Exception as e:
            print(f"❌ Error processing clip {idx}: {e}")
            continue

        if current_total >= max_duration:
            break

    if not clips:
        print("❌ No valid clips to merge.")
        return

    try:
        final_clip = concatenate_videoclips(clips)
        final_clip.write_videofile(output_file, codec='libx264', audio_codec='aac')
        print(f"✅ Final highlight saved to: {output_file}")
    except Exception as e:
        print(f"❌ Error during merging: {e}")
    finally:
        video.close()


# Optional CLI interface
if __name__ == "__main__":
    import sys
    import pandas as pd

    input_video = input("Enter path to MP4 file: ").strip('"')
    output_file = input("Enter full path and name for the final merged highlight (e.g. highlights.mp4): ").strip('"')

    try:
        intervals_df = pd.read_csv("highlight_intervals.csv")
        intervals = intervals_df[['start', 'end']].values.tolist()  # convert to list
    except Exception as e:
        print("❌ Failed to load intervals:", e)
        sys.exit(1)

    extract_and_merge_clips(input_video, intervals, output_file)
