# -*- coding: utf-8 -*-
"""
Created on Wed Oct 19 21:19:58 2016

@author: yuboya
"""

# to calculate this, capture 2 images of 2 specific robotarm position

import math

# pinim = ... in calibrate_transform

def TransformationCalculation(xyzc):
    # robot arm position 1,2 in robot frame
    # (300, 0, 20, 0)


    xr1 = 220
    yr1 = 210
    zr1 = 20

  
    xr2 = 130
    yr2 = 230
    zr2 = 20
    
    
    # x,y,z coordinates in camera frame
    xcs = [point[0] for point in xyzc]
    ycs = [point[1] for point in xyzc]
    zcs = [point[2] for point in xyzc]
    
    xc1 = xcs[0]
    xc2 = xcs[1]
    yc1 = ycs[0]
    yc2 = ycs[1]
    zc1 = zcs[0]
    zc2 = zcs[1]
    
    
    a=xc2-xc1
    b=yc2-yc1
    c=xr2-xr1
    d=yr2-yr1
    
# from xc&yc
    cosa1 = -((d-c)*math.sqrt(2*d**2+2*c**2-b**2-2*a*b-a**2)+((-a)-b)*d+((-a)-b)*c)/(2*c**2+2*d**2)
    cosa2 =  ((d-c)*math.sqrt(2*d**2+2*c**2-b**2-2*a*b-a**2)+(a+b)*d+(a+b)*c)/(2*c**2+2*d**2)
    
    print cosa1, cosa2
    if cosa1>0:
        cosa = cosa1
    elif cosa2>0:
        cosa = cosa2
    else:
        raise ValueError
    
    alpha = math.acos(cosa) # in radians, degrees(alpha)= in degrees
    sina = math.sin(alpha)
    

    deltax1 = -(cosa*xc1+sina*yc1-xr1)
    deltax2 = -(cosa*xc2+sina*yc2-xr2)
    deltax = (deltax1+deltax2)/2
    print 'deltax: ', deltax1, deltax2, deltax

    
    deltay1 = -(cosa*yc1-sina*xc1-yr1)
    deltay2 = -(cosa*yc2-sina*xc2-yr2)
    deltay = (deltay1+deltay2)/2
    print 'deltay: ', deltay1, deltay2, deltay
    
    deltaz1 = -(zc1-zr1)  # 
    deltaz2 = -zc2+zr2
    deltaz = (deltaz1+deltaz2)/2
    print 'deltaz: ', deltaz1, deltaz2, deltaz
    
    
#    deltax=deltax1
#    deltay=deltay1
#    deltax=deltax2
#    deltay=deltay2
    
    return [alpha, deltax,deltay,deltaz]
    

    

