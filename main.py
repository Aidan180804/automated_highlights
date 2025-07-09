from download_yt_video import ask_for_url
from download_yt_video import download_youtube_as_mp4
from download_yt_video import download_youtube_as_mp3

url, output_path = ask_for_url()
download_youtube_as_mp4(url, output_path)
download_youtube_as_mp3(url, output_path)
