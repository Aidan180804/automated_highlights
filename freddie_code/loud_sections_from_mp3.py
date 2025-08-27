import numpy as np
from pydub import AudioSegment
from pydub.utils import make_chunks
from pydub.effects import normalize
from sklearn.mixture import GaussianMixture
import pandas as pd
import os
import sys

def load_audio(file_path):
    if file_path.lower().endswith('.mp3'):
        audio = AudioSegment.from_mp3(file_path)
    else:
        raise ValueError("Unsupported file type")
    return normalize(audio)

def pad_intervals(intervals, pad_before=1.0, pad_after=1.0, total_length=None):
    padded = []
    for start, end in intervals:
        new_start = max(0, start - pad_before)
        new_end = end + pad_after
        if total_length:
            new_end = min(new_end, total_length)
        padded.append((new_start, new_end))
    return padded

def is_speech_like(volume_segment):
    return -40 < volume_segment < -10

def get_loud_sections(audio, chunk_ms=100, interval_sec=5, pad_sec=1.0, max_intervals=30):
    chunks = make_chunks(audio, chunk_ms)
    volumes = np.array([chunk.dBFS for chunk in chunks])
    valid_volumes = volumes[volumes != float('-inf')]

    if len(valid_volumes) == 0:
        print("⚠️ Audio is completely silent.")
        return []

    # GMM to separate loud vs quiet segments
    X = valid_volumes.reshape(-1, 1)
    gmm = GaussianMixture(n_components=2, random_state=42).fit(X)
    means = gmm.means_.flatten()
    threshold = np.min(means) + 0.5 * (np.max(means) - np.min(means))
    loud_indices = np.where(volumes > threshold)[0]

    # Merge contiguous loud chunks
    merged = []
    for idx in loud_indices:
        if not merged or idx > merged[-1][1] + 1:
            merged.append([idx, idx])
        else:
            merged[-1][1] = idx

    # Extract info-rich intervals
    intervals = []
    for start_idx, end_idx in merged:
        region_volumes = volumes[start_idx:end_idx + 1]
        if len(region_volumes) == 0:
            continue
        peak_idx = np.argmax(region_volumes) + start_idx
        peak_time = peak_idx * chunk_ms / 1000.0
        start_time = max(0, peak_time - (interval_sec * 1.5))
        end_time = min(len(audio) / 1000.0, peak_time + (interval_sec * 0.5))

        speech_score = np.mean([is_speech_like(v) for v in region_volumes])

        intervals.append({
            "start": start_time,
            "end": end_time,
            "duration": end_time - start_time,
            "peak_volume": volumes[peak_idx],
            "speech_likelihood": speech_score
        })

    if not intervals:
        return []

    total_duration = len(audio) / 1000.0

    # Score and sort
    for i in intervals:
        i["score"] = i["peak_volume"] + 2.0 * i["speech_likelihood"] + 0.5 * i["duration"]
    intervals = sorted(intervals, key=lambda x: x["score"], reverse=True)
    top_intervals = intervals[:max_intervals]
    top_intervals.sort(key=lambda x: x["start"])

    # Merge overlapping or close intervals
    def merge_close_intervals(intervals, merge_gap=1.0):
        merged = []
        for interval in intervals:
            if not merged:
                merged.append(interval)
            else:
                last = merged[-1]
                if interval["start"] <= last["end"] + merge_gap:
                    last["end"] = max(last["end"], interval["end"])
                    last["score"] = max(last["score"], interval["score"])
                else:
                    merged.append(interval)
        return merged

    top_intervals = merge_close_intervals(top_intervals)

    clean_intervals = [(i["start"], i["end"]) for i in top_intervals]
    return pad_intervals(clean_intervals, pad_before=pad_sec, pad_after=pad_sec, total_length=total_duration)
