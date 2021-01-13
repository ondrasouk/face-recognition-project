import pyautogui as gui
import math

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


def mouse_move(reference_point, center_face_position, cam_dim):
    if len(reference_point):
        dev = [0, 0]
        disp_dim = gui.size()
        dev[0] = center_face_position[0] - reference_point[0]
        dev[1] = center_face_position[1] - reference_point[1]
        if (dev[0]**2+dev[1]**2) >= (RANGE_OF_INSENSITIVITY**2):
            movX, movY = insensitivity(dev[0], dev[1])
            gui.moveRel(movX, movY, 0)
        return 0


def insensitivity(x, y):
    x = 0.2*x
    y = 0.2*y
    return x, y
