# -*- coding: utf-8 -*-
"""
Created on Fri Nov 11 21:09:03 2016

@author: yuboya
"""
import math
import numpy as np

dists=[]
#uvreals = [(132.3, 340.3), (132.3, 399.7),
#           (127.9, 460.9), (204.8, 338.6),
#        (202.7, 395.4),(199.8, 455.3)]

uvreals = [(265.0, 356.0), (165.0, 482.0)]
        
uv35 = [(265.5, 356.0), (166.0, 481.0)]

for i in range(0,len(uvreals)):
    uv = uv35[i]
    uvreal = uvreals[i]
    dist = math.sqrt((uv[0]-uvreal[0])**2+(uv[1]-uvreal[1])**2)
    print dist,'       p ',str(i+1)
    dists.append(dist)
    if i == len(uvreals)-1:
        ave = np.sum(dists)/len(uvreals)
        print ave,'        ave'
        print np.amax(dists),'         max'
#        
        
        
#dists=[]
#prreals = [(300, 0, 20), (250, 50, 20)]
#
#prs = [(300.,    0.,   20. ), ( 252.99629036,   56.8725384 ,   20. )]
#prs = [(297.00370964,  -6.8725384 ,   20. ), ( 250.,   50.,   20. )]
#prs = [(298.50185482, -3.4362692, 20. ), ( 251.49814518, 53.4362692, 20. )]
#
##xrs = [pointr[0] for pointr in pointrs]
##yrs = [pointr[1] for pointr in pointrs]
##zrs = [pointr[2] for pointr in pointrs]
##prs = [(xrs[0],yrs[0],zrs[0]), (xrs[1],yrs[1],zrs[1])]
#
#for i in range(0,len(prreals)):
#    pr = prs[i]
#    prreal = prreals[i]
#    dx = pr[0]-prreal[0]
#    dy = pr[1]-prreal[1]
#    dz = pr[2]-prreal[2]
#    print dx,'  dx'
#    print dy,'  dy'
#    print dz,'  dz'
#    dist = math.sqrt(dx**2+dy**2+dz**2)
#    print dist,'       total d for point',str(i+1)
