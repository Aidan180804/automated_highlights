import yt_dlp
import os

# extract mp4

def ask_for_url():
    
 url = input('enter youtube video URL:').strip('""')
 file_name = input('enter output file name:').strip('""')
 output_folder = r'C:\Users\aidan\OneDrive - The University of Nottingham\Documents\auto highlight project'
 output_path = os.path.join(output_folder, file_name + '.%(ext)s')

 return url, output_path

def download_youtube_as_mp4(url, output_path):

    ydl_opts = {
    'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/mp4',  # best quality
    'outtmpl': output_path,  # full output path
    'merge_output_format': 'mp4',
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
       ydl.download([url])
    
# extract mp3

def download_youtube_as_mp3(url, output_path):
    ydl_opts_mp3 = {
        'format': 'bestaudio/best',
        'outtmpl': output_path,
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



if __name__ == "__main__":
    url, output_path = ask_for_url()
    download_youtube_as_mp4(url, output_path)
    download_youtube_as_mp3(url, output_path)
