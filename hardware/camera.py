# script to run a face recoognition on live camera feed 
# and return the live camera stream with recognized faces.
# based on the demo code in https://github.com/ageitgey/face_recognition

import face_recognition as fr
import cv2
import numpy as np
import os


# use Opencv Haar cascade face classification: different stages of weak classifiers using Haar features
# face_cascade=cv2.CascadeClassifier("haarcascade_frontalface_alt2.xml")
# ds_factor=0.6

# hold saved contacts from saved_faces folder
# name of saved contacts
known_person=[] 
# image of saved contacts
known_image=[]
# encoding object of saved contacts
known_face_encodings=[] 

# add all saved contacts from saved_faces folder
for file in os.listdir("saved_faces"):
    try:
        # add contact name (filename before the . e.g.james.jpg->james)
        known_person.append(file[:file.rfind('.')])
        # add contact image 
        file=os.path.join("saved_faces/", file)
        known_image = fr.load_image_file(file)
        # add face encoding
        known_face_encodings.append(fr.face_encodings(known_image)[0])
    except Exception as e:
        pass

# variables to save face recognition result
face_locations = []
face_encodings = []
face_names = []

# optimization: only run face recongnition every other frame
fr_frame = True

# camera class that takes in the current frame in live video stream and add facial recognition result
class FaceRecognitionCCTV():
    def __init__(self):

        # get camera feed from opencv, input: camera id from system
        self.video = cv2.VideoCapture(0)
    
    def __del__(self):
        self.video.release()

    def get_frame(self):

        # variables to save flag for unknown people alert
        unknown_alert = False

        success, image = self.video.read()

        # facial recognation on every other frame
        if fr_frame:

            # optimization: resize frame of video to 1/4 size for faster face recognition processing
            small_frame = cv2.resize(image, (0, 0), fx=0.25, fy=0.25)

            # BGR to RGB
            rgb_small_frame = small_frame[:, :, ::-1] # all backwards

            # face detection
            face_locations = fr.face_locations(rgb_small_frame)
            face_encoding = fr.face_encodings(rgb_small_frame, face_locations)

            # iterate through saved contacts to see if any of detected faces is known
            for encoding in face_encodings:
                # check if the known faces are in the current detected face
                matches = fr.compare_faces(known_face_encodings,encoding)
                name = 'Unknown'

                # pick the most similar known face to current face in case of multiple match
                face_distances = fr.face_distance(known_face_encodings,encoding)
                top_match = np.argmin(face_distances)

                # if most similar match is contained then update the name
                if matches[top_match]:
                    name = known_person[top_match]
                else:
                    # if exist detected face that does not match any known contact
                    unknown_alert = True
                
                # add name to result
                face_names.append(name)

            # update flag for facial recognition at the end of each frame
            fr_frame = not fr_frame
        
        # add facial recognition result to video feed
        for loc, name in zip(face_locations, face_names):
            # convert back to normal scale
            top = loc[0] * 4
            right = loc[1] * 4
            bottom = loc[2] * 4
            left = loc[3] * 4

            # draw bounding box
            cv2.rectangle(image, (left, top), (right,bottom), (0,0,255), 2)

            # draw name label
            cv2.rectangle(image, (left, bottom-35), (right, bottom),(255,255,255), cv2.FILLED)
            cv2.putText(image, name, (left + 10, bottom - 10), cv2.FONT_HERSHEY_DUPLEX, 1.0, (0, 0, 0), 1)

        # convert cv2 image to encode for video stream
        _, jpeg = cv2.imencode('.jpg', image)

        # return byte image stream and whether there are unknown faces
        return jpeg.tobytes(), unknown_alert