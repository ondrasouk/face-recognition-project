import cv2
from face_detect import face_detect
from mouse_move import mouse_move
from faceRecognition import ear_init
import pyautogui
import threading
import time

# replace 60 with target refresh-rate (my monitor runs at 60fps)
MOUSE_MOVE_SLEEP = 1/60


# Repeating function in another thread for mouse_move
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

    # init reference point coordinates
    global reference_point
    global center_face_position
    center_face_position = []
    reference_point = []
    face_position = []
    left_b = False
    blink = False
    blink_prev = [False, False]
    t_blink = 0

    def mouse_move_wrap():
        mouse_move(reference_point, center_face_position)

    cam = cv2.VideoCapture(0)
    global cam_dim
    cam_dim = [cam.get(cv2.CAP_PROP_FRAME_WIDTH), cam.get(cv2.CAP_PROP_FRAME_HEIGHT)]

    # turn off failsafe (when True cursor hits top-left corner of the screen and program fails)
    pyautogui.FAILSAFE = False
    # turn off pause in pyautogui
    pyautogui.PAUSE = 0

    # init. of detector and predictor
    # used for blink detection
    ear_init()

    thread_mouse = PerpetualTimer(MOUSE_MOVE_SLEEP, mouse_move_wrap)
    # **UNCOMMENT** for enable mouse at  the beginning
    # thread_mouse.start()
    print('[INFO] Press E for mouse enable')

    # Control of mouse is disabled at the beginning
    mouse_enabled = False

    while True:
        # Capturing images
        ret, frame = cam.read()
        # Mirror webcam
        frame = cv2.flip(frame, 1)

        blink_prev[1] = blink_prev[0]
        blink_prev[0] = blink
        # proces frame
        center_face_position, reference_point, blink = face_detect(frame, reference_point)

        # mouse click
        if mouse_enabled and (blink or blink_prev[0]):
            if t_blink == 0:
                t_blink = time.time()
            if (time.time() - t_blink) > 0.3:
                if not(left_b):
                    print("[INFO] Left mouse button PRESSED")
                    pyautogui.mouseDown()
                    left_b = True
        if mouse_enabled and not(blink or blink_prev[0] or blink_prev[1]):
            t_blink = 0
            if left_b:
                print("[INFO] Left mouse button RELEASED")
                pyautogui.mouseUp()
                left_b = False

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
                    print("[STATE] Reference set as:", reference_point)
            # toggle mouse control enable on "E"
            if k == ord('e'):
                if mouse_enabled:
                    mouse_enabled = False
                    thread_mouse.cancel()
                    print('[STATE] Mouse control DISABLED')
                else:
                    mouse_enabled = True
                    thread_mouse.start()
                    print('[STATE] Mouse control ENABLED')

    # Release handle to the webcam
    thread_mouse.cancel()
    cam.release()
    cv2.destroyAllWindows()


