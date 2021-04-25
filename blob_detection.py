import numpy as np
import cv2
import blob

def get_params():
    params = cv2.SimpleBlobDetector_Params()

    params.minThreshold = 10
    params.maxThreshold = 225


    params.filterByArea = True
    params.minArea = 100
    params.maxArea = 150000


    params.filterByCircularity = True
    params.minCircularity = 0.5


    params.filterByConvexity = False
    params.minConvexity = 0.2


    params.filterByInertia = False
    params.minInertiaRatio = 0.01

    return params

def get_detector():
    return cv2.SimpleBlobDetector.create(get_params())


detector = get_detector()

def find_blobs(frame):
    bordered = cv2.copyMakeBorder(frame, 5,5,5,5,cv2.BORDER_CONSTANT, None, [255,255,255])
    hsv = cv2.cvtColor(bordered,cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv, np.array([0,0,0]), np.array([359, 255, 80]))
    mask = cv2.bitwise_not(mask)
    keypoints = detector.detect(mask)

    blobs=[]
    for keypoint in keypoints:
        blobs.append(blob.create_blob_from_keypoint(keypoint))
    
    return blobs