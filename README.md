# Fall Detection Bot

This project is designed to detect falls using a custom model. Follow the instructions below to set up the environment and install the necessary dependencies.

# Script Details

**combined_fall_detection_model.py**: This script combines two approaches—YOLO-based fall detection and a pretrained model from Hugging Face—to identify falls in video footage with greater accuracy. First, the script uses YOLO to detect a potential fall by tracking changes in a person’s posture, particularly by observing if the bounding box around a person’s body shrinks, which can indicate a fall. If YOLO flags a possible fall, the script extracts a short video segment and processes it through a pretrained fall detection model from Hugging Face. This model further analyzes the segment to confirm the fall, providing a confidence score. The script outputs detected falls, along with their confidence scores, and keeps a running total of all confirmed falls in the video. This combined approach aims to improve the precision of fall detection by leveraging both object tracking and machine learning classification.

## Requirements

- **Miniconda** or **Anaconda** installed on your machine.

## Setup Instructions

1. **Create the Conda Environment**

   Open your terminal and create a new Conda environment with Python 3.10:

   ```bash
   conda create -n fallBot python=3.10
2. **Activate the Conda Environment**
    ```bash 
    conda activate fallBot
3. **Follow the steps in notify/README_notify.md file to signup for notifications (OPTIONAL)**
    
    
4. **Install requirements**
    ```bash
    pip install -r requirements.txt
5. **Run the Program**

      ```bash
      python combined_fall_detection_model.py
      ```
    