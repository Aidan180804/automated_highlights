import numpy as np
from pydub import AudioSegment
from pydub.utils import make_chunks
import pandas as pd
import os

def load_audio(file_path):
    if file_path.lower().endswith('.mp3'):
        audio = AudioSegment.from_mp3(file_path)
    else:
        raise ValueError("Unsupported file type")
    return audio


def get_loud_sections(audio, chunk_ms=100, interval_sec=5):
    # Break audio into chunks
    chunks = make_chunks(audio, chunk_ms)
    volumes = np.array([chunk.dBFS for chunk in chunks])
    # Filter out -inf (silent) values for mean/std calculation
    valid_volumes = volumes[volumes != float('-inf')]
    if len(valid_volumes) == 0:
        print("Audio is completely silent.")
        return []
    mean_db = np.mean(valid_volumes)
    std_db = np.std(valid_volumes)
    # Define loud as mean + threshold_db or mean + 2*std
    loud_threshold = mean_db + 1.5*std_db
    loud_indices = np.where(volumes > loud_threshold)[0]
    # Merge close indices
    merged = []
    for idx in loud_indices:
        if not merged or idx > merged[-1][1] + 1:
            merged.append([idx, idx])
        else:
            merged[-1][1] = idx
    # Get intervals
    intervals = []
    for start_idx, end_idx in merged:
        # Find the peak within this region
        region_volumes = volumes[start_idx:end_idx+1]
        # If all are -inf, skip
        if np.all(region_volumes == float('-inf')):
            continue
        peak_idx = np.argmax(region_volumes) + start_idx
        peak_time = peak_idx * chunk_ms / 1000.0
        start_time = max(0, peak_time - interval_sec)
        end_time = min(len(audio) / 1000.0, peak_time + interval_sec)
        intervals.append((start_time, end_time))
    # Merge overlapping intervals
    if not intervals:
        return []
    # Sort intervals by start time
    intervals.sort(key=lambda x: x[0])
    merged_intervals = [intervals[0]]
    for current in intervals[1:]:
        last = merged_intervals[-1]
        if current[0] <= last[1]:  # Overlap
            merged_intervals[-1] = (last[0], max(last[1], current[1]))
        else:
            merged_intervals.append(current)
    return merged_intervals


if __name__ == "__main__":
    file_path = input("Enter path to mp3 file: ").strip('""')
    print(f"File path entered: '{file_path}'")
    try:
        audio = load_audio(file_path)
        intervals = get_loud_sections(audio)
        print("Loud intervals found:", intervals)
    except Exception as e:
        print("Error:", e)
