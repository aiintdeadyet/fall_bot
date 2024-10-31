# Fall Detection Bot

This project is designed to detect falls using a custom model. Follow the instructions below to set up the environment and install the necessary dependencies.

# Script Details

**yolo_fall_detection.py**: This script uses YOLO to identify bounding boxes around a person’s body. A fall is detected if the bounding box shrinks, which may indicate a change in posture due to a fall.

**pretrained_fall_detection_model.py**: This script leverages a pretrained fall detection model from Hugging Face. It splits the input video into two-second clips and classifies each clip to determine if a fall has occurred.

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
3. **Install requirements**
    ```bash
    pip install -r requirements.txt
4. **Run the Program**

    Choose one of the scripts below based on the detection method you wish to use:

    - **Run `pretrained_fall_detection_model` script**:
      ```bash
      python pretrained_fall_detection_model.py
      ```

    - **Run `yolo_fall_detection` script**:
      ```bash
      python yolo_fall_detection.py
      ```
    