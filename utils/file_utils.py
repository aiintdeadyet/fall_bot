import os
from colorama import init, Fore

# Utilized Directories
from config import data_dir, media_folder, FALL_MODEL_NAME

# setup
init(autoreset=True) # Initialize colorama

# Delete all files in the temp_segments directory
def clear_temp_segments(directory):
    """Clear all files in the specified directory."""
    for filename in os.listdir(directory):
        file_path = os.path.join(directory, filename)
        try:
            if os.path.isfile(file_path):
                os.unlink(file_path)  # Remove the file
        except Exception as e:
            print(f"Failed to delete {file_path}. Reason: {e}")

# Prompt the user to select a video file to process from the 'media' folder
def select_video_file():
    """Prompt the user to select a video file to process from the 'media' folder."""
    
    
    # Get a list of all .mp4 files in the media folder
    video_files = [f for f in os.listdir(media_folder) if f.endswith('.mp4')]
    
    # Check if there are any video files in the folder
    if not video_files:
        print(Fore.RED + "No video files found in the 'media' folder.")
        exit()
    
    while True:
        # Print the video file options
        print(Fore.CYAN + "\nSelect the video file to process (enter 'q' to quit):")
        for idx, file in enumerate(video_files, start=1):
            print(Fore.YELLOW + f"{idx}. {file}")
        
        # Get user input
        user_input = input(Fore.CYAN + "\nEnter the number corresponding to your choice: ")
        
        # Handle 'q' input to quit
        if user_input.lower() == 'q':
            print(Fore.GREEN + "\nExiting program.\n")
            exit()
        
        # Validate if the input is a number and within range
        if user_input.isdigit():
            choice = int(user_input)
            if 1 <= choice <= len(video_files):
                # Return the selected file path
                return os.path.join(media_folder, video_files[choice - 1])
        
        # If invalid input, show an error message in red
        print(Fore.RED + "\nInvalid input. Please enter a number corresponding to a video file or 'q' to quit.")