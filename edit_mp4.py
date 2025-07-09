import os
from moviepy.editor import VideoFileClip

def extract_video_clips(input_video, output_dir, intervals):
    os.makedirs(output_dir, exist_ok=True)
    video = VideoFileClip(input_video.strip('""'))
    for idx, row in intervals.iterrows():
        start = row['start']
        end = row['end']
        clip = video.subclip(start, end)
        output_filename = f'clip_{idx+1}_{start:.2f}-{end:.2f}.mp4'
        output_path = os.path.join(output_dir, output_filename)
        clip.write_videofile(output_path, codec='libx264')
    video.close()
    print('Complete!')

if __name__ == "__main__":
  extract_video_clips(input_video, output_dir, intervals)
