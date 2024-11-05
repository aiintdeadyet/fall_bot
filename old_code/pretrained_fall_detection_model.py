# This version works pretty good
from transformers import pipeline
import cv2
import os
import shutil


# Initialize the video classification pipeline
pipe = pipeline("video-classification", model="yadvender12/videomae-base-finetuned-kinetics-finetuned-fall-detect")

# Define the path to your video file you can swap this out with fall.mp4 as well
video_path = "fall2.mp4"
cap = cv2.VideoCapture(video_path)

fps = cap.get(cv2.CAP_PROP_FPS)
frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
duration = frame_count / fps
segment_duration = 2  # seconds per segment

fall_predictions = []


# Function to clear all files inside a directory
def clear_directory(directory):
    if os.path.exists(directory):
        for filename in os.listdir(directory):
            file_path = os.path.join(directory, filename)
            try:
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.unlink(file_path)  # Remove the file or symbolic link
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)  # Remove a directory
            except Exception as e:
                print(f'Failed to delete {file_path}. Reason: {e}')
    else:
        os.makedirs(directory)  

# Clear the directory before we start
clear_directory("temp_segments")

# Directory to store temporary sub-videos
os.makedirs("temp_segments", exist_ok=True)

fall_count = 0

# Process video in segments and track timestamps
for start_time in range(0, int(duration), segment_duration):
    cap.set(cv2.CAP_PROP_POS_MSEC, start_time * 1000)

    # Create a VideoWriter to save each sub-video segment
    segment_path = f"temp_segments/segment_{fall_count}.mp4"
    fall_count = fall_count + 1 
    fourcc = cv2.VideoWriter_fourcc(*"mp4v")
    out = cv2.VideoWriter(segment_path, fourcc, fps, (int(cap.get(3)), int(cap.get(4))))

    for _ in range(int(fps * segment_duration)):
        ret, frame = cap.read()
        if not ret:
            break
        out.write(frame)

    out.release()

    # Run the model on each sub-video
    result = pipe(segment_path)

    # Log only fall predictions with timestamps
    for pred in result:
        if 'fall' in pred['label'].lower():  # Adjust the condition as needed
            fall_predictions.append({
                "time": start_time,
                "label": pred["label"],
                "confidence": pred["score"]
            })
            print(f"FALL DETECTED! Time: {start_time} sec - Label: {pred['label']}, Confidence: {pred['score']}")

cap.release()

# Print all fall predictions
if fall_predictions:
    print("\nAll fall predictions:")
    print(f"All Falls: {len(fall_predictions)}")
    for fall in fall_predictions:
        print(f"Time: {fall['time']} sec - Label: {fall['label']}, Confidence: {fall['confidence']}")
else:
    print("No falls detected.")

