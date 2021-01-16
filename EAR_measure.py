from scipy.spatial import distance as dist
from imutils import face_utils
import imutils
import dlib
import cv2


def EAR_meas(frame):
    '''
    From imput frame detect eyes landmarks, then compute eye-aspect-ratio
    Treshold EAR for closed eyes = 0.25
    EAR is computed as average EAR of each eye
    :return: EAR = float, blink = Boolean
    '''
    # Lower EAR than EAR_treshold means that eyes are closed
    EAR_treshold = 0.22

    # check if inited, if not init
    if not ('detector' in globals()):
        global detector
        global predictor
        print("[STATE] Detector, predictor init while  running")
        detector = dlib.get_frontal_face_detector()
        predictor = dlib.shape_predictor('shape_predictor_68_face_landmarks.dat')
    # resize for faster code
    frame = imutils.resize(frame, width=120)

    # transfer to grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # detect faces in the grayscale frame
    rects = detector(gray, 0)
    # grab the indexes of the facial landmarks for the left and
    # right eye, respectively
    (lStart, lEnd) = [42, 48]
    (rStart, rEnd) = [36, 42]
    # TODO maybe can use nose landmak  for  mouse movements

    # init outtput variables
    avg_ear = 1
    blink = False
    # loop over the face detections
    for rect in rects:
        # determine the facial landmarks for the face region, then
        # convert the facial landmark (x, y)-coordinates to a NumPy
        # array
        shape = predictor(gray, rect)
        shape = face_utils.shape_to_np(shape)

        # extract the left and right eye coordinates, then use the
        # coordinates to compute the eye aspect ratio for both eyes
        leftEye = shape[lStart:lEnd]
        rightEye = shape[rStart:rEnd]
        leftEAR = eye_aspect_ratio(leftEye)
        rightEAR = eye_aspect_ratio(rightEye)

        # average the eye aspect ratio together for both eyes
        avg_ear = (leftEAR + rightEAR) / 2.0

        # check to see if the eye aspect ratio is below the blink
        # threshold, and if so, increment the blink frame counter

        if avg_ear < EAR_treshold:
            # Blink detected
            blink = True
        else:
            # Opened eyes
            blink = False
            # for later use (right click, click and hold...)
    return avg_ear, blink


def ear_init():
    global detector
    global predictor
    print("[STATE] Detector, predictor init.")
    detector = dlib.get_frontal_face_detector()
    predictor = dlib.shape_predictor('shape_predictor_68_face_landmarks.dat')


def eye_aspect_ratio(eye):
    # compute the euclidean distances between the two sets of
    # vertical eye landmarks (x, y)-coordinates
    A = dist.euclidean(eye[1], eye[5])
    B = dist.euclidean(eye[2], eye[4])

    # compute the euclidean distance between the horizontal
    # eye landmark (x, y)-coordinates
    C = dist.euclidean(eye[0], eye[3])

    # compute the eye aspect ratio
    ear = (A + B) / (2.0 * C)

    # return the eye aspect ratio
    return ear
