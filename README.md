# HandVolumeChanger
A python application with which user can increase system volume using his or her hands


Description:

Tools and Technologies: Python 3.10,Numpy,OpenCV,MediaPipe,pyCaw

Working: The main idea behind this project is to enable user to increase/reduce the system volume using his/her hand.This will work only if the system has an inbuilt webcam or supports an external webcam.

OpenCV is used to capture the video of the hand and each frame is passed as input to the MediaPipe hands detector.Mediapipe detects the hand and draws connections between (21 points) of the palm. The length between index finger and thumb finger (point 4 and point 8) is calculated, interpolated using numpy and is passed as input 
to the pyCaw's Mastervolume function and accordingly system volume is increased or decreased.
