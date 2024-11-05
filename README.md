# Fall Detection Bot

This project is designed to detect falls using a custom model. Follow the instructions below to set up the environment and install the necessary dependencies.

# Script Details

**yolo_fall_detection.py**: This script uses YOLO to identify bounding boxes around a person’s body. A fall is detected if the bounding box shrinks, which may indicate a change in posture due to a fall.

**pretrained_fall_detection_model.py**: This script leverages a pretrained fall detection model from Hugging Face. It splits the input video into two-second clips and classifies each clip to determine if a fall has occurred.

**combined_fall_detection_model.py**: This script integrates the functionality of both the yolo_fall_detection.py and pretrained_fall_detection_model.py scripts into a single program. First, it utilizes YOLO to detect potential falls by identifying if a person’s torso size decreases, indicating a possible fall. If a fall is suspected, the script clips the video segment and passes it through a pretrained model from Hugging Face to confirm the fall and provide a confidence score. It then outputs all detected falls along with the total count.

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
    - **Run `combined_fall_detection_model` script**:
      ```bash
      python combined_fall_detection_model.py
      ```
    