# movement_detector
## Mouse Movement detector for HealthHack Melbourne 2016
## Project Description

For this project, we were supplied some videos that show a mouse in a cage. Most of the video consists of uninteresting periods where the mouse is resting. The goal is to detect the interesting periods where the mouse is moving. This python script is designed to detect movement within a video using optical flow analysis from OpenCV.

## Usage

1. Install pythonopencv `sudo apt-get install python-opencv`
2. Run via `python opt_flow2.py <video.mp4>`

This will produce a <video.csv> output file consisting of 4 columns

`[Frame Number, Minute, Second, Maximum Displacement]`

Frame number - sequential order of the frame in the video
Minute, second - timepoint the frame corresponds to based on 25fps calculation
Maximum Displacement - metric describing the magnitude of the biggest displacement vector calculated in the frame




