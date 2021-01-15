import face_recognition
from EAR_measure import EAR_meas
# import EAR_measure
import cv2
import numpy as np
from draw_tool import draw_rect, draw_point, draw_lines

DOWNSCALE_FRAME = 0.25


def face_detect(frame, reference_point):
    # resize frame to 1/4 of original for more FPS
    frame_sized = cv2.resize(frame, (0, 0), fx=DOWNSCALE_FRAME, fy=DOWNSCALE_FRAME)
    # face_recognition uses rgb encoding and opencv uses bgr
    rgb_frame = frame_sized[:, :, ::-1]
    # locate faces in frame
    face_locations = np.multiply(face_recognition.face_locations(rgb_frame), int(1 / DOWNSCALE_FRAME))

    if len(face_locations) == 1:
        face_location = face_locations[0]
        center = center_of_face(face_location)
    else:
        center = []
        face_location = []

    reference_point = show_frame(frame, center, face_location, reference_point)  # show picture with landmarks

    return center, face_location, reference_point


def center_of_face(position):
    (top, right, bottom, left) = position
    center_x = int((right + left) / 2)
    center_y = int((top + bottom) / 2)
    center = (center_x, center_y)
    return center


def face_corp(position, frame):
    (top, right, bottom, left) = position
    width = right - left
    height = top - bottom
    crop_img = frame[top:bottom, left:right]
    return crop_img


def show_frame(frame, center_face_position, face_position, reference_point):
    if len(face_position) != 0:
        if len(reference_point) == 0:
            # Use first face frame as reference
            reference_point = center_face_position
            print("[State] Reference set as:", reference_point)

        # Marking in frame
        edited_frame = frame.copy() # break link between edited_frame and frame
        edited_frame = draw_point(edited_frame, center_face_position, 0) # mark face center point
        edited_frame = draw_point(edited_frame, reference_point, 1)  # mark face center point
        edited_frame = draw_lines(edited_frame, reference_point, center_face_position)  # draw all lines
        edited_frame = draw_rect(edited_frame, face_position)  # mark face

        # preview of face - do corp of face from frame & resize it
        corp_frame = face_corp(face_position, frame)  # corp face boundary
        corp_height, corp_width = tuple(corp_frame.shape[1::-1])
        preview_height = 180  # fix preview window height
        preview_downscale = preview_height / corp_height  # downscaling factor
        corp_frame_sized = cv2.resize(corp_frame, (0, 0), fx=preview_downscale, fy=preview_downscale)  # resizing
        # do EAR measuring rutine
        EAR, blink = EAR_meas(corp_frame_sized)
        # combine two frames - main preview & face preview
        comp_frame = corner_matrix_combine(edited_frame, corp_frame_sized)
        # text about blink state
        if blink == True:
            blinkStr = '!CLICK!'
        else:
            blinkStr = ''

        cv2.putText(comp_frame, blinkStr, (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

        # Display the resulting frame
        cv2.imshow('frame', comp_frame)
    else:
        cv2.imshow('frame', frame)
    return reference_point


def corner_matrix_combine(matA, matB):
    # Take matrix A and to its corned place matB
    # Use right bottom corner
    matA[len(matA)-len(matB):len(matA), len(matA[0])-len(matB[0]):len(matA[0]), ::] = matB
    return matA
