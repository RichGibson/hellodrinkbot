#!/usr/bin/python
from Adafruit_MotorHAT import Adafruit_MotorHAT, Adafruit_DCMotor

import time
import atexit
import sys

# python ./pump.py <motor number> <time in seconds>

if len(sys.argv) < 3 :
    print "Runs motor # <motor> for <time in seconds> and then stops. "
    sys.exit(2)

m = int(sys.argv[1])
t = int(sys.argv[2])

print "run motor %i for %i seconds" % (m,t)


# create a default object, no changes to I2C address or frequency
mh = Adafruit_MotorHAT(addr=0x60)

# recommended for auto-disabling motors on shutdown!
def turnOffMotors():
    mh.getMotor(1).run(Adafruit_MotorHAT.RELEASE)
    mh.getMotor(2).run(Adafruit_MotorHAT.RELEASE)
    mh.getMotor(3).run(Adafruit_MotorHAT.RELEASE)
    mh.getMotor(4).run(Adafruit_MotorHAT.RELEASE)

#atexit.register(turnOffMotors)

################################# DC motor test!
myMotor = mh.getMotor(m)

# set the speed to start, from 0 (off) to 255 (max speed)
myMotor.setSpeed(255)

myMotor.run(Adafruit_MotorHAT.FORWARD);
time.sleep(t)
myMotor.run(Adafruit_MotorHAT.RELEASE);




