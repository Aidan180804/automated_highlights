import whisper
import os

# Load Whisper once globally
model = whisper.load_model("base")

KEYWORDS = ["goal", "scores", "he scores", "what a goal", "it's in", "finds the net"]

def detect_goal_speech(mp3_path, keywords=KEYWORDS, min_gap=10.0):
    print("🗣️ Running speech recognition...")

    result = model.transcribe(mp3_path, fp16=False)
    segments = result.get("segments", [])

    goal_times = []
    last_added = -min_gap

    for seg in segments:
        text = seg['text'].lower()
        start_time = seg['start']
        for word in keywords:
            if word in text and (start_time - last_added) > min_gap:
                goal_times.append((start_time - 2, start_time + 4))  # small window around speech
                last_added = start_time
                break

    print(f"⚽ Detected {len(goal_times)} goal-related speech moments.")
    return goal_times
