
import face_recognition
import cv2
import numpy as np

DOWNSCALE_FRAME = 0.25


def face_detect(frame):
    # variable init .
    face_locations = []
    face_encodings = []
    # resize frame to 1/4 of original for more FPS
    frame = cv2.resize(frame, (0, 0), fx=DOWNSCALE_FRAME, fy=DOWNSCALE_FRAME)
    # face_recognition uses rgb encoding and opencv uses bgr
    rgb_frame = frame[:, :, ::-1]
    # Find all the faces and face encodings in the current frame of video
    # and resize the coordinates to corespond with the original frame size
    face_locations = np.multiply(face_recognition.face_locations(rgb_frame),int(1/DOWNSCALE_FRAME))
    # face_encodings is very slow. Maybe checking every n frames can be possible.
    # face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)

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


