import cv2
from faceRecognition import find_faces
from draw_tool import draw_point, draw_circle


def face_detect(frame, reference_point):
    """
    Detect faces in frame, detect blinking.
    Declare coordinates of face.

    :return: face_coordinates = tuple(x,y), reference_point = tuple(x,y), blink = Boolean
    """

    # color model swap
    rgb_frame = frame[:, :, ::-1]
    # detect faces in frame
    ear, blink, face_coordinates = find_faces(rgb_frame)
    # assign variables if face is not detected
    if len(face_coordinates) < 1:  blink = False
    # show picture with landmarks
    reference_point = show_frame(frame, face_coordinates, reference_point, blink)
    return face_coordinates, reference_point, blink


def show_frame(frame, center_face_position, reference_point, blink):
    """
    Mark all markers to frame and show it in window
    :return: reference point
    """

    # check if any face is detected
    if len(center_face_position) != 0:
        # if there is no defined reference point
        if len(reference_point) == 0:
            # Use first face position as reference
            reference_point = center_face_position
            print("[STATE] First reference set as:", reference_point)

        # Marking in frame
        edited_frame = frame.copy()  # break link between edited_frame and frame
        edited_frame = draw_point(edited_frame, center_face_position, 0)     # mark face center point
        edited_frame = draw_point(edited_frame, reference_point, 1)          # mark face center point
        edited_frame = draw_circle(edited_frame, center_face_position, 100)  # draw circle around face

        # text about blink state
        if blink:
            blink_str = '!CLICK!'  # blinked
        else:
            blink_str = ''  # opened eyes

        cv2.putText(edited_frame, blink_str, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

        # Display the resulting frame
        cv2.imshow('frame', edited_frame)
    else:
        # display ordinary frame, if face is not detected
        cv2.imshow('frame', frame)
    return reference_point
