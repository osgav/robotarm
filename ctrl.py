#!/usr/bin/env python

import usb.core
import usb.util
import sys
import time

from ps3 import *


# robot arm procedures
procs = {}
procs['reset']               = 0x00,0x00,0x00
procs['light_on']            = 0x00,0x00,0x01
procs['grip_close']          = 0x01,0x00,0x00
procs['grip_open']           = 0x02,0x00,0x00
procs['wrist_up']            = 0x04,0x00,0x00
procs['wrist_down']          = 0x08,0x00,0x00
procs['elbow_up']            = 0x10,0x00,0x00
procs['elbow_down']          = 0x20,0x00,0x00
procs['shoulder_up']         = 0x40,0x00,0x00
procs['shoulder_down']       = 0x80,0x00,0x00
procs['rotate_clockwise']    = 0x00,0x01,0x00
procs['rotate_cclockwise']   = 0x00,0x02,0x00

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


def robot_cmd(robot,procedure, nolog=False):
    '''
    send bytes along usb cable to robot arm
    if bytesout (the number of bytes written) is 3 all is well
    because we're trying to write 3 bytes
    '''

    bytesout = robot.ctrl_transfer(0x40, 6, 0x100, 0, procedure, 1000)
    
    proc_name = list(procs.keys())[list(procs.values()).index(procedure)]

    if bytesout == 3:
        if nolog == False:
            print "successful %s" % proc_name
        return True
    else:
        print "failed %s" % proc_name
        return False



def ps3_init():
    ps3_uninitialized = True
    while ps3_uninitialized:

        try:
            print "[+] Initializaing ps3 controller...",
            print "..."
            p = ps3()
            print "DONE"
            ps3_uninitialized = False
        except Exception as e:
            print "oh no... %s" % e
            ps3_uninitialized = True

        time.sleep(5)
    return p
        


def robot_init():
    robot_uninitialized = True
    while robot_uninitialized:

        try:
            print "[+] Initializing robot arm...",
            robot = usb.core.find(idVendor=0x1267, idProduct=0x0001)
            if robot is None:
                raise SystemError('robot arm not found')
            robot.set_configuration()
            robot_uninitialized = False
            print "DONE"
        except Exception as e:
            print "oh no... %s" % e
            robot_uninitialized = True
        
        time.sleep(5)
    return robot




# ctrl.py ENTRYPOINT

def main():
    
    r = robot_init()
    p = ps3_init()

    while True:

        # read ps3 controller state
        p.update()

        #if p.a_joystick_left_x > 0:
        #    print "moved left joystick X RIGHT!" 
        #elif p.a_joystick_left_x < 0:
        #    print "moved left joystick X LEFT!"

        if p.a_joystick_left_y > 0:
            #print "moved left joystick Y DOWN!" 
            robot_cmd(r, procs['elbow_down'])
        elif p.a_joystick_left_y < 0:
            #print "moved left joystick Y UP!"
            robot_cmd(r, procs['elbow_up'])

        #if p.a_joystick_right_x > 0:
        #    print "moved right joystick X RIGHT!"
        #elif p.a_joystick_right_x < 0:
        #    print "moved right joystick X LEFT!"

        elif p.a_joystick_right_y > 0:
            #print "moved right joystick Y DOWN!" 
            if robot_cmd(r,wrist_down):
                print "RIGHT JOYSTICK DOWN moving wrist down"
            else:
                print "RIGHT JOYSTICK DOWN possible error sending data..."
        elif p.a_joystick_right_y < 0:
            #print "moved right joystick Y UP!"
            if robot_cmd(r,wrist_up):
                print "RIGHT JOYSTICK UP moving wrist up"
            else:
                print "RIGHT JOYSTICK UP possible error sending data..."


        elif p.left:
            print "LEFT DPAD moving counter clockwise"
            robot_cmd(r,rotate_cclockwise)
        elif p.right:
            print "RIGHT DPAD moving clockwise"
            robot_cmd(r,rotate_clockwise)
        elif p.up:
            print "UP DPAD moving shoulder up"
            robot_cmd(r,shoulder_up)
        elif p.down:
            print "DOWN DPAD moving shoulder down"
            robot_cmd(r,shoulder_down)


        elif p.select:
            print "select pressed"
        elif p.start:
            print "start pressed"
        elif p.ps:
            print "ps pressed"


        elif p.l2:
            print "L2 closing grip"
            robot_cmd(r,grip_close)
        elif p.r2:
            print "R2 opening grip"
            robot_cmd(r,grip_open)
        elif p.l1:
            print "L1 sending light_on"
            robot_cmd(r,light_on)
        elif p.r1:
            print "R1 sending light_on"
            robot_cmd(r,light_on)


        elif p.triangle:
            print "TRIANGLE sending reset"
            robot_cmd(r,reset)
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
            robot_cmd(r,reset, nolog=True)


        # pause for 10ms before starting
        # over and reading ps3 controller state again
        time.sleep(.01)


if __name__ == '__main__':
    main()


