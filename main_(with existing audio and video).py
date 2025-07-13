# loud sections from mp3
from loud_sections_from_mp3 import load_audio
from loud_sections_from_mp3 import get_loud_sections
import pandas as pd

output_folder = input('enter path to output folder:').strip('""')
file_path = input("Enter path to mp3 file: ").strip('""')
print(f"File path entered: '{file_path}'")
audio = load_audio(file_path)
intervals = get_loud_sections(audio)
intervals = pd.DataFrame(intervals)
intervals.rename(columns = {0 : 'start', 1 : 'end'}, inplace=True)


# edit mp4
from edit_mp4  import extract_video_clips
from edit_mp4 import merge_and_rename_highlights
import sys

input_video = input('enter path to mp4  file')
output_dir = input('enter different folder directory:').strip('""')
merged_dir = output_folder
if output_dir == merged_dir:
   print("Output directory and merged directory cannot be the same. Exiting program.")
   sys.exit()
else:
    print("Directories are valid. Continuing with processing...")

extract_video_clips(input_video, output_dir, intervals)
merge_and_rename_highlights(output_dir, merged_dir)
