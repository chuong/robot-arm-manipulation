# -*- coding: utf-8 -*-
"""
@author: yuboya
"""

import numpy as np
import cv2
from scipy import ndimage
import math
from skimage.morphology import disk

def LocatePins(kernel_size, mask):
    kernel = disk(kernel_size) # circular structuring element
#    print('Kernel Size = %s' %str(kernel_size)) 
#    print('Kernel: \n%s' %str(kernel))
    # optical kernel size =3
    # ks =4:
#     [[0 0 0 0 1 0 0 0 0]
#     [0 0 1 1 1 1 1 0 0]
#     [0 1 1 1 1 1 1 1 0]
#     [0 1 1 1 1 1 1 1 0]
#     [1 1 1 1 1 1 1 1 1]
#     [0 1 1 1 1 1 1 1 0]
#     [0 1 1 1 1 1 1 1 0]
#     [0 0 1 1 1 1 1 0 0]
#     [0 0 0 0 1 0 0 0 0]]    
    
    #kernel = np.ones((kernel_size,kernel_size),np.uint8) 
    #    mask1 = cv2.erode(mask,kernel) # erode noise with kernel_red
    #    cv2.imshow('mask1',mask1) # show mask image
    #cv2.waitKey(3) # hold image for 3 secs    

# worse than only dilation
#    mask2 = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
#    
#    cv2.imshow('mask_closing', mask2) # show mask image
#    cv2.waitKey(3) # hold image for 3 millisecs    
    
    
    mask2 = cv2.dilate(mask,kernel)
    
    cv2.imshow('mask_dilated', mask2) # show mask image
    cv2.waitKey(3) # hold image for 3 millisecs
    
    
    row = mask2.shape[0]  
    col = mask2.shape[1]
    

    points = [] # white point location in x,y coordinates
    pins = []
    pinsn = []
    ave = 0
    crop_size = 30  #35 is better than 30, 30 may cause multiple pixels detected for 1 pin, for pin7
    #print ('image size %s' %str([row,col])) # [480, 640]
    
    for u in range(0, row+crop_size, 2*crop_size):
        for v in range(0, col+crop_size, 2*crop_size):
            if len(points) > 0:
                processed = False
                for p in points:
                    if abs(u-p[0]) < crop_size and abs(v-p[1]) < crop_size:
                        processed = True
                        break
                if processed:
                    continue
            crop_img = mask2[(u-crop_size):(u+crop_size),(v-crop_size):(v+crop_size)] 
            # to check whether all pixels have been processed            
#            print('crop_image size %s' %str([(u-crop_size),(u+crop_size),(v-crop_size),(v+crop_size)]) )        
            
            if crop_img.sum() != 0: # if white pixels in crop image
                #print("found point %s" %str([u,v]))
                points.append(np.array((u,v)))
 
    
                ave = ndimage.measurements.center_of_mass(crop_img)
                ave = ave + points[-1] - [crop_size, crop_size]
                


                if len(pins)>0:
                    # Avoid crop and split connecting components, ignore the white pixels detected less than the region of crop_size 
                    for i in range(0, len(pins)):                                                
                        pin=pins[i]
                        
                        if pin !=[]:
                            dist = math.sqrt((ave[0]-pin[0])**2+(ave[1]-pin[1])**2)
                            if dist <crop_size:

                                pins[i]=[]
                                avep = ave
                                newu = int(ave[0])
                                newv = int(ave[1])
                                crop_img = mask2[(newu-crop_size):(newu +crop_size),(newv-crop_size):(newv+crop_size)]
                            
                                ave = ndimage.measurements.center_of_mass(crop_img)
                                ave = ave + avep - [crop_size, crop_size] 


                cv2.imshow('crop_img',crop_img)
                cv2.waitKey(3)

                pins.append(ave)
                print pins,'pins'

    for i in range(0, len(pins)):
        if pins[i] !=[]:
            pinsn.append(pins[i])
    print pinsn,'pinsn'
    return pinsn, mask2