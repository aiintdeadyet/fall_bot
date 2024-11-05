import cv2
import numpy as np
from ultralytics import YOLO
import cvzone
import collections
import time
import os
from transformers import pipeline

def clear_temp_segments(directory):
    """Clear all files in the specified directory."""
    for filename in os.listdir(directory):
        file_path = os.path.join(directory, filename)
        try:
            if os.path.isfile(file_path):
                os.unlink(file_path)  # Remove the file
        except Exception as e:
            print(f"Failed to delete {file_path}. Reason: {e}")

def initialize_pipeline():
    """Initialize the video classification pipeline."""
    return pipeline("video-classification", model="yadvender12/videomae-base-finetuned-kinetics-finetuned-fall-detect")

def select_video_file():
    """Prompt the user to select a video file to process."""
    print("Select the video file to process:\n1. fall.mp4\n2. fall2.mp4")
    video_choice = input()
    if video_choice == '1':
        return 'fall.mp4'
    elif video_choice == '2':
        return 'fall2.mp4'
    else:
        print("Invalid input. Exiting.")
        exit()

def process_video(video_file, model, pipe):
    """Process the selected video file for fall detection."""
    cap = cv2.VideoCapture(video_file)
    count = 0
    frame_buffer = collections.deque(maxlen=30)  # Buffer to store frames
    fall_detected = False
    fall_start_time = None
    video_writer = None

    while True:
        ret, frame = cap.read()
        if not ret:
            break
        count += 1
        if count % 3 != 0:
            continue

        frame = cv2.resize(frame, (1020, 600))
        frame_buffer.append(frame.copy())  # Store the current frame in the buffer

        # Run YOLOv8 tracking on the frame
        results = model.track(frame, persist=True, classes=0)

        # Check if there are any boxes in the results
        if results[0].boxes is not None and results[0].boxes.id is not None:
            # Get the boxes (x, y, w, h), class IDs, track IDs, and confidences
            boxes = results[0].boxes.xyxy.int().cpu().tolist()  # Bounding boxes
            class_ids = results[0].boxes.cls.int().cpu().tolist()  # Class IDs
            track_ids = results[0].boxes.id.int().cpu().tolist()  # Track IDs
            confidences = results[0].boxes.conf.cpu().tolist()  # Confidence score

            for box, class_id, track_id, conf in zip(boxes, class_ids, track_ids, confidences):
                c = model.model.names[class_id]
                x1, y1, x2, y2 = box
                h = y2 - y1
                w = x2 - x1
                thresh = h - w

                if thresh <= 0:
                    cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 255), 2)
                    cvzone.putTextRect(frame, f'{track_id}', (x1, y2), 1, 1)
                    cvzone.putTextRect(frame, f"{'Fall'}", (x1, y1), 1, 1)

                    if not fall_detected:
                        fall_detected = True
                        fall_start_time = time.time()
                        # Initialize video writer
                        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
                        video_writer = cv2.VideoWriter(f'temp_segments/fall_detected_{int(fall_start_time)}.mp4', fourcc, 30, (1020, 600))
                        
                        # Write whatever frames are available in the buffer
                        for buffered_frame in frame_buffer:
                            video_writer.write(buffered_frame)

                    video_writer.write(frame)

                else:
                    cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                    cvzone.putTextRect(frame, f'{track_id}', (x1, y2), 1, 1)
                    cvzone.putTextRect(frame, f"{'Normal'}", (x1, y1), 1, 1)

                    if fall_detected:
                        # Stop recording when fall is over
                        fall_detected = False
                        video_writer.release()
                        video_writer = None

        cv2.imshow("RGB", frame)
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    # Release resources
    cap.release()
    cv2.destroyAllWindows()
    if video_writer:
        video_writer.release()

def analyze_fall_segments(pipe):
    """Analyze saved fall segments with the pretrained model."""
    fall_count = 0  # Counter for the number of falls detected
    for filename in os.listdir('temp_segments'):
        if filename.endswith('.mp4'):
            video_path = os.path.join('temp_segments', filename)
            
            # Run the model on each sub-video
            try:
                result = pipe(video_path)
            except RuntimeError as e:
                print_red(f"Error processing video! {video_path}: {e}")
                #print(f"Error processing video! {video_path}: {e}")
                continue

            # Check if the pretrained model also detects a fall
            fall_detected_by_model = any('fall' in pred['label'].lower() for pred in result)

            if fall_detected_by_model:
                fall_count += 1  # Increment fall count only if both models detect a fall
                for pred in result:
                    if 'fall' in pred['label'].lower():
                        print_green(f"{fall_count} FALL DETECTED! Label: {pred['label']}, Confidence: {pred['score']}")
                        #print(f"{fall_count} FALL DETECTED! Label: {pred['label']}, Confidence: {pred['score']}")

    # Print the total number of falls detected
    print(f"Total number of falls detected: {fall_count}")

def print_green(text):
    """Print text in green color."""
    print(f"\033[92m{text}\033[0m")

def print_red(text):
    """Print text in red color."""
    print(f"\033[91m{text}\033[0m")


def main():
    """Main function to execute the fall detection pipeline."""
    # Clear temporary segments directory
    clear_temp_segments('temp_segments')

    # Initialize the video classification pipeline
    pipe = initialize_pipeline()

    # Load the YOLOv8 model
    model = YOLO("yolo11s.pt")
    model(verbose=False)[0] # This suppresses output statements that can be a bit annoying

    # Select the video file to process
    video_file = select_video_file()

    # Process the selected video file
    process_video(video_file, model, pipe)

    # Analyze the fall segments
    analyze_fall_segments(pipe)

if __name__ == "__main__":
    main()
