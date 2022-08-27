# ukr_lib.py - library for Ukranian Roulette.
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

class Ukr():
    def __init__(self, **kwargs):
        """ Keyword arguments include:
            emulation   - do we have a pi and a motor hat?
            ukr_max_drink - The number of drinks before a bad drink is guaranteed
            ukr_drink_counter
            ukr_bad
        """

        

        self.mh1 = MotorKit()
        atexit.register(self.turnOffMotors)

        # I'm going to just run wild with unnamed arguments 
        for k, v in kwargs.items():
            setattr(self, k, v)

        if not hasattr(self, 'ukr_bad'):
            self.ukr_bad=0
        if not hasattr(self, 'ukr_drink_counter'):
            self.ukr_drink_counter=0
        if not hasattr(self, 'ukr_max_drink'):
            self.ukr_max_drink=6


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

    def ukr_next_drink(self):
        ''' For Ukranian Roulette  increment the counter and if need be, select the next bad shot
         
        ''' 
        flag=True        
        self.ukr_drink_counter += 1
        if self.ukr_bad == 0: 
            self.ukr_bad = random.randrange(6)+1

        if self.ukr_drink_counter == self.ukr_bad: 
            flag=False
            self.ukr_drink_counter=1
            self.ukr_bad = random.randrange(6)+1
            
        #if  
        if (self.ukr_drink_counter > self.ukr_max_drink) or (self.ukr_bad == 0):
            self.ukr_drink_counter=1
            self.ukr_bad = random.randrange(6)+1
    
        return flag


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
        ukr=Ukr(emulation=0)
        ukr.mh1.motor1.throttle=-1
        self.assertEqual(-1,ukr.mh1.motor1.throttle)
        time.sleep(.5)
        ukr.turnOffMotors()
        self.assertEqual(None,ukr.mh1.motor1.throttle)

    def test_ukr_next_drink(self):
        # 
        ukr=Ukr(emulation=0)
        # they should start as zero.
        self.assertEqual(ukr.ukr_bad,0)
        self.assertEqual(ukr.ukr_drink_counter,0)
        cnt = 1
        while 1:
            ukr.ukr_next_drink()
            print('cnt: %i drink_counter: %i bad: %i ' % (cnt, ukr.ukr_drink_counter, ukr.ukr_bad))
            if ukr.ukr_drink_counter == ukr.ukr_bad:
                self.assertEqual(1,1,"We got a bad drink")
                break
            # we must fail at least once in ukr_max_drink (normall six) tries. And never go over that 
            # we can fail the first time.
            if cnt > ukr.ukr_max_drink:
                self.fail('ukr_next_drink did not end after max drinks')
            cnt+=1
        # Todo: probably need some test that ukr_bad is not always the same pump. But for now
        # you can run the tests and see if ukr_bad changes.

if __name__ == '__main__':
    print('Running hellodrinkbot library tests')
    unittest.main()



