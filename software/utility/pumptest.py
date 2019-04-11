#!/usr/bin/python
from Adafruit_MotorHAT import Adafruit_MotorHAT #, Adafruit_DCMotor

import time
import atexit
import sys

# python ./pumptest.py  <time in seconds>

if len(sys.argv) < 2 :
    print "usage pumptest.py  <time in seconds>"
    print "Runs each motor for <time> seconds, and then repeats "
    sys.exit(2)

t = int(sys.argv[1])

print "run motors 1,2,3,4 for %i seconds" % (t)


# create a default object, no changes to I2C address or frequency
mh = Adafruit_MotorHAT(addr=0x60)

# recommended for auto-disabling motors on shutdown!
def turnOffMotors():
    mh.getMotor(1).run(Adafruit_MotorHAT.RELEASE)
    mh.getMotor(2).run(Adafruit_MotorHAT.RELEASE)
    mh.getMotor(3).run(Adafruit_MotorHAT.RELEASE)
    mh.getMotor(4).run(Adafruit_MotorHAT.RELEASE)

atexit.register(turnOffMotors)

################################# DC motor test!
m = [None]
for i in range(1,5):
	m.append(mh.getMotor(i))
	# set the speed to start, from 0 (off) to 255 (max speed)
	m[i].setSpeed(255)

while 1:
	n = 1
	for i in m[1:]:
		print ('Start motor: ', n)
		i.run(Adafruit_MotorHAT.FORWARD);
		time.sleep(t)
		i.run(Adafruit_MotorHAT.RELEASE);
		n = n+1
	print('all pumps off waiting...')
	time.sleep(t)
