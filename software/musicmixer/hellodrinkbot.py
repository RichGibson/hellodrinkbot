# hellodrinkbot.py - library for hello drinkbot toys

import sys
import os
import pdb
import time
import atexit
import random
from datetime import datetime
import threading


try:
    from adafruit_motorkit import MotorKit
    emulation=0
except:
    # no motorkit
    emulation=1

class HelloDrinkbot():
    def __init__(self, **kwargs):
        """ Keyword arguments include:
            emulation   - do we have a pi and a motor hat?
        """
        self.mh1 = MotorKit()
        atexit.register(self.turnOffMotors)

        # I'm going to just run wild with unnamed arguments 
        for k, v in kwargs.items():
            setattr(self, k, v)

        # mapping pumps 1-8, ignore 0, because adjusting just
        # messes me up and leads to off by one
        self.dispense_flag=[0 for f in range(9)]
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

    def motor_on(self, pump, pumptime):
        print('\tStarting pump %s for %i seconds' % (pump, pumptime))
        self.dispense_flag[pump]=1
        #motor=0,1,2,3
        motor = pump // 2
        # direction = -1 or 1
        if pump % 2 == 0:
            direction = -1
        else:
            direction = 1
        self.m[motor].throttle = direction
        time.sleep(pumptime)
        self.m[motor].throttle = 0
        self.dispense_flag[pump]=0
        print('\tStopping pump %s after %i seconds' % (pump, pumptime))


    def dispense(self,pump, pumptime):
        '''
        pump 1-8 odd numbers are -1 even numbers 1, I guess.
        pump 1 self.m[0].throttle=-1
        pump 2 self.m[0].throttle=1
        pump 3 self.m[1].throttle=-1
        pump 4 self.m[1].throttle=1
        pump 5 self.m[2].throttle=-1
        pump 6 self.m[2].throttle=1
        pump 7 self.m[3].throttle=-1
        pump 8 self.m[3].throttle=1
        '''
        print(pump,time)
        print('dispense() pump %d time %d ' % (pump, pumptime))
        # check if we are dispensing on our pump, or our pump sister.
        # if not, set the dispense flag and call motor_on 
        if  self.dispense_flag[pump]==0:
            x=threading.Thread(target=self.motor_on, args=(pump, pumptime))
            x.start()



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
        hd=HelloDrinkbot(emulation=0)
        hd.mh1.motor1.throttle=-1
        self.assertEqual(-1,hd.mh1.motor1.throttle)
        time.sleep(.5)
        hd.turnOffMotors()
        self.assertEqual(None,hd.mh1.motor1.throttle)

if __name__ == '__main__':
    print('Running hellodrinkbot library tests')
    unittest.main()



