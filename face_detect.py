import face_recognition
from EAR_measure import EAR_meas
# import EAR_measure
import cv2
import numpy as np
from draw_tool import draw_rect, draw_point, draw_lines,  draw_circle

DOWNSCALE_FRAME = 0.25 # todo could erase this, its done in EAR_measure


def face_detect(frame, reference_point):
    # resize frame to 1/4 of original for more FPS
    #frame_sized = cv2.resize(frame, (0, 0), fx=DOWNSCALE_FRAME, fy=DOWNSCALE_FRAME)
    # face_recognition uses rgb encoding and opencv uses bgr
    rgb_frame = frame[:, :, ::-1]
    # do main recognition
    ear, blink, nose_coordinates = EAR_meas(rgb_frame)
    # init output variable
    face_location = [] #todo erase this
    # assign variables if face is detected #TODO cleanup here
    if len(nose_coordinates) >= 1: # todo rewrite statement
       # corp_frame_sized, boundary = corp_preview(frame, nose_coordinates) #todo erase this
        center = nose_coordinates
    else:
        center = []
        corp_frame_sized = []
        blink = False

    reference_point = show_frame(frame, center, reference_point,
                                 blink)  # show picture with landmarks

    return center, face_location, reference_point


def center_of_face(position):
    (top, right, bottom, left) = position
    center_x = int((right + left) / 2)
    center_y = int((top + bottom) / 2)
    center = (center_x, center_y)
    return center


def face_corp(position, frame):
    (top, right, bottom, left) = position
    crop_img = frame[top:bottom, left:right]
    return crop_img


def show_frame(frame, center_face_position, reference_point, blink):
    if len(center_face_position) != 0:
        if len(reference_point) == 0:
            # Use first face frame as reference
            reference_point = center_face_position
            print("[STATE] Reference set as:", reference_point)

        # Marking in frame
        edited_frame = frame.copy()  # break link between edited_frame and frame
        edited_frame = draw_point(edited_frame, center_face_position, 0)  # mark face center point
        edited_frame = draw_point(edited_frame, reference_point, 1)  # mark face center point
        # todo  draw lines, still solving problem.. so its commented
        # edited_frame = draw_lines(edited_frame, reference_point, center_face_position)
        edited_frame = draw_circle(edited_frame, center_face_position, 100)

        # combine two frames - main preview & face preview
        #comp_frame = corner_matrix_combine(edited_frame, corp_frame_sized) todo erase
        # text about blink state
        if blink:
            blink_str = '!CLICK!'
        else:
            blink_str = ''

        cv2.putText(edited_frame, blink_str, (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

        # Display the resulting frame
        cv2.imshow('frame', edited_frame)
    else:
        cv2.imshow('frame', frame)
    return reference_point


def corner_matrix_combine(matA, matB): #todo erase this
    # Take matrix A and to its corned place matB
    # Use right bottom corner
    matA[len(matA) - len(matB):len(matA), len(matA[0]) - len(matB[0]):len(matA[0]), ::] = matB
    return matA


def corp_preview(frame, nose_coordinates): # todo erase this
    # preview of face - do corp of face from frame & resize it
    x_size, y_size, z_size = frame.shape    # create coordinates for rectangle corp preview
    prew_size = int(20/2)  #size of  preview in px
    boundary = [0,0,0,0]
    boundary[0] = nose_coordinates[0] - prew_size  # left
    boundary[1] = nose_coordinates[0] + prew_size  # right
    boundary[2] = nose_coordinates[1] - prew_size  # top
    boundary[3] = nose_coordinates[1] + prew_size  # bottom boundary

    if boundary[0] < 0:      boundary[0] = 0
    if boundary[1] > x_size: boundary[1] = x_size
    if boundary[2] < 0:      boundary[2] = 0
    if boundary[3] > y_size: boundary[3] = y_size

    corp_frame = face_corp([boundary[0], boundary[3], boundary[1], boundary[2]], frame)  # corp face boundary
    preview_height = 180  # fix preview window height
    preview_downscale = preview_height / prew_size*2  # downscaling factor
    corp_frame_sized = cv2.resize(corp_frame, (0, 0), fx=preview_downscale, fy=preview_downscale)  # resizing
    return corp_frame_sized, boundary
