import pyautogui as gui
import math
import time

# in percent of diameter of active range
RANGE_OF_INSENSITIVITY = 10
# scale of input movement
SCALE = 0.5
# when none face is detected continue movement for n seconds
TIME_TO_STOP = 0.5

"""
Set mouse position from actual position of cursor.
Move the cursor from previous position according to difference
of center face position and reference point.
"""
def mouse_move(reference_point, center_face_position):
    # to remember last move
    global mov_x
    global mov_y
    # initialize mouse position from actual mouse position
    if not('mouse_x' in globals()):
        global mouse_x
        global mouse_y
        global t
        mouse_x, mouse_y = gui.position()
        t = 0
    # block first few loops (between starting thread and first analyzed frame)
    if (len(reference_point) == 0):
        return
    # when no face is detected and reference point was set continue in movement
    if len(center_face_position) == 0:
        if t == 0:
            t = time.time()
        if (time.time() - t) >= TIME_TO_STOP:
            t = 0
            mov_x = 0.0
            mov_y = 0.0
        move(mov_x, mov_y)
        return
    t = 0
    dev_x = 0.0
    dev_y = 0.0
    dev_x = center_face_position[0] - reference_point[0]
    dev_y = center_face_position[1] - reference_point[1]
    if (dev_x**2+dev_y**2) >= (RANGE_OF_INSENSITIVITY**2):
        dev_d = 0.0
        dev_r = math.sqrt(dev_x**2 + dev_y**2) - RANGE_OF_INSENSITIVITY
        if dev_x != 0:
            dev_d = math.atan(dev_y/dev_x)
            if (dev_x < 0):
                dev_d += math.pi
        else:
            if dev_y > 0:
                dev_d = math.pi/2
            if dev_y < 0:
                dev_d = -math.pi/2
        mov_r = 0.1*dev_r + (0.05*dev_r)**2
        mov_x = mov_r * math.cos(dev_d)
        mov_y = mov_r * math.sin(dev_d)
        mov_x *= SCALE
        mov_y *= SCALE
        move(mov_x, mov_y)
    else:
        mov_x = 0.0
        mov_y = 0.0
    return


"""
Move the cursor from coordinates mouse_x, mouse_y (actual position of cursor)
by the distance x,y (input).
"""
def move(x, y):
    global mouse_x
    global mouse_y
    mouse_x += x
    mouse_y += y
    if gui.onScreen(mouse_x, mouse_y):
        gui.moveTo(mouse_x, mouse_y)
    else:
        if mouse_x < 0:
            mouse_x = 0.0
        if mouse_y < 0:
            mouse_y = 0.0
        dim = gui.size()
        if mouse_x > dim[0]:
            mouse_x = float(dim[0])
        if mouse_y > dim[1]:
            mouse_y = float(dim[1])
        gui.moveTo(mouse_x, mouse_y)
