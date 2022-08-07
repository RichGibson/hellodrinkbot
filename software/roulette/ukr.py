# Ukrainian Roulette

import sys
import random
import pdb
import readchar
import time

emulation=0
max_drink_counter=6 # one bad drink in each group of six
bad = 0
drink_counter = 0

try:
    import RPi.GPIO as GPIO # Import Raspberry Pi GPIO library

    GPIO.setwarnings(False) # Ignore warning for now
    GPIO.setmode(GPIO.BOARD) # Use physical pin numbering

    # Set pins 10 and 12 to be an input pin and set initial value to be pulled low (off)
    GPIO.setup(10, GPIO.IN, pull_up_down=GPIO.PUD_DOWN) 
    GPIO.setup(12, GPIO.IN, pull_up_down=GPIO.PUD_DOWN) 

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
            # serve the icky drink
            # reset drink_counter and bad. Or should I? One bad out of six shots
            #drink_counter=0
            #bad=0
        else:
            # serve a fine shot
            print('\tYou get to go to space. Congratulations')

# We don't know the state of the drink counter or of anything.
# you push the button and 1 or 2 shots are poured.
# 1 out of 6 shots should be bad. But there are edge cases one should
# keep in mind.



print("Starting loop. Press a button, or the keys '1', '2', or 'Q'")
while True: # Run forever
    if emulation == 1:
        key = readchar.readkey()
        if key.upper()=='Q':
            sys.exit(2)

        key=int(key)
        if key in (1,2):
            dispense(key)


    else:
        if GPIO.input(10) == GPIO.HIGH:
            one_player()
        if GPIO.input(12) == GPIO.HIGH:
            two_player()
