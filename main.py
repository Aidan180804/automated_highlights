# download yt video
from download_yt_video import ask_for_url
from download_yt_video import download_youtube_as_mp4
from download_yt_video import download_youtube_as_mp3

url, output_path = ask_for_url()
download_youtube_as_mp4(url, output_path)
download_youtube_as_mp3(url, output_path)


# loud sections from mp3
from loud_sections_from_mp3 import load_audio
from loud_sections_from_mp3 import get_loud_sections
import pandas as pd

file_path = input("Enter path to mp3 file: ").strip('""')
print(f"File path entered: '{file_path}'")
audio = load_audio(file_path)
intervals = get_loud_sections(audio)
intervals = pd.DataFrame(intervals)
intervals.rename(columns = {0 : 'start', 1 : 'end'}, inplace=True)


# edit mp4
from edit_mp4  import extract_video_clips
from edit_mp4 import merge_and_rename_highlights

input_video = input('enter path to mp4  file')
output_dir = r'C:\Users\aidan\OneDrive - The University of Nottingham\Documents\auto highlight project\audio files'
merged_dir = r'C:\Users\aidan\OneDrive - The University of Nottingham\Documents\auto highlight project'
extract_video_clips(input_video, output_dir, intervals)
merge_and_rename_highlights(output_dir, merged_dir)



