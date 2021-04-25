import numpy as np
import cv2

cap = cv2.VideoCapture("motion_test.mp4")
params = {"maxCorners": 0, "qualityLevel": 0.02, "minDistance": 10, "blockSize": 1, "mask": None}
lk_params = {"winSize": (30,30), "maxLevel": 2, "criteria": (cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 0.03)}

color = (0, 255, 0)

ret, first_frame = cap.read()

prev_grey = cv2.cvtColor(first_frame, cv2.COLOR_BGR2GRAY)
prev  = cv2.goodFeaturesToTrack(prev_grey, **params)

out = cv2.VideoWriter("output.avi", cv2.VideoWriter_fourcc("D","I","V","X"), 24,(len(first_frame), len(first_frame[0])))


pause = False


j = 0
while(cap.isOpened()):
    if not pause:
        ret, frame = cap.read()

        greyscale = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        next_frame, status, error = cv2.calcOpticalFlowPyrLK(prev_grey, greyscale, prev, None, **lk_params)

        good_old = prev[status == 1]
        good_new = next_frame[status == 1]

        prev_grey = greyscale.copy()
        if ((j%20) == 0):
            prev = cv2.goodFeaturesToTrack(prev_grey, **params)
        else:
            prev = good_new.reshape(-1, 1, 2)
        
        j+=1

        mask = np.zeros_like(first_frame)

        for i, (new, old) in enumerate(zip(good_new, good_old)):
            a,b = new.ravel()
            c,d = old.ravel()

            mask = cv2.line(mask, (a,b), (c,d), color, 2)
            frame = cv2.circle(frame, (a,b), 3, color, -1)
        
        output = cv2.add(frame, mask)

        cv2.imshow("frame", output)
        out.write(output)

    key = cv2.waitKey(10) & 0xFF
    if(key == ord('q')):
        break
    elif(key == ord(' ')):
        pause = not pause

out.release()
cap.release()
cv2.destroyAllWindows()