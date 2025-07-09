from download_yt_video import ask_for_url
from download_yt_video import download_youtube_as_mp4
from download_yt_video import download_youtube_as_mp3

url, output_path = ask_for_url()
download_youtube_as_mp4(url, output_path)
download_youtube_as_mp3(url, output_path)





file_path = input("Enter path to mp3 file: ").strip('""')
print(f"File path entered: '{file_path}'")
audio = load_audio(file_path)
intervals = get_loud_sections(audio)
intervals.rename(columns = {0 : 'start', 1 : 'end'}, inplace=True)
if not intervals:
  print("No loud sections found.")
     
else:
  print("complete.")
