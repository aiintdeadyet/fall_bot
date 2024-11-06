import sys
from ultralytics import YOLO

# Pycache is killing me
# sys.dont_write_bytecode = True

# Import config

from utils.config import data_dir, media_folder, FALL_MODEL_NAME, YOLO_MODEL_NAME
1
# Import utils
from utils.file_utils import clear_temp_segments, select_video_file
from utils.video_utils import process_video, analyze_fall_segments, initialize_pipeline


def main():
    """Main function to execute the fall detection pipeline."""
    # Prepare data directory by removing any existing files
    clear_temp_segments(data_dir)

    # Initialize the video classification pipeline
    pipe = initialize_pipeline()

    # Load the YOLOv8 model
    model = YOLO(YOLO_MODEL_NAME)
    model(verbose=False)[0] # This suppresses output statements that can be a bit annoying

    # Select the video file to process
    video_file = select_video_file()

    # Process the selected video file
    process_video(video_file, model, pipe)

    # Analyze the fall segments
    analyze_fall_segments(pipe)
    
    # Clean up data directory on exit
    clear_temp_segments(data_dir)

if __name__ == "__main__":
    main()
