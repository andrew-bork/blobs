import cv2
import numpy as np
import blob_detection
import blob as BLOB

cap = cv2.VideoCapture("motion_test.mp4")


ret, first = cap.read()

old = blob_detection.find_blobs(first)

path = np.zeros_like(first)

while(cap.isOpened()):

    ret, frame = cap.read()

    blobs = blob_detection.find_blobs(frame)
    
    
    BLOB.find_change(old, blobs, None)

    for blob in blobs:
        l,r = blob.get_bounding_box_int()
        frame = cv2.rectangle(frame, l, r, blob.col, 3)

        if(blob.prev != None):
            path = cv2.line(path, blob.pos_int(), blob.prev.pos_int(), blob.col,1)
            l,r = blob.prev.get_bounding_box_int()
            frame = cv2.rectangle(frame, l, r, blob.prev.col, 3)

    frame = cv2.add(frame,path)

    old = blobs
     
    cv2.imshow("blobs", frame)
    key = cv2.waitKey(10) & 0xFF
    if(key == ord('q')):
        break
