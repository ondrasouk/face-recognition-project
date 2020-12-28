import face_recognition
import cv2
import numpy as np


def face_detect(frame):
    # variable init .
    face_locations = []
    face_encodings = []
    frame = np.array(frame)

    # Find all the faces and face encodings in the current frame of video
    face_locations = face_recognition.face_locations(frame)
    face_encodings = face_recognition.face_encodings(frame, face_locations)
    if len(face_locations) == 1:
        for face_position in face_locations:
            print(face_position)
            print(type(face_position))
            center = center_of_face(face_position)
    else:
        center = []
        face_locations = []
    return center, face_locations


def center_of_face(position):
    (top, right, bottom, left) = position
    center_x = int((right + left) / 2)
    center_y = int((top + bottom) / 2)
    center = (center_x, center_y)
    return center


