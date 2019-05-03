#!/usr/bin/python
from Adafruit_MotorHAT import Adafruit_MotorHAT #, Adafruit_DCMotor

import time
import atexit
import sys

# python ./pump.py <motor number> <time in seconds>

if len(sys.argv) < 3 :
    print "usage pump.py <motor>  <time in seconds>"
    print "Runs motor # <motor> for <time in seconds> and then stops. "
    sys.exit(2)

m = int(sys.argv[1])
t = int(sys.argv[2])

m2 = (m+1)/2

# create a default object, no changes to I2C address or frequency
mh = Adafruit_MotorHAT(addr=0x60)


myMotor=mh.getMotor(m2)

def turnOffMotors():
    mh.getMotor(m2).run(Adafruit_MotorHAT.RELEASE)

atexit.register(turnOffMotors)

myMotor.setSpeed(255)

print('m: %i m2: %i' %(m, m2))
if m % 2:
	print('forward')
	myMotor.run(Adafruit_MotorHAT.FORWARD);
else:
	print('backward')
	myMotor.run(Adafruit_MotorHAT.BACKWARD);
time.sleep(t)
myMotor.run(Adafruit_MotorHAT.RELEASE);








