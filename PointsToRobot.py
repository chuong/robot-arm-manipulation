
"""

@author: yuboya
"""

### pins position to be sent to robot

## from TransformationCalculation:



import numpy as np
import math

def PointsToRobot(alpha, deltax,deltay,deltaz,xyzc):
    
    sina = math.sin(alpha)
    cosa = math.cos(alpha)
    pointrs = []

    for pointc in xyzc:

    # METHOD 2: matrix calculation
        pc = pointc.reshape(3,1)
        R = np.array([cosa, -sina, 0, sina, cosa, 0, 0,0,1])
        R = R.reshape(3,3) 
        T= np.array([deltax,deltay,deltaz])
        T = T.reshape(3,1)
        pr = np.dot(np.transpose(R),pc)+T
        pointr = pr.reshape(1,3)
        
        pointrs.append(pointr)
        
    return pointrs

