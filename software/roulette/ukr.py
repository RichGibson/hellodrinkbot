# Ukrainian Roulette

import sys
import random
import atexit
import pdb
import readchar
import time
import threading
from adafruit_motorkit import MotorKit

emulation=0
max_drink_counter=6 # one bad drink in each group of six
bad = 0
drink_counter = 0


left_button=5
right_button=6

#####

mh1 = MotorKit()

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

def dispense(button):
    """ dispense for a player
    player 1 is pumps 1 and 3
    player 2 is pumps 5 and 7

    player 1 - Motor 1 forward good stuff
    player 1 - Motor 2 forward bad stuff
    player 2 - Motor 3 forward good stuff
    player 2 - Motor 4 forward bad stuff
    """
    print('dispense button: ', button)
    if button==left_button:
        key='1'
        player=1
    else:
        key='2'
        player=2

    global drink_counter
    global bad
    # 1 = left player
    # 2 = right player

    # get drink number and bad number
    next_drink()

    print('Dispense player=%i drink_counter=%i bad=%i ' % (player,drink_counter, bad), end='')
    if drink_counter==bad:
        # serve the icky drink
        # reset drink_counter and bad. Or should I? One bad out of six shots
        # 0 1 0 1
        # motors  1,2,3,4
        # left = 1 right=2
        # if bad it is 2 or 4
        # good = 1, 3
        # bad  = 2, 4
        #bad = player+1
       
         
        if player==1:
            pump =2
        if player==2:
            pump = 4

        print('\n\tpump %i You are NOT going to space today' % pump)
        m[pump].throttle = -1
        time.sleep(t)
        m[pump].throttle = None 

        drink_counter=0
        bad=0
    else:
        # serve a fine shot
        # player = 1 or 2
        # pump = 1 or 3 
        # how do I deal with my sense of cognitive decline. A little machine which 
        # takes player and bad/good and maps it to a pump. Should be easier than I make it.
        if player==1:
            pump = 1
        if player==2:
            pump = 3

        print('\n\tpump %i You get to go to space. Congratulations' % pump)
        m[pump].throttle = -1
        time.sleep(sleep_time)
        m[pump].throttle = None

    print('service complete for %s \n' % key)

# recommended for auto-disabling motors on shutdown!
def turnOffMotors():
    try:
        mh1.motor1.throttle = None 
        mh1.motor2.throttle = None
        mh1.motor3.throttle = None
        mh1.motor4.throttle = None
    except:
        pass

#atexit.register(turnOffMotors)

################################# DC motor test!
m = [None]
try:
    m.append(mh1.motor1)
    m.append(mh1.motor2)
    m.append(mh1.motor3)
    m.append(mh1.motor4)
except:
    print("can't add motors")
    sys.exit(2)

try:
    import RPi.GPIO as GPIO # Import Raspberry Pi GPIO library

    # GPIO.setwarnings(False) # Ignore warning for now
    GPIO.setwarnings(True) # Ignore warning for now
    #GPIO.setmode(GPIO.BOARD) 
    GPIO.setmode(GPIO.BCM)


    # Set pins left_button and right_button input pins and set initial value to be pulled low (off)
    GPIO.setup(left_button, GPIO.IN, pull_up_down=GPIO.PUD_UP) 
    GPIO.setup(right_button, GPIO.IN, pull_up_down=GPIO.PUD_UP) 
    GPIO.add_event_detect(left_button,GPIO.RISING,callback=dispense) # Setup event on rising edge
    GPIO.add_event_detect(right_button,GPIO.RISING,callback=dispense) # Setup event on rising edge

except:
    print('Raspberry pi not responding, continuing in emulation mode')
    emulation=1

def next_drink():
    """ increment the counter and if need be select the next bad shot"""
    global drink_counter
    global bad
    if bad == 0:
        bad = random.randrange(6)+1
    drink_counter += 1
    if drink_counter > max_drink_counter:
        drink_counter=1
        bad = random.randrange(6)+1

    return



sleep_time=2
def dispense(button):
    """ dispense for a player
    player 1 is pumps 1 and 3
    player 2 is pumps 5 and 7

    player 1 - Motor 1 forward good stuff
    player 1 - Motor 2 forward bad stuff
    player 2 - Motor 3 forward good stuff
    player 2 - Motor 4 forward bad stuff
    """
    print('dispense button: ', button)
    if button==left_button:
        key='1'
        player=1
    else:
        key='2'
        player=2

    global drink_counter
    global bad
    # 1 = left player
    # 2 = right player

    # get drink number and bad number
    next_drink()

    print('Dispense player=%i drink_counter=%i bad=%i ' % (player,drink_counter, bad), end='')
    if drink_counter==bad:
        # serve the icky drink
        # reset drink_counter and bad. Or should I? One bad out of six shots
        # 0 1 0 1
        # motors  1,2,3,4
        # left = 1 right=2
        # if bad it is 2 or 4
        # good = 1, 3
        # bad  = 2, 4
        #bad = player+1
       
         
        if player==1:
            pump =2
        if player==2:
            pump = 4

        print('\n\tpump %i You are NOT going to space today' % pump)
        m[pump].throttle = -1
        m[pump].throttle = None 
        time.sleep(sleep_time)
        drink_counter=0
        bad=0
    else:
        # serve a fine shot
        # player = 1 or 2
        # pump = 1 or 3 
        # how do I deal with my sense of cognitive decline. A little machine which 
        # takes player and bad/good and maps it to a pump. Should be easier than I make it.
        if player==1:
            pump = 1
        if player==2:
            pump = 3

        print('\n\tpump %i You get to go to space. Congratulations' % pump)
        m[pump].throttle = -1
        time.sleep(sleep_time)
        m[pump].throttle = None

    print('service complete for %s \n' % key)

print("Waiting for a button or enter")
message = input("Press enter to quit\n\n") # Run until someone presses enter
GPIO.cleanup()
