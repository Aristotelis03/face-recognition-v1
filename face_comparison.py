import face_recognition
import cv2
import os
import glob
import numpy as np

class FaceComparison:
    def __init__(self):
            self.known_face_encodings = []
            self.known_face_names = []
            self.loaded_filenames = set()

            # Resize frame for a faster speed
            self.frame_resizing = 0.25

            loaded_encodings_dict = np.load('face_encodings.npy', allow_pickle=True).item()
            for name, encoding in loaded_encodings_dict.items():
                # Compare the encoding with img_test and get the result
                self.known_face_encodings.append(encoding)

                # Assign the comparison result to the name in the results dictionary
                self.known_face_names.append(name)

    def compare_faces(self, frame):
        # Resize the image
        small_frame = cv2.resize(frame, (0, 0), fx=self.frame_resizing, fy=self.frame_resizing)
        # Convert the image from BGR color (which OpenCV uses) to RGB color
        rgb_small_frame = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)
        face_locations = face_recognition.face_locations(rgb_small_frame)
        face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)
        face_names = []
        for face_encoding in face_encodings:
            # See if the face is a match for the faces in the list
            matches = face_recognition.compare_faces(self.known_face_encodings, face_encoding)
            # Set default name to Unknown
            name = "Unknown"

            # Use the known face with the smallest distance to the new face
            face_distances = face_recognition.face_distance(self.known_face_encodings, face_encoding)
            best_match_index = np.argmin(face_distances)
            if matches[best_match_index]:
                name = self.known_face_names[best_match_index]
            face_names.append(name)

        # Convert to numpy array to adjust coordinates with frame resizing quickly
        face_locations = np.array(face_locations)
        face_locations = face_locations / self.frame_resizing
        return face_locations.astype(int), face_names

