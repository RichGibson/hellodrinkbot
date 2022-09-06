# bender_lib.py - library for Bender
# I wanted a library for all of the hello drinkbot toys, but code and abstractions
# are hard. Sorry.

import sys
import pdb
import time
import atexit
import random
from datetime import datetime


try:
    from adafruit_motorkit import MotorKit
    emulation=0
except:
    # no motorkit
    emulation=1

class Bender():
    def __init__(self, **kwargs):
        """ Keyword arguments include:
            emulation   - do we have a pi and a motor hat?
        """

        self.mh1 = MotorKit()
        atexit.register(self.turnOffMotors)

        # I'm going to just run wild with unnamed arguments 
        for k, v in kwargs.items():
            setattr(self, k, v)


        self.buttons ={} 
        try:
            import RPi.GPIO as GPIO # Import Raspberry Pi GPIO library
            GPIO.setwarnings(False) # Ignore warning for now
            GPIO.setmode(GPIO.BCM) # GPIO.BCM or GPIO.BOARD

        except Exception as e:
            print(e)
            print('Raspberry pi not responding, continuing in emulation mode')
            self.emulation=1

        self.m = []
        try:
            self.m.append(self.mh1.motor1)
            self.m.append(self.mh1.motor2)
            self.m.append(self.mh1.motor3)
            self.m.append(self.mh1.motor4)
        except Exception as e:
            print(e)
            print("can't add motors in HelloDrinkbot.__init__()")
            sys.exit(2)
        # initialize 


    def turnOffMotors(self):
        self.mh1.motor1.throttle = None
        self.mh1.motor2.throttle = None
        self.mh1.motor3.throttle = None
        self.mh1.motor4.throttle = None


#### Tests below here
import unittest
class TestHelloDrinkbot(unittest.TestCase):
    def test(self):
        self.assertEqual(1,1) 

    def test_imports(self):
        try:
            from adafruit_motorkit import MotorKit
            emulation=0
        except:
            # no motorkit
            emulation=1
            self.assertEqual(1,0,"Can't import motorkit")

    def test_motors(self):
        # does self.turnOffMotors work?
        bender=Bender(emulation=0)
        bender.mh1.motor1.throttle=-1
        self.assertEqual(-1,bender.mh1.motor1.throttle)
        time.sleep(.5)
        bender.turnOffMotors()
        self.assertEqual(None,bender.mh1.motor1.throttle)


if __name__ == '__main__':
    print('Running hellodrinkbot library tests')
    unittest.main()



