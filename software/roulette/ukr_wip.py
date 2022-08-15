# Ukrainian Roulette - Work in progress to convert to use hellodrinkbot library

import sys
import random
import pdb
import readchar
import time
import threading

sys.path.append('..')
from hellodrinkbot import HelloDrinkbot as HD

hd = HD(emulation=0, left_button=5, right_button=6, ukr_max_drink=6, ukr_bad=0, ukr_drink_counter=0)



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
    if button==hd.left_button:
        key='1'
        player=1
    else:
        key='2'
        player=2

    # 1 = left player
    # 2 = right player

    # get drink number and bad number
    hd.ukr_next_drink()

    print('Dispense player=%i hd.ukr_drink_counter=%i bad=%i ' % (player,hd.ukr_drink_counter, hd.ukr_bad), end='')
    if hd.ukr_drink_counter==hd.ukr_bad:
        # serve the icky drink
        # reset hd.ukr_drink_counter and bad. Or should I? One bad out of six shots
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
        hd.m[pump].throttle = -1
        time.sleep(sleep_time)
        hd.m[pump].throttle = None 

        hd.ukr_drink_counter=0
        hd.ukr_bad=0
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
        hd.m[pump].throttle = -1
        time.sleep(sleep_time)
        hd.m[pump].throttle = None

    print('service complete for %s \n' % key)

################################# 
print("Waiting for a button to be pressed, or the enter key to quit")
#message = input("Press enter to quit\n\n") # Run until someone presses enter
while True:
    print('.', end='')
    time.sleep(.1)
GPIO.cleanup()
