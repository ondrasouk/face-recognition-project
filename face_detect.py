import face_recognition
import cv2
import numpy as np


def face_detect(frame):
    # variable init .
    face_locations = []
    face_encodings = []
    frame = np.array(frame)
    #frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
    # Find all the faces and face encodings in the current frame of video
    face_locations = face_recognition.face_locations(frame)
    face_encodings = face_recognition.face_encodings(frame, face_locations)

    if len(face_locations) == 1:
        face_location = face_locations[0]
        center = center_of_face(face_location)
    else:
        center = []
        face_location = []
    return center, face_location


def center_of_face(position):
    (top, right, bottom, left) = position
    center_x = int((right + left) / 2)
    center_y = int((top + bottom) / 2)
    center = (center_x, center_y)
    return center


