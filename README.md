# Hand Reader for Audio Control

This script uses the MediaPipe library to control audio via hand keypoint recognition. Output parameters are mapped to specific keypoint calculations, such as hand distance and distance between fingers and thumb. 

## How to run

Prepare virtual environment with libraries in requirements.txt (tested on MacOS). 

Run the following script: 

    $ hand_reader.py

## Resources

RGB color picker: https://rgbcolorpicker.com (note: OpenCV is BGR, so need to invert red and blue order).