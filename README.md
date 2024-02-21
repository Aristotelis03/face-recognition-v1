# face-recognition-v1

## A Python-based live face regonition system 

A tool designed to detect faces in real-time using the face-recognition and OpenCV (cv2) libraries. Consisting of three core files, including image_encodings.py, main.py, and compare_face.py, the system extracts facial features from a set of images, encodes them, and compares them with live camera input for identification purposes. The main.py file orchestrates the live camera feed, dynamic face comparison, interface and provides functionality the option to add new faces on-the-fly. Complemented by a repository of sample images and a face_encodings.npy file storing facial encodings, the system offers a robust solution for real-time face detection and recognition tasks.

## Features
### Face Recognition
<img width="475" alt="Sample" src="https://github.com/Aristotelis03/face-recognition-v1/assets/122119588/af9e2564-7d3e-40b6-85d0-0ff051eb7351">

### Data
The image_encoding.py script, in addition to creating the the face_encodings.npy file, can also return the names and the encodings using the following arguments. This helps te user keep track of their input.
```
python image_encodings --encodings
python image_encodings --names
```

### Capturing Faces While Using the Application
The face-recognition-v1 is capable of capturing faces in real-time as it's being used.

<img width="475" alt="Capture3" src="https://github.com/Aristotelis03/face-recognition-v1/assets/122119588/e4db1d26-05d2-4494-93e1-c2eb694b41a2">


## User Instructions
This is a complete guide on how to set up and use face-recognition-v1.

### Installation
To use this application, the installation of the libraries [OpenCV](https://pypi.org/project/opencv-python/) and [face-recognition](https://pypi.org/project/face-recognition/) is necessary.

The following commands install the libraries.
```
pip install --upgrade pip
pip install opencv-python
pip install face_recognition
```

### Images and encodings 
The first step is to add some faces to the Images folder. There are already some samples in this folder. The user can add their face in this folder or capture it later when the project is running.

The following command rewrites the encodings and the names in the face_encodings.npy file based on the files in the Image folder.
```
python image_encodings.py
```
### Execution
After the creation of the face_encodings.py file, the face-recognition-v1 is ready to use.
```
python main.py
```
### Usage 
The user can enable and disable the face recognition by clicking the application's window and pressing 'f' on the keyboard. If the image of the person in the camera was not in the image folder before running image_encodings, the displayed text will be 'Unknown'.

The user can capture the face in the camera by clicking on the window and pressing 'r' on the keyboard. the user will be prompted to enter a name which must not match any of the names in the list that will be displayed.

The program terminates by pressing 'q' or by closing the window


## Acknowledgments
This project implements some ideas from [Face Recognition In Real-Time With OpenCV And Python](https://pysource.com/2021/08/16/face-recognition-in-real-time-with-opencv-and-python/)

## Isues
