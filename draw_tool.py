import cv2
import numpy as np
from mouse_move import mouse_move


def draw_rect(frame, position):
    (top, right, bottom, left) = position
    color = (255, 0, 0)
    cv2.rectangle(frame, (left, top), (right, bottom), color, 1)
    return frame


def draw_point(frame, center, colorKey):
    color = {0: (255, 255, 255),
             1: (255, 255, 0)}
    cv2.circle(frame, center, 1, color[colorKey], 3)
    return frame


def draw_lines(frame, reference_point, center_face_position):
    # connect line
    frame = cv2.line(frame, reference_point, center_face_position, (0, 255, 255), 1)
    # x,y deviation  line
    x, y = reference_point
    xDev = center_face_position[0] - reference_point[0]  # x deviation
    yDev = center_face_position[1] - reference_point[1]  # y deviation
    xLinePoint = xDev + x
    yLinePoint = yDev + y
    frame = cv2.line(frame, reference_point, (xLinePoint, y), (0, 255, 0), 2)  # x dev. line
    frame = cv2.line(frame, reference_point, (x, yLinePoint), (0, 255, 0), 2)  # y dev. line
    # mouse_move(xDev,yDev,0.01)

    return frame
