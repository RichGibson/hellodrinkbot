# thread_test

# I want to lock pumps and call 'dispense()'  then unlock when it returns
# 

import logging
import threading
import time
import pdb

try:
    import RPi.GPIO as GPIO # Import Raspberry Pi GPIO library

    GPIO.setwarnings(False) # Ignore warning for now
    GPIO.setmode(GPIO.BCM)
    #GPIO.setup(13, GPIO.IN)
    #GPIO.setup(19, GPIO.IN)


    # Set pins to be input pins and set initial value to be pulled low (off)
    #GPIO.setup(13, GPIO.IN, pull_up_down=GPIO.PUD_DOWN) 
    GPIO.setup(12, GPIO.IN, pull_up_down=GPIO.PUD_UP) 
    GPIO.setup(6, GPIO.IN, pull_up_down=GPIO.PUD_UP) 

except:
    print('Raspberry pi not responding, continuing in emulation mode')
    emulation=1


flags = {}
flags['1']=0
flags['2']=0 

def thread_function(name):
    name=str(name)
    global flags
    print("Thread %s: starting" % name)
    print(type(name))
    print(name)
    print(flags[name])
    time.sleep(4)
    print("Thread %s: finishing" % name)
    flags[name]=0

print("Starting eventful loop.")
while True: # Run forever
    if GPIO.input(12) == GPIO.LOW:
        if flags['1'] == 0:
                flags['1'] = 1
                print(' button 1 pushed flags: ', flags)
                x = threading.Thread(target=thread_function, args=(1,))
                x.start()
    if GPIO.input(6) == GPIO.LOW:
        if flags['2'] == 0:
                print(flags)
                flags['2'] = 1
                print(' button 2 pushed flags: ', flags)
                y = threading.Thread(target=thread_function, args=(2,))
                y.start()

