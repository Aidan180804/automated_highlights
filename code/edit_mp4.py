import os
from moviepy.editor import VideoFileClip
import subprocess

# extract highlight clips
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

# merge and rename highligts
def merge_and_rename_highlights(output_dir, merged_dir):
    """
    Merges all mp4 files in output_dir into a single file in merged_dir, then renames it based on user input.
    """
    # List all mp4 files, sorted by name
    mp4_files = [f for f in os.listdir(output_dir) if f.endswith('.mp4')]
    mp4_files.sort()

    # Create a file list for ffmpeg
    filelist_path = os.path.join(output_dir, 'filelist.txt')
    with open(filelist_path, 'w', encoding='utf-8') as f:
        for filename in mp4_files:
         abs_path = os.path.abspath(os.path.join(output_dir, filename)).replace('\\', '/')
         f.write(f"file '{abs_path}'\n")

    
    # Output file path
    output_file = os.path.join(merged_dir, 'merged_output.mp4')

    # Run ffmpeg to concatenate
    subprocess.run([
        'ffmpeg', '-f', 'concat', '-safe', '0', '-i', filelist_path, '-c', 'copy', output_file
        ], check=True)

    # Remove original mp4 files
    for filename in mp4_files:
        os.remove(os.path.join(output_dir, filename)) 

    # Remove the filelist
    if os.path.exists(filelist_path):
        os.remove(filelist_path)

    print(f"Merged file saved as: {output_file}")

    new_name = input('enter highlights file name:').strip('""') + '.mp4'
    os.rename(output_file,  os.path.join(merged_dir, new_name))

if __name__ == "__main__":
    
  input_video = input('enter path to mp4  file')
  output_dir = input('enter output directory:').strip('""')
  merged_dir = input('enter merged directory:').strip('""')
  extract_video_clips(input_video, output_dir, intervals)
  merge_and_rename_highlights(output_dir, merged_dir)
