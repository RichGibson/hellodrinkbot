#!/usr/bin/python

# pump_manual.py basically just use pdb 
# Modified to use the new MotorKit, which also requires python3

from adafruit_motorkit import MotorKit
#from Adafruit_MotorHAT import Adafruit_MotorHAT, Adafruit_DCMotor

import time
import atexit
import sys
import pdb

# python ./pumptest.py  <time in seconds>

if len(sys.argv) < 2 :
    print ("usage pumptest.py  <time in seconds>")
    print ("Runs all motors forward then all motors backwards for <time> seconds, and then repeats ")
    sys.exit(2)

t = float(sys.argv[1])
#t = int(sys.argv[1])

print( "run motors 1,2,3,4 for %i seconds" % (t))

# wait is motor hat or motor kit the new one?
# create a default object, no changes to I2C address or frequency
#mh1 = Adafruit_MotorHAT(addr=0x60)
#mh2 = Adafruit_MotorHAT(addr=0x61)

mh1 = MotorKit()
onehat = False
try:
    mh2 = MotorKit(address=0x61)
    onehat=True
except:
    onehat=False


# recommended for auto-disabling motors on shutdown!
def turnOffMotors():
    mh1.motor1.throttle = None 
    mh1.motor2.throttle = None
    mh1.motor3.throttle = None
    mh1.motor4.throttle = None
    try:
        mh2.motor1.throttle = None
        mh2.motor2.throttle = None
        mh2.motor3.throttle = None
        mh2.motor4.throttle = None
    except:
        pass

atexit.register(turnOffMotors)

#mh1.motor1.throttle=1
#mh2.motor1.throttle=1
#print('motors initialized any lights?')
#pdb.set_trace()
#mh1.motor1.throttle=-1
#mh2.motor1.throttle=-1

#print('well?')
#pdb.set_trace()
################################# DC motor test!
m = [None]
m.append(mh1.motor1)
m.append(mh1.motor2)
m.append(mh1.motor3)
m.append(mh1.motor4)
try:
    m.append(mh2.motor1)
    m.append(mh2.motor2)
    m.append(mh2.motor3)
    m.append(mh2.motor4)
except:
    pass

for i in m[1:]:
     print(i)

print('you have m and i.throttle=-1 or 1')
pdb.set_trace()

sys.exit(2)
while 1:
    print ('Start negative motors ')
    for i in m[1:]:
            i.throttle=-1
    time.sleep(t)

    print ('Start positive motors ')
    for i in m[1:]:
            print('before throttle')
            i.throttle=1
            print('after throttle')
    time.sleep(t)
