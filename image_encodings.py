import face_recognition
import cv2
import os
import glob
import numpy as np
import sys
from colorama import Fore, Back, Style

class LoadEncodings:
    def __init__(self):
        self.known_face_encodings = []
        self.known_face_names = []
        self.loaded_filenames = set()

    def load_encoding_images(self, images_path):
        print(Style.RESET_ALL + "-----------------------------")
        print("Loading Encodings")
        print(Style.RESET_ALL + "-----------------------------")

        # Load Images
        images_path = glob.glob(os.path.join(images_path, "*.*"))
        print("-{} encoding images found-".format(len(images_path)))

        # Store image encoding and names
        print("-Extracting encodings-")
        for img_path in images_path:
            if img_path in self.loaded_filenames:
                continue  # Skip if the image has already been loaded
            img = cv2.imread(img_path)
            rgb_img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

            # Get the filename only from the initial file path.
            basename = os.path.basename(img_path)
            (filename, ext) = os.path.splitext(basename)

            # Get encoding
            existing_encodings = face_recognition.face_encodings(rgb_img)
            img_encoding = existing_encodings[0]
            
            # Store file name and file encoding
            self.known_face_encodings.append(img_encoding)
            self.known_face_names.append(filename)
            self.loaded_filenames.add(img_path) 

        # Create a dictionary with names and corresponding encodings
        encodings_dict = {name: encoding for name, encoding in zip(self.known_face_names, self.known_face_encodings)}
        # Save the dictionary to an Numpy file
        np.save('face_encodings.npy', encodings_dict)
        # Load Numpy file to display the dictionary
        loaded_encodings_dict = np.load('face_encodings.npy', allow_pickle=True).item()
        
        # Extra option using arguments
        if(len(sys.argv) == 2):
            print("Return the encodings")
            if(sys.argv[1] == "--encodings"):
                print(Style.RESET_ALL + "-----------------------------")
                print("Encodings:", loaded_encodings_dict)
                print(Style.RESET_ALL + "-----------------------------")
            print("Return the names")
            if(sys.argv[1] == "--names"):
                print(Style.RESET_ALL + "-----------------------------")
                print("Names:", [name for name, encoding in loaded_encodings_dict.items()])
                print(Style.RESET_ALL + "-----------------------------")

        print("-Encodings are loaded-")
        print(Style.RESET_ALL + "-----------------------------")

def main():
    # Create an instance of SimpleFacerec
    facerec = LoadEncodings()

    # Load encoding images from the directory
    facerec.load_encoding_images("images")

if __name__ == "__main__":
    main()

