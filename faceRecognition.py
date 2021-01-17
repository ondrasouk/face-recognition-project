from scipy.spatial import distance as dist
from imutils import face_utils
import dlib
import cv2


def find_faces(frame):
    """
    Algorithm detecting faces and take location of each landmark
        Than compute center of face (landmark #30),
        detect eyes landmarks, then compute eye-aspect-ratio (closing eyes sensing)

    Threshold EAR for closed eyes = 0.22
    EAR is computed as average EAR of each eye

    :return: avg_ear = float, blink = Boolean, nose_pos = tuple(1x2)
    """

    # Lower EAR than EAR_threshold means that eyes are closed
    ear_treshold = 0.22

    # check if inited, if not init
    if not ('detector' in globals()):
        global detector
        global predictor
        print("[STATE] Detector, predictor initialized while  running")
        detector = dlib.get_frontal_face_detector()
        predictor = dlib.shape_predictor('shape_predictor_68_face_landmarks.dat')

    # resize for faster code
    # for webcam you can use full size resolution
    # frame = imutils.resize(frame, width=450)

    # transfer to grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # detect faces in the grayscale frame
    rects = detector(gray, 0)
    # grab the indexes of the facial landmarks for the left and
    # right eye, respectively
    (lStart, lEnd) = [42, 48]
    (rStart, rEnd) = [36, 42]
    nose_landmark = 30  # index of root of nose (center of face)

    # init output variables
    avg_ear = 1
    blink = False
    nose_pos = []
    # loop over the face detections
    for rect in rects:
        # determine the facial landmarks in the face
        shape = predictor(gray, rect)
        shape = face_utils.shape_to_np(shape)  # convert to NumPy array
        
        # get coordinates for nose landmark
        nose_pos = shape[nose_landmark] 
        # extract the left and right eye coordinates, then use the
        # coordinates to compute the eye aspect ratio for both eyes
        left_eye = shape[lStart:lEnd]
        right_eye = shape[rStart:rEnd]
        left_ear = eye_aspect_ratio(left_eye)
        right_ear = eye_aspect_ratio(right_eye)

        # average EAR for both eyes
        avg_ear = (left_ear + right_ear) / 2.0

        if avg_ear < ear_treshold:
            # Blink detected
            blink = True
        else:
            # Opened eyes
            blink = False
    return avg_ear, blink, nose_pos


def ear_init():
    """
    Initialization of predictor and detector.
    Need to be init before start to prevent lag.
    :return: NONE
    """

    # make detector and predictor as global
    # so could not be initialized every cycle
    global detector
    global predictor
    # print info message
    print("[STATE] Detector, predictor initialized.")
    # init face detector
    detector = dlib.get_frontal_face_detector()
    # init shape predictor
    # uses pre-learned faces database with landmarks
    predictor = dlib.shape_predictor('shape_predictor_68_face_landmarks.dat')


def eye_aspect_ratio(eye):
    """
    compute the euclidean distances between the two sets of
    vertical eye landmarks (x, y)-coordinates
    """

    A = dist.euclidean(eye[1], eye[5])
    B = dist.euclidean(eye[2], eye[4])

    # compute the euclidean distance between the horizontal
    # eye landmark (x, y)-coordinates
    C = dist.euclidean(eye[0], eye[3])

    # compute the eye aspect ratio
    ear = (A + B) / (2.0 * C)

    # return the eye aspect ratio
    return ear
