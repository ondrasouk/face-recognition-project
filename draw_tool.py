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
    cv2.circle(frame, tuple(center), 1, color[colorKey], 3)
    return frame


def draw_lines(frame, reference_point, center_face_position):
    # connect line
    center_face_position = list(center_face_position)
    frame = cv2.line(frame, reference_point, (center_face_position[0],center_face_position[1]), (0, 255, 255), 1)
    # **UNCOMMENT** for printing of deviation lines in x/y directions
    # # x,y deviation  line
    # x, y = reference_point
    # xDev = center_face_position[0] - reference_point[0]  # x deviation
    # yDev = center_face_position[1] - reference_point[1]  # y deviation
    # xLinePoint = xDev + x
    # yLinePoint = yDev + y
    # frame = cv2.line(frame, reference_point, (xLinePoint, y), (0, 255, 0), 2)  # x dev. line
    # frame = cv2.line(frame, reference_point, (x, yLinePoint), (0, 255, 0), 2)  # y dev. line
    # **UNCOMMENT_END**
    return frame


def draw_circle(frame, center_coordinates, radius):
    center_coordinates = tuple(center_coordinates)
    frame = cv2.circle(frame, center_coordinates, radius, (0, 0, 255), 1)
    return frame
