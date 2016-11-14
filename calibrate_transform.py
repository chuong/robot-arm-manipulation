# -*- coding: utf-8 -*-
"""
Created on Mon Oct 24 19:31:31 2016

This script is used to check the accuracy of points to be sent to robot
The locations of pins are obtained from the robot user interface,
the calculated pin position from the image will be used to compare 
with the known positions in robot frame

The image used here is 'robot1.jpg', need more sample images from robot!

@author: yuboya
"""

import numpy as np
import cv2
from matplotlib import pylab as plt

from Calibration_final import Calibration_final
from LocatePin import LocatePins
from TransformationCalculation import TransformationCalculation
from ImageToCamera import ImageToCamera
from PointsToRobot import PointsToRobot

[camera_matrix, dist_coefs] = Calibration_final()

img_index = 4

pinim = cv2.imread('transl'+str(img_index)+'.jpg') # for frame transformation

cv2.imshow('pin',pinim) # show mask image
cv2.waitKey(3)

# undistort
dst = cv2.undistort(pinim, camera_matrix, dist_coefs, None, camera_matrix)

#cv2.imwrite('calibresult.jpg',dst)  
cv2.imshow('calibresult.jpg',dst) 
cv2.waitKey(3)

# Our operations on the frame come here
hsv = cv2.cvtColor(dst, cv2.COLOR_BGR2HSV)

# Display the resulting frame
cv2.imshow('hsv',hsv)
cv2.waitKey(3)



## abstract red pixels   

## for robot point location
#176.016666667 127.5 86.7
#172.536111111 140.25 76.5
#174.525 84.15 84.15
#172.536111111 140.25 76.5

# 168.558333333 73.95 89.25
# 169.055555556 43.35 71.4

#169.055555556 40.8 130.05
#172.536111111 20.4 112.2
lower_red2 = np.array([162,20,58])  # define a lower boundary of red h,s,v
upper_red2= np.array([177,140,110])  # define a upper boundary of red h,s,v
mask = cv2.inRange(hsv,lower_red2,upper_red2)
cv2.imshow ('mask',mask)
cv2.waitKey(3)



# save all image pixels that are in the range between these boundaries to mask, these are red pixels but shown in white(255)
cv2.imshow('mask',mask) # show mask image

cv2.waitKey(3) # hold image for 3 millisecs

kernel_size = 3  # change to check accuracy

# dilation: 3x3 square 
# [[295.30639235815045, 0.87999753381752532, 20.0], [255.18988453808879, 57.185822915069835, 20.0]]
# 4 disk cosa= 0.99750164308 a= 0.070702162791
# [[299.26968609129403, 0.051720982473057203, 20.0], [252.61786726264, 52.856090732448251, 20.0]]
# 3 disk cosa= 0.995251396044 a= 0.0974922246005
# [[298.62925523995233, 0.13406196650118346, 20.0], [253.48606473430698, 53.950191342786987, 20.0]]
# 2 disk
# [[298.19273203172799, 0.20397432061006154, 20.0], [253.93053743165532, 54.557020027242885, 20.0]]
# cosa = 1
#[[300.0, 0.0, 20.0], [249.62664409508216, 49.376808403063215, 20.0]]

# >=5 disk
#alpha = math.acos(num/den) # in radians, degrees(alpha)= in degrees
#ValueError: math domain error >1 or <-1 ?????

# closing(dilation,erosion) 
#3 =1 =5
#[[294.43001767329497, 1.1477479356869853, 20.0], [255.50898867591528, 57.934400260985669, 20.0]]
#5
#[[294.43001767329497, 1.1477479356869853, 20.0], [255.50898867591528, 57.934400260985669, 20.0]]
#2 = 4
#[[294.43228735673364, 1.1472802457862781, 20.0], [255.51125835935397, 57.933932571084945, 20.0]]
pins, mask2 = LocatePins(kernel_size, mask)
print 'pins position in image frame:'
print pins

# from camera to table: 34.3-34.4
## from camera to robot finger: 15.8+15.4 =31.2
# from robot finger to table:3.2-3.3 pin red; 
# from pin top to table:4.6
zc = -344 # change to check accuracy

xyzc = ImageToCamera(zc, camera_matrix, pins)
print 'Position of pinheads in camera frame:\n', xyzc

[alpha, deltax,deltay,deltaz] = TransformationCalculation(xyzc)
print 'alpha, deltax,deltay,deltaz:'
print alpha, deltax,deltay,deltaz


pointrs = PointsToRobot(alpha, deltax,deltay,deltaz,xyzc)
print 'Position of pinheads in robot frame:\n',pointrs


# show detected position on original image, to see the accuracy of detection
plt.imshow(pinim)
pinx = [pin[0] for pin in pins]
piny = [pin[1] for pin in pins]
plt.plot(piny, pinx, 'ro') # plt.plot(x coor, y coor)
#plt.savefig('robot'+str(img_index)+'kernel'+str(kernel_size)+'.jpg') 
plt.show()
