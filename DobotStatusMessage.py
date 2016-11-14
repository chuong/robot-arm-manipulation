#! /usr/bin/env python

import struct
import binascii


class DobotStatusMessage():
    def __init__(self):
        pass

    MESSAGE_LENGTH = 42

    position = [None]*4  # x, y, z, yaw
    angles = [None]*4  # base, long, short, servo
    isGrab = None
    gripperAngle = None
    
    ## x,y,z,servo coordinates
    def get_x_coordinate(self):
        return self.position[0]
    def get_y_coordinate(self):
        return self.position[1]
    def get_z_coordinate(self):
        return self.position[2]
    def get_rotation_value(self):
        return self.position[3]
    
    ## angles    
    def get_base_angle(self):
        return self.angles[0]

    def get_rear_arm_angle(self):
        return self.angles[1]

    def get_front_arm_angle(self):
        return self.angles[2]

    def get_servo_angle(self):
        return self.angles[3]
        
    ## gripper: may not needed since it can be get directly from parse_ascii 
    def get_isgrab(self):
        return self.isgrab
    def get_gripper_angle(self):
        return self.gripperAngle
        
    def parse_ascii(self, ascii_list):
        assert isinstance(ascii_list, list)
        assert len(ascii_list) == self.MESSAGE_LENGTH
        assert isinstance(ascii_list[0], str)
        assert ascii_list[0] == 'a5'
        assert ascii_list[-1] == '5a'

        for i in range(10):
            first_byte = i * 4 + 1
            # and back to binary... TODO: remove ascii detour
            b = binascii.a2b_hex("".join(e for e in ascii_list[first_byte:first_byte + 4]))
            as_float = struct.unpack('<f', b)[0]

            if i < 4:
                self.position[i] = as_float
            if i < 8:
                self.angles[i - 4] = as_float
            if i == 8:
                self.isGrab = as_float > 0
            if i == 9:  # tenth float
                self.gripperAngle = as_float

