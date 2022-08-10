# Ukrainian Roulette

import sys
import random
import pdb
import readchar
import time
import threading
from adafruit_motorkit import MotorKit

emulation=0
max_drink_counter=6 # one bad drink in each group of six
bad = 0
drink_counter = 0

LEFT=0
RIGHT=1
GOOD=0
BAD=1



#####

mh1 = MotorKit()

#mh2 = MotorKit(address=0x61)

# recommended for auto-disabling motors on shutdown!
def turnOffMotors():
    try:
        mh1.motor1.throttle = None 
        mh1.motor2.throttle = None
        mh1.motor3.throttle = None
        mh1.motor4.throttle = None
        #mh2.motor1.throttle = None
        #mh2.motor2.throttle = None
        #mh2.motor3.throttle = None
        #mh2.motor4.throttle = None
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
    GPIO.setup(12, GPIO.IN, pull_up_down=GPIO.PUD_UP) 
    GPIO.setup(6, GPIO.IN, pull_up_down=GPIO.PUD_UP) 

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


thread_flags={}
thread_flags['1']=0
thread_flags['2']=0

t=2
def dispense(player):
    """ dispense for a player
    player 1 is pumps 1 and 3
    player 2 is pumps 5 and 7

    player 1 - Motor 1 forward good stuff
    player 1 - Motor 2 forward bad stuff
    player 2 - Motor 3 forward good stuff
    player 2 - Motor 4 forward bad stuff
    """

    key = str(player)
    global thread_flags
    global drink_counter
    global bad
    print("In dispense player=",player) 
    # 1 = left player
    # 2 = right player

    # get drink number and bad number
    next_drink()
    #print('\tdispense a drink player=%i drink_counter=%i bad=%i ' % (player,drink_counter, bad), end='')
    print('\tdispense a drink player= drink_counter= bad= ')
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
        m[pump].throttle = 1
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
        m[pump].throttle = 1
        time.sleep(t)
        m[pump].throttle = None

    thread_flags[key]=0
    print('service complete for %s \n' % key)

# We don't know the state of the drink counter or of anything.
# you push the button and 1 or 2 shots are poured.
# 1 out of 6 shots should be bad. But there are edge cases one should
# keep in mind.

print("Starting loop. Press a button, or the keys '1', '2', or 'Q' emulation=",emulation)
while True: # Run forever
    if emulation == 1:
        key = readchar.readkey()
        if key.upper()=='Q':
            sys.exit(2)
        key=int(key)
        if key in (1,2):
            dispense(key)

    else:
        if GPIO.input(12) == GPIO.LOW:
            if thread_flags['1']==0:
                print(' button 1 pushed ')
                thread_flags['1']=1
                x = threading.Thread(target=dispense, args=(1,))
                x.start()
        if GPIO.input(6) == GPIO.LOW:
            if thread_flags['2']==0:
                print('button 2 pushed')
                thread_flags['2']=1
                y = threading.Thread(target=dispense, args=(2,))
                y.start()
