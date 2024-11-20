import os
import sys
import shutil
import tkinter as tk
from tkinter import filedialog
from colorama import init, Fore

# Config
# sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.config import data_dir, media_folder, FALL_MODEL_NAME

# setup
init(autoreset=True) # Initialize colorama

# Delete all files in the temp_segments directory
# Set debug=True print out debug statements
def clear_temp_segments(directory, debug=True):
    """Clear all files in the specified directory. Remove directory if it is empty after clearing files."""
    
    # Create directory if it doesn't exist
    os.makedirs(directory, exist_ok=True)
    if debug:
        print(Fore.GREEN + f"Ensuring directory exists: {directory}")
    
    # Remove files in the directory
    for filename in os.listdir(directory):
        file_path = os.path.join(directory, filename)
        try:
            if os.path.isfile(file_path):
                os.unlink(file_path)  # Remove the file
                if debug:
                    print(Fore.YELLOW + f"Deleted file: {file_path}")
        except Exception as e:
            if debug:
                print(Fore.RED + f"Failed to delete {file_path}. Reason: {e}")

    # Check if the directory is now empty; if so, remove it
    if not os.listdir(directory):
        try:
            os.rmdir(directory)
            if debug:
                print(Fore.GREEN + f"Directory '{directory}' was empty and has been removed.")
        except Exception as e:
            if debug:
                print(Fore.RED + f"Failed to remove directory '{directory}'. Reason: {e}")
            

def show_file_picker():
    """Show a file picker dialog and return an array of selected file paths.  Supports multiple file uploads at once"""
    
    # Make a top-level instance and hide it
    root = tk.Tk()
    root.withdraw()

    # Make it almost invisible - no decorations, 0 size, top left corner
    root.overrideredirect(True)
    root.geometry('0x0+0+0')

    # Show window again and lift it to top for focus
    root.deiconify()
    root.lift()
    root.focus_force()

    # Open file dialog and return selected filenames
    filenames = filedialog.askopenfilenames(parent=root)

    # Destroy the top-level instance to make it invisible again
    root.destroy()

    return filenames



# Prompt the user to select a video file to process from the 'media' folder
# Or Upload, up to, multiple video files at once
def select_video_file():
    """Prompt the user to select or upload a video file from the 'media' folder."""
    
    # Ensure the media directory exists; create if it doesn't
    os.makedirs(media_folder, exist_ok=True)
    
    # Define allowed video extensions
    video_extensions = ('.mp4', '.mov')  # Add other media extensions if needed

    # Get a list of existing video files in the media folder
    video_files = [f for f in os.listdir(media_folder) if f.endswith(video_extensions)]
    
    while True:
        # Display options
        extensions_list = ', '.join(video_extensions)
        print(Fore.CYAN + f"\nEnter 'u' to upload a video ({extensions_list})")
        print("Enter 'l' for live video input")
        print("Enter 'q' to quit")
        print("Or select an uploaded video below:\n")
        
        # List existing video files
        if video_files:
            for idx, file in enumerate(video_files, start=1):
                print(Fore.YELLOW + f"{idx}. {file}")
        else:
            print(Fore.YELLOW + "No video files found in the 'media' folder. Uploading files can be selected using 'u'.\n")

        # Get user input
        #user_input = input(Fore.CYAN + "\nEnter 'u' to upload, 'q' to quit, or a number to select a file: ")
        user_input = input(Fore.GREEN + "Your choice: ").strip().lower()


        # Handle quit
        if user_input.lower() == 'q':
            print(Fore.GREEN + "\nExiting program.\n")
            exit()

        elif user_input == 'l':
            print(Fore.GREEN + "Live video input selected.")
            return 'live'

        # Handle upload option
        elif user_input.lower() == 'u':
            # Use show_file_picker() to get the selected files
            selected_files = show_file_picker()
            
            for file_path in selected_files:
                # Check if the file is of the correct type
                if not file_path.endswith(video_extensions):
                    print(Fore.RED + f"Invalid file type: {file_path}. Skipping.")
                    continue  # Skip files that don't match the required extension
                
                # Check if file already exists in the media folder
                destination = os.path.join(media_folder, os.path.basename(file_path))
                if os.path.exists(destination):
                    print(Fore.YELLOW + f"File {file_path} already exists in {media_folder}. Skipping.")
                else:
                    try:
                        # Copy file to media folder
                        shutil.copy(file_path, destination)
                        print(Fore.GREEN + f"Uploaded {os.path.basename(file_path)} to '{media_folder}'")
                    except Exception as e:
                        print(Fore.RED + f"Failed to upload file {file_path}. Reason: {e}")
            
            # Refresh video_files list to include new uploads
            video_files = [f for f in os.listdir(media_folder) if f.endswith(video_extensions)]

        # Handle selection of an existing file
        elif user_input.isdigit():
            choice = int(user_input)
            if 1 <= choice <= len(video_files):
                return os.path.join(media_folder, video_files[choice - 1])

        # Invalid input handling
        else:
            print(Fore.RED + "Invalid input. Please enter 'u', 'q', or a number corresponding to a video file.")

def process_video(video_file, model, pipe):
    if video_file == 'live':
        cap = cv2.VideoCapture(0)
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            # Process the frame with the model and pipeline
            process_frame(frame, model, pipe)
            cv2.imshow('Live Video', frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        cap.release()
        cv2.destroyAllWindows()
    else:
        # Existing code to process video file
        pass
def process_frame(frame, model, pipe):
    # Implement frame processing logic here
    pass

if __name__ == "__main__":
    # Initialize the video classification pipeline
    pipe = initialize_pipeline()

    # Load the YOLOv8 model
    model = YOLO(YOLO_MODEL_NAME)
    model(verbose=False)[0]

    # Select the video file to process
    video_file = select_video_file()

    # Process the selected video file
    process_video(video_file, model, pipe)

    # Analyze the fall segments
    analyze_fall_segments(pipe)
    
    # Clean up data directory on exit
    clear_temp_segments(data_dir)