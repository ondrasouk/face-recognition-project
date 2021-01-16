import cv2
'''
Set of function for marking objects direct into frame
We used lot more of draw functions, but finally we need only these two:

-draw_point(frame, center, colorKey)
    used for marking center of face and reference point
-draw_circle(frame, center_coordinates, radius)
    used for face marking
'''

def draw_point(frame, center, colorKey):
    color = {0: (255, 255, 255),
             1: (255, 255, 0)}
    cv2.circle(frame, tuple(center), 1, color[colorKey], 4)
    return frame


def draw_circle(frame, center_coordinates, radius):
    frame = cv2.circle(frame, tuple(center_coordinates), radius, (0, 0, 255), 1)
    return frame
