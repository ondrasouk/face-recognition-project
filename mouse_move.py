import pyautogui as gui
import math
import time

MAX_SPEED_LINEAR = 10
# in percent of screen per second when there is no movement
RANGE_OF_INSENSITIVITY = 10
# in percent of diameter of active range
ACTIVE_RANGE_WIDTH = 100
# in percent of smaller dimension of bounding box
ACCELERATION = 0
# time constant
SCALE_X = 0.5
SCALE_Y = 0.5
# scale of output mouse movement
TIME_TO_STOP = 0.5
# when none face is detected continue movement for n seconds


def mouse_move(reference_point, center_face_position, cam_dim, t):
    global movX
    global movY
    if (len(reference_point) != 0):
        if len(center_face_position) == 0:
            if not('a' in globals()):
                global a
                a = 0
            else:
                a += 1
            if a >= int(TIME_TO_STOP/t):
                a = 0
                movX = 0
                movY = 0
            gui.move(movX, movY, 0)
            return 0
        dev = [0, 0]
        disp_dim = gui.size()
        dev[0] = center_face_position[0] - reference_point[0]
        dev[1] = center_face_position[1] - reference_point[1]
        if (dev[0]**2+dev[1]**2) >= (RANGE_OF_INSENSITIVITY**2):
            movX, movY = insensitivity(dev[0], dev[1])
            gui.move(movX, movY, 0)
        else:
            movX = 0
            movY = 0
        return 0


def insensitivity(x, y):
    x = 0.1*x
    y = 0.1*y
    return x, y
