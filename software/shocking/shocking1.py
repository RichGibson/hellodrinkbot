# Shocking1 - first experiments with the DS3502 DigiPot

import sys
import random
import pdb
import readchar
import time
from adafruit_motorkit import MotorKit
import board
import adafruit_ds3502
i2c = board.I2C()
ds3502 = adafruit_ds3502.DS3502(i2c)

emulation=0
max_drink_counter=6 # one bad drink in each group of six
bad = 0
drink_counter = 0


mh1 = MotorKit()

# recommended for auto-disabling motors on shutdown!
def turnOffMotors():
    mh1.motor1.throttle = None 
    mh1.motor2.throttle = None
    mh1.motor3.throttle = None
    mh1.motor4.throttle = None
    #mh2.motor1.throttle = None
    #mh2.motor2.throttle = None
    #mh2.motor3.throttle = None
    #mh2.motor4.throttle = None

#atexit.register(turnOffMotors)

m = [None]
m.append(mh1.motor1)
m.append(mh1.motor2)
m.append(mh1.motor3)
m.append(mh1.motor4)
#m.append(mh2.motor1)
#m.append(mh2.motor2)
#m.append(mh2.motor3)
#m.append(mh2.motor4)


try:
    import RPi.GPIO as GPIO # Import Raspberry Pi GPIO library

    GPIO.setwarnings(False) # Ignore warning for now
    #GPIO.setmode(GPIO.BOARD) 
    GPIO.setmode(GPIO.BCM)
    #GPIO.setup(13, GPIO.IN)
    #GPIO.setup(19, GPIO.IN)


    # Set pins 10 and 12 to be an input pin and set initial value to be pulled low (off)
    #GPIO.setup(13, GPIO.IN, pull_up_down=GPIO.PUD_DOWN) 
    GPIO.setup(13, GPIO.IN, pull_up_down=GPIO.PUD_UP) 
    GPIO.setup(19, GPIO.IN, pull_up_down=GPIO.PUD_UP) 

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


def dispense(player):
    """ dispense for a player
    player 1 is pumps 1 and 3
    player 2 is pumps 5 and 7

    player 1 - Motor 1 forward good stuff
    player 1 - Motor 2 forward bad stuff
    player 2 - Motor 3 forward good stuff
    player 2 - Motor 4 forward bad stuff
    """

    global drink_counter
    global bad
    print("\nIn dispense player=",player) 
    for i in range(player):
        # get drink number and bad number
        next_drink()
        print('\tdispense a drink player=%i drink_counter=%i bad=%i ' % (i,drink_counter, bad), end='')
        if drink_counter==bad:
            print('\tYou are not going into space today.')
            time.sleep(1)
            # serve the icky drink
            # reset drink_counter and bad. Or should I? One bad out of six shots
            drink_counter=0
            bad=0
        else:
            # serve a fine shot
            time.sleep(1)
            print('\tYou get to go to space. Congratulations')

    print('service complete\n')

# We don't know the state of the drink counter or of anything.
# you push the button and 1 or 2 shots are poured.
# 1 out of 6 shots should be bad. But there are edge cases one should
# keep in mind.


print("Starting loop. Press a button, or if you are not on a pi  the keys '1', '2', or 'Q'")
flag1=False
wiper1 = 0
#while True:
#    for i in range (12):
#        print(i*10)
#        ds3502.wiper = i*10
#        time.sleep(1)


while True: # Run forever
    # event loops don't need to run at system speed
    time.sleep(.01)
    t=time.time()
    if emulation == 1:
        key = readchar.readkey()
        if key.upper()=='Q':
            sys.exit(2)

        key=int(key)
        if key in (1,2):
            dispense(key)


    else:
        if GPIO.input(13) == GPIO.LOW:
            #dispense(1)
            if flag1==False:
                wiper1 += 10
                print('Was False now true.')
                print('Was False now true. wiper1: ', wiper1)
                ds3502.wiper = wiper1
                if wiper1 > 128:
                    wiper1 = 0
            flag1=True
        else:
            #GPIO.input(13) == GPIO.HIGH
            if flag1==True:
                print('Was True now false.')
                #ds3502.wiper = wiper1
            flag1 = False

        if GPIO.input(19) == GPIO.LOW:
            print('button 2 pushed')
            #dispense(2)
