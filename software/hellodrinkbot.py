# hellodrinkbot.py - library for hello drinkbot toys

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

class HelloDrinkbot():
    def __init__(self, **kwargs):
        """ Keyword arguments include:
            left_button
            right_button
                 The GPiO's of the buttons for Ukranian Roulette and the Shocking Robot
            emulation   - do we have a pi and a motor hat?
            ukr_max_drink - one drink in this number will be bad
            ukr_drink_counter
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

            # TODO: need to figure out the proper callback for a button. Possibly pass it? 
            # Set pins left_button and right_button input pins and set initial value to be pulled low (off)
            if self.left_button:
                GPIO.setup(self.left_button, GPIO.IN, pull_up_down=GPIO.PUD_UP) 
                GPIO.add_event_detect(self.left_button,GPIO.RISING,callback=self.dispense, bouncetime=300) # Setup event on rising edge
                self.buttons[self.left_button]=0
                
            if self.right_button:
                GPIO.setup(self.right_button, GPIO.IN, pull_up_down=GPIO.PUD_UP) 
                GPIO.add_event_detect(self.right_button,GPIO.RISING,callback=self.dispense, bouncetime=300) # Setup event on rising edge
                self.buttons[self.right_button]=0
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

    def dispense(self,button):
        # button 2 is bouncing. So need to do something about that
        # check for bounce
        print('in dispense: ', button)
        if self.buttons[button]==0:
            self.buttons[button]=1
            now = datetime.now()
            print("\tin HelloDrinkbot.dispense() button: " ,now, button)
            #time.sleep(.4)
            self.buttons[button]=0
        print('\tdispense done\n')


    def turnOffMotors(self):
        self.mh1.motor1.throttle = None
        self.mh1.motor2.throttle = None
        self.mh1.motor3.throttle = None
        self.mh1.motor4.throttle = None

    def ukr_next_drink(self):
        """ For Ukranian Roulette  increment the counter and if need be, select the next bad shot"""
        self.ukr_drink_counter += 1
        if (self.ukr_drink_counter > self.ukr_max_drink) or (self.ukr_bad == 0):
            self.ukr_drink_counter=1
            self.ukr_bad = random.randrange(6)+1
    
        return


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



