# Martini or fuck you.

# Todo: currently allows double dispensing, a gin and vodka martini
# can be served at the same time, ala ukranian roulette.
# I need to either make two dispensers in Bender, or change this code to
# only dispense one martini at a time.

import pdb
from time import sleep
import board
import digitalio
from adafruit_seesaw.seesaw import Seesaw
from adafruit_seesaw.digitalio import DigitalIO
from adafruit_seesaw.pwmout import PWMOut

from threading import Thread, Event
import urllib.request

# For most boards.
i2c = board.I2C()

# Todo: This sometimes fails on start up so just try again
# RuntimeError: Seesaw hardware ID returned (0xc3) is not correct! Expected 0x55 or 0x87. Please check your wiring.
cnt = 0
while cnt < 5:
    try:
        arcade_qt = Seesaw(i2c, addr=0x3A)
        cnt = 99
    except:
        cnt+=1
        print('Seesaw hardware error...waiting to try again. cnt: ', cnt) 
        sleep(2)
        pass


# initialize buttons[] and leds[]
# Button pins in order (1, 2, 3, 4)
button_pins = (18, 19, 20, 2)
buttons = []
for button_pin in button_pins:
    button = DigitalIO(arcade_qt, button_pin)
    button.direction = digitalio.Direction.INPUT
    button.pull = digitalio.Pull.UP
    buttons.append(button)

# LED pins in order (1, 2, 3, 4)
led_pins = (12, 13, 0, 1)
leds = []
for led_pin in led_pins:
    led = PWMOut(arcade_qt, led_pin)
    leds.append(led)

try:
    from adafruit_motorkit import MotorKit
    emulation=0
except:
    # no motorkit
    emulation=1 

from bender_lib import Bender as Bender    
bender = Bender(emulation=0)

# Todo: want to turn off the light of a dispenser that is not dispensing
# there is a race condition, which is why in this loop I turn the led off
# and then on, so when it is interrupted it doesn't interfere with dispense()
# turning the light on.
def blink(foo):
    '''blink leds until stopped. Why? '''
    while True:
        if event.is_set():
            sleep(1)
            continue
        for num in (0,1):
            leds[num].duty_cycle = 0 
            sleep(.25)
            leds[num].duty_cycle = 65535
            sleep(.25)

event = Event()
ledthread = Thread(target=blink, args=(0,))
ledthread.start()

def dispense(num, bender):
    # whoops, race condition
    event.set()
    print("Start Dispense button: %i" % (num))
    leds[num].duty_cycle = 65535
    # todo: does urllib block? yes. So it is perfect

    # todo: need to determine the pump.
    # my 1,3,5,7 maps to dispensers 0,2,4,6
    # 0,2 - good stuff
    # 4,6 - You never expect the Malort
    # map 0 and 1 to good and bad

    # which pump should we use? 
    gin = num 
    bad = 2+num
    pump = num

    print('\tdispensing  a martini to pump %i ' % pump)

    # TODO: move this somewhere reasonable
    ml = 10 # how big is the drink? 10 is tiny for testing.
    SECONDS_PER_ML = 18/100. # huh?
    delay = ml*SECONDS_PER_ML

    # dispense our shot...
    bender.m[pump].throttle=-1
    sleep(delay)
    bender.m[pump].throttle=0

    leds[num].duty_cycle = 0 
    print('\tend dispense: ', num)
    flags[num]=0
    # I want to restart ledthread
    event.clear()
       
flags=[0,0]



first_pour=True
if __name__ == '__main__':
    print('Bender is ready for buttons...')
    while True:
        for led_number, button in enumerate(buttons):
            if led_number > 1:
                continue

            if not button.value:
                if first_pour:
                    #ledthread.stop()
                    first_pour=False

                if flags[led_number] == 1:
                    #print('sorry already pressed')
                    pass
                else:
                    flags[led_number] = 1
                    #print("Button pressed %i: value: %r" % (led_number, button.value))
                    x = Thread(target=dispense, args=(led_number,bender))
                    #x = Thread(target=dispense, args=(led_number,bender))
                    x.start()


# Copyright and other notices
# The original button code started with the AdaFruit example. 
# There is not much left of the original sample code, but props for
# the starting point..
# 
# This is AdaFruit sample license
#PDX-FileCopyrightText: 2022 Kattni Rembor for Adafruit Industries
# SPDX-License-Identifier: MIT
"""Arcade QT example that pulses the button LED on button press"""
