
import face_recognition
import cv2
import numpy as np
from draw_tool import draw_rect, draw_point, draw_lines

DOWNSCALE_FRAME = 0.25


def face_detect(frame, reference_point):  #TODO reference point make as global
    # variable init .
    face_locations = []
    face_encodings = []
    # resize frame to 1/4 of original for more FPS
    frame_sized = cv2.resize(frame, (0, 0), fx=DOWNSCALE_FRAME, fy=DOWNSCALE_FRAME)
    # face_recognition uses rgb encoding and opencv uses bgr
    rgb_frame = frame_sized[:, :, ::-1]
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

    reference_point = show_frame(frame, center, face_location, reference_point) # show picture with landmarks

    return center, face_location, reference_point


def center_of_face(position):
    (top, right, bottom, left) = position
    center_x = int((right + left) / 2)
    center_y = int((top + bottom) / 2)
    center = (center_x, center_y)
    return center

def face_corp(position, frame):
    (top, right, bottom, left) = position
    width = right-left
    height = top - bottom
    crop_img = frame[top:bottom, left:right]
    return crop_img

def show_frame(frame, center_face_position, face_position,reference_point):
    if len(face_position) != 0:
        if len(reference_point) == 0:
            # Use first face frame as reference
            reference_point = center_face_position
            print("Reference set as:", reference_point)

        # Marking in frame
        edited_frame = draw_point(frame, center_face_position, 0)  # mark face center point
        edited_frame = draw_point(edited_frame, reference_point, 1)  # mark face center point
        edited_frame = draw_lines(edited_frame, reference_point, center_face_position)  # draw all lines
        edited_frame = draw_rect(edited_frame, face_position)  # mark face

        # Display the resulting frame
        cv2.imshow('frame', edited_frame)
    else:
        cv2.imshow('frame', frame)
    return reference_point  #TODO reference point as global!

