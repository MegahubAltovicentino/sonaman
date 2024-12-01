# Hand Reader for Audio Control

This script uses the MediaPipe library to control audio via hand keypoint recognition. Output parameters are mapped to specific keypoint calculations, such as hand distance and distance between fingers and thumb. 

## How to run

Prepare virtual environment with libraries in requirements.txt (tested on MacOS). 

Run the following script: 

    $ hand_reader.py

## Parameters

As of Dec 1st, 2024, the following parameters are being calculated and can be sent via OSC (as `/params`): 

    self.params = {
        'p1': 0, # distance between thumb and index
        'p2': 0, # distance between thumb and middle
        'p3': 0, # distance between thumb and ring
        'p4': 0, # distance between thumb and pinky
        'p5': 0, # pinch 
        'p6': 0, # thumb-index, for 2nd hand to appear in frame
        'p7': 0, # thumb-middle, for 2nd hand
        'p8': 0, # thumb-ring, for 2nd hand
        'p9': 0, # thumb-pinky, for 2nd hand
        'p10': 0, # pinch for 2nd hand
        'p11': 0, # distance between both hands 
    }

## Resources

RGB color picker: https://rgbcolorpicker.com (note: OpenCV is BGR, so need to invert red and blue order).