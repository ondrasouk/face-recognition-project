import face_recognition
import cv2
import numpy as np
from face_detect import face_detect
from draw_tool import draw_rect, draw_point, draw_lines
from mouse_move import mouse_move
import pyautogui
import threading
import time


class PerpetualTimer:

    def __init__(self, seconds, target):
        self._should_continue = False
        self.is_running = False
        self.seconds = seconds
        self.target = target
        self.thread = None

    def _handle_target(self):
        self.is_running = True
        self.target()
        self.is_running = False
        self._start_timer()

    def _start_timer(self):
        if self._should_continue:
            self.thread = threading.Timer(self.seconds, self._handle_target)
            self.thread.start()

    def start(self):
        if not self._should_continue and not self.is_running:
            self._should_continue = True
            self._start_timer()

    def cancel(self):
        if self.thread is not None:
            self._should_continue = False
            self.thread.cancel()


if __name__ == '__main__':
    
    def mouse_move_wrap():
        mouse_move(reference_point, center_face_position, cam_dim)

    cam = cv2.VideoCapture(0)
    global cam_dim
    cam_dim = [cam.get(cv2.CAP_PROP_FRAME_WIDTH), cam.get(cv2.CAP_PROP_FRAME_HEIGHT)]

    # init reference point coordinates
    global reference_point
    global center_face_position
    center_face_position = []
    reference_point = []

    # turn off failsafe (when True cursor hits top-left corner of the screen and program fails)
    pyautogui.FAILSAFE = False

    t = PerpetualTimer(0.01, mouse_move_wrap)
    t.start()

    while True:
        # Capturing images
        ret, frame = cam.read()
        # Mirror webcam
        frame = cv2.flip(frame, 1)
        # Detecting
        center_face_position, face_position = face_detect(frame)  # detect face position
        if len(face_position) != 0:
            if len(reference_point):
                # mouse_move(reference_point, center_face_position, cam_dim)
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
    t.cancel()
    cam.release()
    cv2.destroyAllWindows()


