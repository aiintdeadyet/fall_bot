
import cv2
import mediapipe as mp
import sys


# Initialize Mediapipe pose
mp_pose = mp.solutions.pose
pose = mp_pose.Pose()


def extract_frames(video_path):
    """Extracts frames from the video file."""
    cap = cv2.VideoCapture(video_path)
    frames = []
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        frames.append(frame)
    cap.release()
    return frames


def detect_pose(frame):
    """Detects pose landmarks in a frame using MediaPipe."""
    results = pose.process(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
    return results.pose_landmarks  # Returns None if no landmarks are detected


def check_for_fall(landmarks):
    """Determines if a fall occurred based on keypoint positions."""
    if landmarks:
        nose_y = landmarks.landmark[mp_pose.PoseLandmark.NOSE].y
        hip_y = landmarks.landmark[mp_pose.PoseLandmark.LEFT_HIP].y
        # Simple heuristic: if the head is close to the ground (y-coordinate is high)
        if nose_y > hip_y + 0.1:  # Adjust threshold as needed
            return True
    return False


def detect_fall_in_video(video_path):
    """Analyzes the video for any fall events."""
    frames = extract_frames(video_path)
    fall_detected = False
    for frame in frames:
        landmarks = detect_pose(frame)
        if check_for_fall(landmarks):
            fall_detected = True
            break  # Exit loop if a fall is detected
    return fall_detected


def main():
    if len(sys.argv) < 2:
        print("Usage: python main.py <video_filepath>")
        sys.exit(1)

    video_path = sys.argv[1]
    fall_detected = detect_fall_in_video(video_path)

    if fall_detected:
        print("Fall detected in the video.")
    else:
        print("No fall detected in the video.")


if __name__ == "__main__":
    main()
