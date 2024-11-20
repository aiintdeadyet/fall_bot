import cv2
import cvzone
import collections
import time
import os
import sys
from colorama import init, Fore
from transformers import pipeline

# Setup    
init(autoreset=True) # Initialize colorama


# Import config
# sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.config import data_dir, FALL_MODEL_NAME

# Initialize Video Classification Pipeline
def initialize_pipeline():
    """Initialize the video classification pipeline."""
    return pipeline("video-classification", model=FALL_MODEL_NAME)
      

def process_video(video_file, model, pipe):
    """Creates clips of possible falls in the video and saves them in the temp_segments directory."""
    message_printed = False
    if video_file == 'live':
        cap = cv2.VideoCapture(0)
        print(Fore.GREEN + "Using live video input from webcam.")
    else:
        cap = cv2.VideoCapture(video_file)
        print(Fore.GREEN + f"Using video file: {video_file}")

    if not cap.isOpened():
        print(Fore.RED + "Error: Could not open video source.")
        return
    
    # Let's make checkpoints in the video when we think there might be a fall
    ##cap = cv2.VideoCapture(video_file)
    count = 0
    frame_buffer = collections.deque(maxlen=30)  # Buffer to store frames
    fall_detected = False
    fall_start_time = None
    video_writer = None

    # Loop every 3rd video frame
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        count += 1
        if count % 3 != 0:
            continue

        # Resize the frame to a standard size
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

            # Loop through each object box in the frame
            for box, class_id, track_id, conf in zip(boxes, class_ids, track_ids, confidences):
                detected_object = model.model.names[class_id]
                x1, y1, x2, y2 = box
                h = y2 - y1
                w = x2 - x1
                thresh = h - w

                # Width > Height ? Possible Fall 
                if thresh <= 0:
                    cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 255), 2)
                    cvzone.putTextRect(frame, f'{track_id}', (x1, y2), 1, 1)
                    cvzone.putTextRect(frame, f"{'Fall'}", (x1, y1), 1, 1)

                    # If a fall is detected, initialize a video writer and start recording
                    if not fall_detected:
                        fall_detected = True
                        fall_start_time = time.time()
                        # Initialize video writer
                        # specify 4 letter CODEC to tell cv2 how the video should be saved
                        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
                        video_writer = cv2.VideoWriter(f'{data_dir}/fall_detected_{int(fall_start_time)}.mp4', fourcc, 30, (1020, 600))
                        
                        # Write whatever frames are available in the buffer
                        for buffered_frame in frame_buffer:
                            video_writer.write(buffered_frame)
                    video_writer.write(frame)

                # If no fall is detected, draw a green rectangle around the object
                else:
                    cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                    cvzone.putTextRect(frame, f'{track_id}', (x1, y2), 1, 1)
                    cvzone.putTextRect(frame, f"{'Normal'}", (x1, y1), 1, 1)

                    # Fall was detected previously but not now
                    if fall_detected:
                        # Stop recording when fall is over
                        fall_detected = False
                        video_writer.release()
                        video_writer = None

        if video_file == 'live':
            cv2.imshow("Live Video", frame)
            if message_printed == False:
                print(Fore.GREEN + "Press 'q' to stop video capture.")
                message_printed = True

        else: 
            cv2.imshow("RGB", frame)
            if cv2.waitKey(1) & 0xFF == ord("q"):
                break

        # Break the loop if 'q' is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            print(Fore.GREEN + "Stopping video capture.")
            break

    # Release resources when video processing is complete
    cap.release()
    cv2.destroyAllWindows()
    if video_writer:
        video_writer.release()


def analyze_fall_segments(pipe):
    """Analyze saved fall segments with the pretrained model."""
    fall_count = 0  # Counter for the number of falls detected
    
    # Get all clips of possible falls
    for filename in os.listdir(data_dir):
        
        # Process each fall clip
        if filename.endswith('.mp4'):
            video_path = os.path.join(data_dir, filename)
            
            # Run the model on each sub-video
            try:
                result = pipe(video_path)
            except RuntimeError as e:
                # Stop checking this clip if some error occurs
                print(Fore.RED + f"Error processing video! {video_path}: {e}")
                continue

            # Check if the pretrained model also detects a fall
            fall_detected_by_model = any('fall' in pred['label'].lower() for pred in result)

            if fall_detected_by_model:
                fall_count += 1  # Increment fall count only if both models detect a fall
                for pred in result:
                    if 'fall' in pred['label'].lower():
                        print(Fore.GREEN + f"{fall_count} FALL DETECTED! Label: {pred['label']}, Confidence: {pred['score']}")
                        cap = cv2.VideoCapture(video_path)
                        while cap.isOpened():
                            ret, frame = cap.read()
                            if not ret:
                                break
                            cv2.putText(frame, f"{fall_count} FALL DETECTED! Label: {pred['label']}, Confidence: {pred['score']}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
                            cv2.imshow("Fall Detection", frame)
                            if cv2.waitKey(1) & 0xFF == ord('q'):
                                break
                        cap.release()
                        cv2.destroyAllWindows()

    # Print the total number of falls detected
    print(f"Total number of falls detected: {fall_count}")