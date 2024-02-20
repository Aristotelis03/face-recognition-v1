import os
import cv2
from face_comparison import FaceComparison
from image_encodings import LoadEncodings
import time
import face_recognition
from colorama import Fore, Back, Style

print(Style.RESET_ALL + "-----------------------------")
print("Face recognition t1")
print(Style.RESET_ALL + "-----------------------------")

# Load camera
cap = cv2.VideoCapture(0)

# Set frame rate (e.g., 30 frames per second)
# cap.set(cv2.CAP_PROP_FRAME_WIDTH, 400)
# cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 400)

# Load face comparison faces
face_rec = FaceComparison( )

# Boolean virables
enable_face_recognition = False
enable_capture = False

# Capture image
def capture_face(ret, frame):
    global face_rec    
    if ret:
        print("Face Capturing ")
        print(Style.RESET_ALL + "-----------------------------")
        print("Known names: ",face_rec.known_face_names)
        # Get input for the new name
        name = input('Name: ')
        
        # Check if the name exists
        if name in face_rec.known_face_names:
            print(Style.RESET_ALL + "-----------------------------")
            print("*Name already exists")
            print(Fore.RED + "*Capture terminated*")
            print(Style.RESET_ALL + "-----------------------------")
            return -1
        
        # Get the frame encodings to check if it already exists
        rgb_img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        img_encoding = face_recognition.face_encodings(rgb_img)[0]
        face_exists = False   
        # Check if the captured face is already recorded
        for encoding in face_rec.known_face_encodings:
            result = face_recognition.compare_faces([encoding], img_encoding)
            # print(face_recognition.compare_faces([encoding], img_encoding))
            if result == [True]:
                print(Style.RESET_ALL + "-----------------------------")
                print("*Face encoding already exists*")
                print(Fore.RED + "*Capture terminated*")
                face_exists = True
                print(Style.RESET_ALL + "-----------------------------")
             
        if not face_exists:
            # Create a new file
            print(Style.RESET_ALL + "-----------------------------")
            print("*New face detected*")
            filename = name + ".jpg"
            directory_path = "images/"
            file_path = os.path.join(directory_path, filename)
            cv2.imwrite(file_path, frame)
            print(Fore.GREEN + "*New face added*")
            # Load encodings
            load_encodings = LoadEncodings( )
            load_encodings.load_encoding_images("images")
            # Load new  encodings in the face_rec  
            face_rec = FaceComparison( )
    return 0


# Tracking variables

# Face recognition frequency in frames (Disabled)
face_recognition_frequency = 5
frame_counter = 0
# Used for frames display
pTime = 0

while True:
    ret, frame = cap.read()
    frame_height, frame_width, _ = frame.shape

    # Count fps
    cTime = time.time()
    fps = 1/(cTime-pTime)
    pTime = cTime

    frame_counter += 1
    # Flip the image
    frame = cv2.flip(frame, 1)

    # Display fps
    cv2.putText(frame, f'FPS: {int(fps)}', (20,70), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 200), 2)
    
    # Display title
    text= "Facial Recognition System"
    text_size, _ = cv2.getTextSize(text, cv2.FONT_HERSHEY_SIMPLEX, 0.6, 2)
    text_x = int((frame_width - text_size[0]) / 2)
    text_y = int((frame_height + text_size[1]) / 2)
    cv2.putText(frame, text, (text_x, 25), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 200), 2)

    # Face recognition on/off indication
    if enable_face_recognition: 
        cv2.putText(frame, "FR: ON", (20,110), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 200), 2)
    else:
        cv2.putText(frame, "FR: OFF", (20,110), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 200), 2)
    
    # Face recognition
    # if enable_face_recognition and frame_counter % face_recognition_frequency == 0:
    if enable_face_recognition:
        # Compare the current frame with the face in the face_encodings.npy
        face_locations , face_names = face_rec.compare_faces(frame)
        for face_loc, name in zip(face_locations,face_names):
            # Pass the face encondings in variables
            y1, x2, y2, x1 = face_loc[0], face_loc[1], face_loc[2], face_loc[3] 
            # Display the name
            cv2.putText(frame, name, (x1, y2 + 20), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 200), 2)
            # Draw the rectangle around the face 
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 200), 2)
        
        # Reset frame counter
        frame_counter = 0

    # Display everything in the window 
    cv2.imshow("Frame", frame)

    key = cv2.waitKey(1) & 0xFF 

    if key == ord('q'):  # Press 'q' to quit
        print(Fore.RED + "Terminating")
        print(Style.RESET_ALL + "-----------------------------")
        break
    elif key == ord('f'):  # Press 'f' to enable face recognition
        enable_face_recognition = not enable_face_recognition  # Toggle the flag
        if enable_face_recognition:
            print(Fore.WHITE +"Face recognition: " + Fore.GREEN +"ON")
            print(Style.RESET_ALL + "-----------------------------")

        else:
            print(Fore.WHITE + "Face recognition: " + Fore.RED + "OFF")
            print(Style.RESET_ALL + "-----------------------------")
    
    if key == ord('r'):  # Press 'r' to to capture unknown face 
        enable_capture = True
        capture_face(ret, frame)

    # Check for the window close event
    if cv2.getWindowProperty("Frame", cv2.WND_PROP_VISIBLE) < 1:
        print(Fore.RED + "Terminating")
        print(Style.RESET_ALL + "-----------------------------")
        break
  
cap.release()
cv2.destroyAllWindows()
