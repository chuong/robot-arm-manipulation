

"""
the camera robot, position position must be fixed
in process of calculating transformation, the paper position must be fixed 
the final y position must be same as the proginal y position

@author: yuboya
"""

import time
import sys
from DobotSerialInterface import DobotSerialInterface

dobot_interface = DobotSerialInterface()

print "Opened connection"
dobot_interface.set_speed()
dobot_interface.set_playback_config()

i=0
sleep_duration = 5 #3

first_round = False
time.sleep(2) # wait for robot initialization

while True:


    print 1 # point 1
    dobot_interface.send_absolute_position(220, 210, 20, 20, 3)  # JUMP
    
    print 2 # point 2
    dobot_interface.send_absolute_position(130, 230, 20, -3, 2)

    print 2 # point 2
    #dobot_interface.send_absolute_position(210, -180, 50, 0)  # JUMP
    dobot_interface.send_absolute_position(130, 230, 20, -3, 3)  # JUMP
    
    print 1 # point 1
    dobot_interface.send_absolute_position(220, 210, 20, -3, 2)  # JUMP

    i = i+1
    print ('i='),i
    
    # 5 cycles
    if i==5:
        print ('Last Round: Move to initial position!')
        dobot_interface.send_absolute_position(265, 0, 25, 0, 3)  # JUMP
        time.sleep(sleep_duration)
        sys.exit(0)

        

