# -*- coding: utf-8 -*-
"""
Created on Tue Nov 15 17:41:49 2016

@author: yuboya
"""

This is the instruction for using the code to locate the pins and move the Dobot.
2 interfaces are used to achieve the goal. 
"calibrate_my" for vision localization of the pin from input image "pinr73.jpg",
"interface" for control robot movement to grab the pin.

How to use "calibrate_my" :
    
1. Prepare: taking image of pin tray from "cv2vedio.py"
	1.1 Change COM number in cap = cv2.VideoCapture(0), 
	1.2 Type s to capture image, type q to exist program
	1.3 Modify the name of image as you like

2. Run "calibrate_my":
	2.1 "Calibration_final" will do camera calibraiton and output camera intrinsic matrix
	2.1 Choose the image you saved from preparation by changing the image name in :pinim = cv2.imread('show'+str(img_index)+'.jpg')
	2.2 Modify the HSV range to adapt to the pinhead colour in your image. 
		Note: you can use the software "GIMP" to find the HSV value of pinhead, and use calculateHSV.py to transfer HSV from (360degrees, 100%,100%) to pyhton HSV value.
	2.3 Change the kernel size based on the size of pinhead. same size performs better and have higher accuracy.
	2.4 "zc" is the height from camera(image plane) to pinhead, change "zc" in mm to your actual height.
	2.5 Run "calibrate_transform" to get transformation parameters from camera frame to robot frame:
         2.5.1 The provided image is "transl6", you can choose to use your image with 2 known points in both camera frame and robot frame
         2.5.2 in "TransformationCalculation.py", Change the positions of 2 point in robot frame by changing "xr1, yr1,zr1, xr2, yr2, zr2"
                 ,copy the calculation result "alpha, deltax,deltay,deltaz" to "calibrate_my"
    2.6 If you only use the provided image, skip step 2.5, else: run "calibrate_my.py" again, and you will get the pinhead positions in robot frame

3. Run "interface.py":
    3.1 Change the point positions, 
        for example: in "dobot_interface.send_absolute_position(220, 210, 20, 20, 3)", the input is (x, y, z, opening angle of gripper, pause time after sending command)
    3.2 Change i for cycles of picking pins, put in another position, go back. 
    3.3 You can change the initialization position to another position, with 45 degrees of joint angle 1 and 2, high accuracy can be attained.
Noted: This code can be modified to automatically get the pinhead postition from "calibrate_my", so that it can move to another pinhead position in next cycle.