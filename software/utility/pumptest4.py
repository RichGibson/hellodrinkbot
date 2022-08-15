#!/usr/bin/python

# pumptest4 - test the 4 motors on 1,2,3,4. I _think_forward.

import time
import atexit
import sys
import pdb

# python ./pumptest.py  <time in seconds>

if len(sys.argv) < 2 :
    print ("usage pumptest.py  <time in seconds>")
    print ("Runs each motor for <time> seconds, and then repeats ")
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

while 1:
    n = 1
    print(n)
    for i in m[1:]:
            print ('Start motor: ', n, ' negative')
            print()
            i.throttle=-1
            time.sleep(t)
            i.throttle=None

            print ('Start motor: ', n, ' positive')
            i.throttle=1
            time.sleep(t)
            i.throttle=0

            n = n+1
    print('all pumps off waiting...')
    time.sleep(t)
