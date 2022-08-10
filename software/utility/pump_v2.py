#!/usr/bin/python
# pump_v2.py - turn a pump on for a given amount of time.

# turn pump 1 on for 2 seconds
# python3.py pump_v2.py 1 2

# this automatically handles two motor shields. 

from adafruit_motorkit import MotorKit

import time
import atexit
import sys
import pdb

# python ./pump.py <motor number> <time in seconds>

if len(sys.argv) < 3 :
    print( "usage pump.py <motor>  <time in seconds>")
    print( "Runs motor # <motor> for <time in seconds> and then stops. ")
    sys.exit(2)

# 3 and 4 and 7 and 8 are reversed. I don't understand that.

pump=int(sys.argv[1])
timecnt=int(sys.argv[2])


def load_motors():
    """ load all possible motors as through we had 32 motor hats. But that is an absurd number,
    so lets be semi reasonable and only load 4 boards """

    max_brd = 4 # 32 are possible
    motors=[None]
    print('Trying to load up to %i Motor Hats' % max_brd)
    for i in range(0,4):
        addr = 0x60+i
        try:
            mh = MotorKit(address=addr)
            motors.append(mh.motor1)
            motors.append(mh.motor2)
            motors.append(mh.motor3)
            motors.append(mh.motor4)
            print('board found at ', hex(addr))
        except:
            print('no board at ', hex(addr))
            #print('no board at %x' % addr)
    return motors

motors=load_motors()

def turnOffMotors():
    for i in motors:
        try:
            i.throttle = None
        except:
            pass

atexit.register(turnOffMotors)

# motors is a zero baed array, but ignore motors[0]
motor_cnt = len(motors)-1
pump_cnt  = motor_cnt*2

motor = int((pump+1)/2)
if motor > motor_cnt:
    print("We have %i pumps. You asked for pump %i which is out of range" % (pump_cnt, pump))
    sys.exit(2)

print("turn on pump %i on motor %i " % (pump, motor))
myMotor=motors[motor]

if pump % 2:
	print('backward %i seconds' % timecnt)
	myMotor.throttle = -1
else:
	print('forward %i seconds' % timecnt)
	myMotor.throttle = 1

time.sleep(timecnt)
myMotor.throttle = None 








