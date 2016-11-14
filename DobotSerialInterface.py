

import thread
import struct
from collections import deque
import serial
import time
from DobotStatusMessage import DobotStatusMessage
import binascii
import datetime


def f2b(i):
    return struct.pack('<f', i)


class DobotSerialInterface:

    serial_connection = None ## initial connection status: not connected
    read_buffer = deque() ## define read buffer
    current_status = None

    MOVE_MODE_JUMP = 0
    MOVE_MODE_JOINTS = 1  # joints move independent
    MOVE_MODE_LINEAR = 2  # linear movement

    def __init__(self, port_name='COM3', baud_rate=9600):
        thread.start_new_thread(self.read_loop, ())
        self.connect(port_name, baud_rate)

    def __del__(self): ## Destructor, close port when serial port instance is freed.
        print "Closing  "
        if self.serial_connection is not None and self.serial_connection.isOpen():
            print "Closing serial connection"
            self.serial_connection.close() ## close serial connection


    def connect(self, port_name='COM3', baud_rate=9600):
        self.serial_connection = None
        try:  # open port
            self.serial_connection = serial.Serial(
                port=port_name,
                baudrate=baud_rate,
                parity=serial.PARITY_NONE,  ## enable parity checking
                stopbits=serial.STOPBITS_ONE,  
                bytesize=serial.EIGHTBITS,  ## number of data bits
                timeout=0   ## set a timeout value,  non-blocking mode, 
				## return immediately in any case, returning zero or more, up to the requested number of bytes
            )
        except serial.SerialException as e:
            print "Could not connect", e

        time.sleep(2)  # no idea why but robot does not move if speed commands are sent
        # directly after opening serial

        while self.current_status is None:
            print "Waiting for status message"
            time.sleep(1)
        print "received first status message with position", self.current_status.position 
		## print initial position: "received first status message with position [291.05303955078125, 0.0, -33.794578552246094, 0.0]"

    def is_connected(self):
        return (self.serial_connection is not None) and self.serial_connection.isOpen()

    def _send_command(self, cmd_str_10):
        assert len(cmd_str_10) == 10

        if not self.is_connected():
            print "No serial connection"

        cmd_str_42 = ['\x00']*DobotStatusMessage.MESSAGE_LENGTH
        cmd_str_42[0] = '\xA5'
        cmd_str_42[-1] = '\x5A'
        for i in range(10):
            str4 = struct.pack('<f', float(cmd_str_10[i]))
            cmd_str_42[4 * i + 1] = str4[0]
            cmd_str_42[4 * i + 2] = str4[1]
            cmd_str_42[4 * i + 3] = str4[2]
            cmd_str_42[4 * i + 4] = str4[3]
        cmd_str = ''.join(cmd_str_42)
        self.serial_connection.write(cmd_str)
        #print "sending", binascii.b2a_hex(cmd_str)

    def _send_absolute_command(self, cartesian, p1, p2, p3, p4, move_mode,grip_angle,pause_time):
        # global cmd_str_10
        cmd_str_10 = [0]*10
        cmd_str_10[0] = 3 if cartesian else 6  # state=3:position or 6:angles
        cmd_str_10[2] = p1
        cmd_str_10[3] = p2
        cmd_str_10[4] = p3
        cmd_str_10[5] = p4
        #cmd_str_10[6] = 1#isgrab
        cmd_str_10[7] = move_mode  ## 0:Jump, 1:MovL, 2: MovJ
        cmd_str_10[8] = grip_angle #-90 to 90
        cmd_str_10[9] = pause_time # this can be set after sending each command
        self._send_command(cmd_str_10)

    def send_absolute_position(self, x, y, z, grip_angle,pause_time, rot=0, move_mode=0,): #MOVE_MODE_LINEAR):
        print "sending position %f %f %f %f" % (x, y, z, grip_angle)
        self._send_absolute_command(True, x, y, z, rot, move_mode,grip_angle, pause_time)

    def send_absolute_angles(self, base, rear, front, rot,  move_mode=MOVE_MODE_JUMP): #MOVE_MODE_LINEAR):
        # todo: assertions for ranges
        self._send_absolute_command(False, base, rear, front, rot,  move_mode)

    def set_initial_angles(self, rear_arm_angle, front_arm_angle):
        print 'setting angles to', rear_arm_angle, front_arm_angle
        cmd_str_10 = [0]*10
        cmd_str_10[0] = 9
        cmd_str_10[1] = 3  # set initial angle
        cmd_str_10[2] = rear_arm_angle
        cmd_str_10[3] = front_arm_angle
        self._send_command(cmd_str_10)

    def set_speed(self, VelRat=100, AccRat=100): 
    # arm stuck(stop in the process for maybe 0.3s)
    # when robot move nearly to the limit of its working angles (280,120...)
        cmd_str_10 = [0]*10
        cmd_str_10[0] = 10  ## teach & playback configuration
        cmd_str_10[2] = AccRat
        cmd_str_10[3] = VelRat
        self._send_command(cmd_str_10)

    def set_playback_config(self):
        cmd_str_10 = [0]*10
        cmd_str_10[0] = 9  ## motion parameters configuration are shown when state= 9
        cmd_str_10[1] = 1  ## choose mode 1: playback configuration
        cmd_str_10[2] = 200  # JointVel (max)
        cmd_str_10[3] = 200  # JointAcc
        cmd_str_10[4] = 200  # ServoVel
        cmd_str_10[5] = 200  # ServoAcc
        cmd_str_10[6] = 800  # LinearVel
        cmd_str_10[7] = 1000  # LinearAcc
        cmd_str_10[9] = 50 # JumpHeight
        self._send_command(cmd_str_10)
        


    def read_loop(self):
        print "Entering loop"

        cnt = 0

        while True:

            if self.serial_connection is None:
                print "Waiting for serial connection"
                time.sleep(0.5)
                continue

            r = self.serial_connection.read(200)  # TODO: select better count and read-type (see init)
            # print "read", len(r), "chars"

            ascii = binascii.b2a_hex(r)
            for i in range(len(ascii) / 2):
                self.read_buffer.append(ascii[2 * i] + ascii[2 * i + 1])

            n = len(self.read_buffer)
            if n < DobotStatusMessage.MESSAGE_LENGTH:
                continue

            # remove stuff in front of 'A5'
            while len(self.read_buffer):
                s = self.read_buffer[0]
                if s == 'a5':
                    break
                self.read_buffer.popleft()


            while len(self.read_buffer) >= DobotStatusMessage.MESSAGE_LENGTH:
                message = list()
                # print "buffer size", len(self.read_buffer)
                for i in range(DobotStatusMessage.MESSAGE_LENGTH):
                    message.append(self.read_buffer.popleft())

                # sanity check
                if message[-1] != '5a':
                    # print "Message was not terminated by '5a', but", message[-1], "ignoring message"
                    continue

                msg = DobotStatusMessage()
                msg.parse_ascii(message)


                self.current_status = msg
                if cnt % 10 == 0:  ## present status
                    #print datetime.datetime.now(), msg.angles
                    print datetime.datetime.now(), msg.position
                cnt += 1


