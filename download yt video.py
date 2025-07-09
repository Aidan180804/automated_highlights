import yt_dlp
import os

# extract mp4

url = input('enter youtube video URL:').strip('""')
file_name = input('enter output file name:').strip('""')
output_folder = r'C:\Users\aidan\OneDrive - The University of Nottingham\Documents\auto highlight project'
output_path = os.path.join(output_folder, file_name + '.%(ext)s')

def download_youtube_as_mp4(url)

ydl_opts = {
    'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/mp4',  # best quality
    'outtmpl': output_path,  # full output path
    'merge_output_format': 'mp4',
}

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
       ydl.download([url])
    
# extract mp3

def download_youtube_as_mp3(url, output_folder):
    output_template = os.path.join(output_folder, f'{file_name}.mp3')

    ydl_opts_mp3 = {
        'format': 'bestaudio/best',
        'outtmpl': output_template,
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'quiet': False,
        'noplaylist': True,
 }

    with yt_dlp.YoutubeDL(ydl_opts_mp3) as ydl:
        ydl.download([url])

download_youtube_as_mp4(url, output_path)
download_youtube_as_mp3(url, output_path)
