# -*- coding: utf-8 -*-
"""

@author: yuboya
"""
import numpy as np

def ImageToCamera(zc, camera_matrix, pins):
    
    f= camera_matrix[1][1] #=[0,0]
    cy = camera_matrix[0][2] # v
    cx = camera_matrix[1][2] # u
    
    # u = pin[0], v=pin[1], z = distance between camera and pin top
    xyzc = [np.array([zc*(pin[0]-cx)/f, zc*(pin[1]-cy)/f, zc])  for pin in pins]
    
    return xyzc