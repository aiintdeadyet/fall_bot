import sys
from ultralytics import YOLO
import os

# Pycache is killing me
# sys.dont_write_bytecode = True

# Import config

from utils.config import data_dir, potential_falls_dir, media_folder, FALL_MODEL_NAME, YOLO_MODEL_NAME
# Import utils
from utils.file_utils import clear_temp_segments, select_video_file
from utils.video_utils import process_video, analyze_fall_segments, initialize_pipeline, process_webcam


def main():
    """Main function to execute the fall detection pipeline."""
    # Prepare data directory by removing any existing files
    clear_temp_segments(data_dir)
    clear_temp_segments(potential_falls_dir)

    # Ensure the directory exists after clearing
    os.makedirs(data_dir, exist_ok=True)
    os.makedirs(potential_falls_dir, exist_ok=True)


    # Initialize the video classification pipeline
    pipe = initialize_pipeline()

    # Load the YOLOv8 model
    model = YOLO(YOLO_MODEL_NAME)
    model(verbose=False)[0] # This suppresses output statements that can be a bit annoying

    # Select the video file to process
    video_file = select_video_file()

    # Process the selected video file
    if video_file == 'webcam':
        process_webcam(model, pipe)
    else:
        process_video(video_file, model, pipe)

    # Analyze the fall segments
    analyze_fall_segments(pipe)
    
    # Clean up data directory on exit
    clear_temp_segments(data_dir)
    clear_temp_segments(potential_falls_dir)

if __name__ == "__main__":
    main()
