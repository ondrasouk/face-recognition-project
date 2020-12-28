import face_recognition
import cv2
import numpy as np
from face_detect import face_detect
from draw_tool import draw_rect, draw_point, draw_lines
from mouse_move import mouse_move

cam = cv2.VideoCapture(0)

# init reference point coordinates
reference_point = []

while True:
    # Capturing images
    ret, frame = cam.read()
    # Operations with frame
    # Detecting
    center_face_position, face_position = face_detect(frame)  # detect face position
    if len(face_position) != 0:
        if len(reference_point):
            # ToDo mouse movements
            pass
        else:  # Use first face frame as reference
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

    # Keystroke detect:
    k = cv2.waitKey(1)
    if k > 0:  # keystroke detected
        # quit on "Q"
        if k == ord('q'):
            break
        # new reference point on "R"
        if k == ord('r'):
            if len(center_face_position) != 0:
                reference_point = center_face_position
                print("Reference set as:", reference_point)

# Release handle to the webcam
cam.release()
cv2.destroyAllWindows()
