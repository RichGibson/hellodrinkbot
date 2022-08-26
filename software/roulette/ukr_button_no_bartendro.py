import pdb
import time
import board
import digitalio
from adafruit_seesaw.seesaw import Seesaw
from adafruit_seesaw.digitalio import DigitalIO
from adafruit_seesaw.pwmout import PWMOut

from threading import Thread
import urllib.request

# For most boards.
i2c = board.I2C()

# Todo: This sometimes fails on start up
# RuntimeError: Seesaw hardware ID returned (0xc3) is not correct! Expected 0x55 or 0x87. Please check your wiring.
arcade_qt = Seesaw(i2c, addr=0x3A)

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


def dispense(num):
    print('start dispense: ', num)
    leds[num].duty_cycle = 65535
    #time.sleep(3)
    # todo: get bartendro up
    # todo: set the url of local bartendero, maybe to hostname? 
    # todo: does urllib block? yes. So it is perfect
    # todo: need to determine the pump.
    # my 1,3,5,7 maps to dispensers 0,2,4,6
    # 0,2 - good stuff
    # 4,6 - You never expect the Malort
    # map 0 and 1 to good and bad
 
    good = 0 + 2*num 
    bad = 4 + 2*num

    pump = good
    # the url is: 
    # /dispenser/size in ml
    # if button 0 is pushed, and then button 1, then  it appears
    # that the right pump turns off prematurely when the left pump turns off.
    # the led waits, but the pump stops.
    # this mush be in bartendro.
    apicall="http://ukr.local:8080//ws/dispense/%i/12" % pump
    print('calling: ', apicall)
    try:
        with urllib.request.urlopen(apicall) as response:
            rslt  = response.read()
            print('bartendro returned: ', rslt)
            time.sleep(2)
    except urllib.error.URLError:
        print('URLError trying to pour the shot. Is Bartendro running? num=', num)

    leds[num].duty_cycle = 0 
    print('end dispense: ', num)
    flags[num]=0
        
    

flags=[0,0]

if __name__ == '__main__':
    print('Ukranian Roulette is ready for buttons...')
    while True:
        for led_number, button in enumerate(buttons):
            if led_number > 1:
                continue

            if not button.value:
                if flags[led_number] == 1:
                    #print('sorry already pressed')
                    pass
                else:
                    flags[led_number] = 1
                    #print("Button pressed %i: value: %r" % (led_number, button.value))
                    x = Thread(target=dispense, args=(led_number,))
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
