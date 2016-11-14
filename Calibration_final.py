
"""

Calibration before dealing with images 

@author: yuboya
"""


import numpy as np
import cv2

def Calibration_final():
    # prepare object points, like (0,0,0), (1,0,0), (2,0,0) ....,(6,5,0)
    square_size = 37 # 37mm
    pattern_size = (9, 6)
    objp = np.zeros((np.prod(pattern_size),3), np.float32)
    objp[:,:2] = np.indices(pattern_size).T.reshape(-1,2)
    objp *= square_size
    
    # Arrays to store object points and image points from all the images.
    objpoints = [] # object points： 3D real world points
    imgpoints = []
    
    images = ['chessboard1.jpg','chessboard2.jpg','chessboard3.jpg','chessboard4.jpg',\
    'chessboard5.jpg','chessboard6.jpg','chessboard7.jpg','chessboard8.jpg','chessboard9.jpg',\
    'chessboard10.jpg','chessboard11.jpg','chessboard12.jpg','chessboard13.jpg','chessboard14.jpg',\
    'chessboard15.jpg','chessboard16.jpg','chessboard17.jpg','chessboard18.jpg','chessboard19.jpg',\
    'chessboard20.jpg','chessboard21.jpg','chessboard22.jpg','chessboard23.jpg','chessboard24.jpg',\
    'chessboard25.jpg','chessboard26.jpg']
    
    for fname in images:
    
#        print "Finding chessboard corners in image %s" %fname
        img = cv2.imread(fname)
        image_size = (img.shape[1], img.shape[0])
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
        # Find the chess board corners
        ret, corners = cv2.findChessboardCorners(gray, (9,6),None)

        # If found, add object points, image points (after refining them)
        if ret:
            objpoints.append(objp)
    		
    	  # termination criteria
            criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)
    
            #cornerSubPix: increase the accuracy of the corners we found
            #Refines the corner locations
            cv2.cornerSubPix (gray, corners,(11,11),(-1,-1), criteria)
            imgpoints.append(corners.reshape(-1,2))

            # Draw and display the corners
            cv2.drawChessboardCorners(img, (9,6), corners, ret)

    
        else:
            print('Cannot find chessboard')
    
    flags = cv2.CALIB_FIX_PRINCIPAL_POINT + cv2.CALIB_FIX_ASPECT_RATIO + cv2.CALIB_ZERO_TANGENT_DIST +cv2.CALIB_FIX_K3
    ret, camera_matrix, dist_coefs, rvecs, tvecs = cv2.calibrateCamera(objpoints, imgpoints, image_size,flags=flags)
    print "RMS:", ret
    print "camera matrix:\n", camera_matrix
    print "distortion coefficients: ", dist_coefs.ravel()
    
    return camera_matrix, dist_coefs

