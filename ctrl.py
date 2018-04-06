#!/usr/bin/env python

import usb.core
import usb.util
import sys
import time

from ps3 import *


# initialize robot arm and ps3 controller

try:
    print "[+] Initializing robot arm...",
    dev = usb.core.find(idVendor=0x1267, idProduct=0x0001)
    if dev is None:
        raise SystemError('robot arm not found')
    dev.set_configuration()
    print "DONE"
except Exception as e:
    print "oh no... %s" % e
    exit(0)

try:
    print "[+] Initializing ps3...",
    print "..."
    p = ps3()
    print "DONE"
except Exception as e:
    print "oh no... %s" % e




# robot arm procedures

reset                  = 0x00,0,0
light_on               = 0x00,0,1
grip_close             = 0x01,0,0
grip_open              = 0x02,0,0
wrist_up               = 0x04,0,0
wrist_down             = 0x08,0,0
elbow_up               = 0x10,0,0
elbow_down             = 0x20,0,0
shoulder_up            = 0x40,0,0
shoulder_down          = 0x80,0,0
rotate_clockwise       = 0x00,0x01,0
rotate_cclockwise      = 0x00,0x02,0


def robot_cmd(procedure):
    '''
    send bytes along usb cable to robot arm
    if bytesout (the number of bytes written) is 3 all is well
    because we're trying to write 3 bytes
    '''

    bytesout = dev.ctrl_transfer(0x40, 6, 0x100, 0, procedure, 1000)

    if bytesout == 3:
        return True
    else:
        return False




def main():

    while True:

        # read ps3 controller state
        p.update()

        #if p.a_joystick_left_x > 0:
        #    print "moved left joystick X RIGHT!" 
        #elif p.a_joystick_left_x < 0:
        #    print "moved left joystick X LEFT!"

        if p.a_joystick_left_y > 0:
            #print "moved left joystick Y DOWN!" 
            if robot_cmd(elbow_down):
                print "LEFT JOYSTICK DOWN moving elbow down"
            else:
                print "LEFT JOYSTICK DOWN possible error sending data..."
        elif p.a_joystick_left_y < 0:
            #print "moved left joystick Y UP!"
            if robot_cmd(elbow_up):
                print "LEFT JOYSTICK UP moving elbow up"
            else:
                print "LEFT JOYSTICK DOWN possible error sending data..."

        #if p.a_joystick_right_x > 0:
        #    print "moved right joystick X RIGHT!"
        #elif p.a_joystick_right_x < 0:
        #    print "moved right joystick X LEFT!"

        elif p.a_joystick_right_y > 0:
            #print "moved right joystick Y DOWN!" 
            if robot_cmd(wrist_down):
                print "RIGHT JOYSTICK DOWN moving wrist down"
            else:
                print "RIGHT JOYSTICK DOWN possible error sending data..."
        elif p.a_joystick_right_y < 0:
            #print "moved right joystick Y UP!"
            if robot_cmd(wrist_up):
                print "RIGHT JOYSTICK UP moving wrist up"
            else:
                print "RIGHT JOYSTICK UP possible error sending data..."


        elif p.left:
            print "LEFT DPAD moving counter clockwise"
            robot_cmd(rotate_cclockwise)
        elif p.right:
            print "RIGHT DPAD moving clockwise"
            robot_cmd(rotate_clockwise)
        elif p.up:
            print "UP DPAD moving shoulder up"
            robot_cmd(shoulder_up)
        elif p.down:
            print "DOWN DPAD moving shoulder down"
            robot_cmd(shoulder_down)


        elif p.select:
            print "select pressed"
        elif p.start:
            print "start pressed"
        elif p.ps:
            print "ps pressed"


        elif p.l2:
            print "L2 closing grip"
            robot_cmd(grip_close)
        elif p.r2:
            print "R2 opening grip"
            robot_cmd(grip_open)
        elif p.l1:
            print "L1 sending light_on"
            robot_cmd(light_on)
        elif p.r1:
            print "R1 sending light_on"
            robot_cmd(light_on)


        elif p.triangle:
            print "TRIANGLE sending reset"
            robot_cmd(reset)
        elif p.circle:
            print "circle pressed"
        elif p.cross:
            print "cross pressed"
        elif p.square:
            print "square pressed"


        elif p.joystick_left:
            print "left joystick clicked!"
        elif p.joystick_right:
            print "right joystick clicked!"


        else:
            # stop moving
            robot_cmd(reset)


        # pause for 100ms before starting
        # over and reading ps3 controller state again
        time.sleep(.01)


if __name__ == '__main__':
    main()


