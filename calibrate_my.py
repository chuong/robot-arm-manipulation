# -*- coding: utf-8 -*-
"""
Created on Fri Oct 01 11:06:53 2016

This script will provide the world coordinates of pins location to the robot, 
so the robot can grasp the pin.

# to check the accuracy, need to retake images by fixing the box and pins position,
also need to record relative robot coordinates

@author: yuboya
"""

import numpy as np
import cv2
from matplotlib import pylab as plt

from Calibration_final import Calibration_final
from LocatePin import LocatePins
from ImageToCamera import ImageToCamera
from PointsToRobot import PointsToRobot
    
[camera_matrix, dist_coefs] = Calibration_final()

    
#img_index = 9
img_index = 0
#img_index = 72
#img_index = 54 # one point missing
#img_index = 7

#pinim = cv2.imread('robot1.jpg') # for frame transformation

pinim = cv2.imread('show'+str(img_index)+'.jpg')
cv2.imshow('pin',pinim) # show mask image
cv2.waitKey(3)

# undistort
dst = cv2.undistort(pinim, camera_matrix, dist_coefs, None, camera_matrix)
#cv2.imshow('calibresult.jpg',dst) 
#cv2.waitKey(3)

# Our operations on the frame come here
hsv = cv2.cvtColor(dst, cv2.COLOR_BGR2HSV)

# Display the resulting frame
cv2.imshow('hsv',hsv)
cv2.waitKey(3)


## abstract red pixels   


## for pin detection
lower_red0 = np.array([0,113,118])  # define a lower boundary of red h,s,v
upper_red0 = np.array([9,132,139])  # define a upper boundary of red h,s,v
mask0 = cv2.inRange(hsv,lower_red0,upper_red0) 
cv2.imshow ('mask0',mask0)
cv2.waitKey(3)

# pin06: point6: (176.51 147.9 63.75) 175.022222222 66.3 86.7
lower_red1 = np.array([175,88,98])  # define a lower boundary of red h,s,v
upper_red1= np.array([179,175,142])  # define a upper boundary of red h,s,v
mask1 = cv2.inRange(hsv,lower_red1,upper_red1)
cv2.imshow ('mask1',mask1)
cv2.waitKey(3)

mask = mask0 + mask1 



# save all image pixels that are in the range between these boundaries to mask, these are red pixels but shown in white(255)
cv2.imshow('mask',mask) # show mask image
cv2.waitKey(3) # hold image for 3 millisecs

kernel_size = 3

# dilation: 3x3 square
#[[279.94581861394647, 111.42971488388372, 20.0], [242.23307517567358, 116.66777466790846, 20.0], [239.34081387245706, 77.742430803096724, 20.0]]

# closing(dilation,erosion)
#

pins, mask2 = LocatePins(kernel_size, mask)

print 'Position of pinheads in image frame:\n', pins

# from camera to table: 343-344mm
## from camera to robot finger: 15.8+15.4 =31.2
# from robot finger to table:3.2-3.3 pin red;  actually z=20mm in robot frame for manipulation
# from pin top to table:4.6

zc = -301
xyzc = ImageToCamera(zc, camera_matrix, pins)
print 'Position of pinheads in camera frame:\n', xyzc


### pins position to be sent to robot

# with already calculated relationship btw camera frame and robot frame
#alpha = 0.185336856481
#deltax = -240.127807845
#deltay = -100.568946542 
#deltaz = -364.0

#0.560742524377 192.976250048 307.334780811 364.0

alpha = 0.560742524377
deltax = 192.976250048
deltay = 307.334780811
deltaz = 364.0

pointrs = PointsToRobot(alpha, deltax,deltay,deltaz,xyzc)
print 'Position of pinheads in robot frame:\n',pointrs


# show detected position on original image, to see the accuracy of detection
plt.figure()
plt.subplot(1,2,2)
plt.imshow(pinim)
pinx = [pin[0] for pin in pins]
piny = [pin[1] for pin in pins]
plt.plot(piny, pinx, 'ro') # plt.plot(x coor, y coor)
plt.axis([0,640,480,0])
plt.grid(True)
plt.xlabel('y axis')
plt.ylabel('x axis')
plt.title('Original Image with Red Pins')
#plt.savefig('robot'+str(img_index)+'kernel'+str(kernel_size)+'.jpg') 

plt.subplot(1,2,1)
mask2[mask2<128] = 1
mask2[mask2>=128] = 0
plt.imshow(mask2,cmap='Greys') # show mask image
plt.xlabel('v axis')
plt.ylabel('u axis')
plt.title('Dilated Image: Found Pins')
#plt.savefig('robot'+str(img_index)+'kernel'+str(kernel_size)+'.jpg') 
plt.show()

