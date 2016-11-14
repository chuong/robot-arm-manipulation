# -*- coding: utf-8 -*-
"""
Created on Fri Sep 23 11:56:43 2016

@author: yuboya
"""

import cv2

# number of images to capture
cap = cv2.VideoCapture(0)
i=0

while(True):
    # Capture frame-by-frame
    ret, frame = cap.read()

    # Our operations on the frame come here
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    
    # Display the resulting frame
    cv2.imshow('frame',frame)
    cv2.imshow('hsv',hsv)
    key = cv2.waitKey(1) & 0xFF
    if key == ord('q'):
        break
    elif key == ord('s'):
        cv2.imwrite('show'+str(i)+'.jpg' ,frame)
        i=i+1
        


# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()
