# Test buttons 

import sys
import time


try:
    import RPi.GPIO as GPIO # Import Raspberry Pi GPIO library

    GPIO.setwarnings(True) # 
    GPIO.setmode(GPIO.BCM)

    # Set pins 13 and 19 to be an input pin and set initial value to be pulled low (off)
    GPIO.setup(13, GPIO.IN, pull_up_down=GPIO.PUD_UP) 
    GPIO.setup(19, GPIO.IN, pull_up_down=GPIO.PUD_UP) 

    GPIO.setup(12, GPIO.IN, pull_up_down=GPIO.PUD_UP) 
    GPIO.setup(6, GPIO.IN, pull_up_down=GPIO.PUD_UP) 

except:
    print('Raspberry pi not responding, continuing in emulation mode')
    emulation=1

print("Starting loop. Press a button")
while True: # Run forever
    t=time.now()
    if GPIO.input(12) == GPIO.LOW:
        print(' button 1 pushed ', t)
    if GPIO.input(6) == GPIO.LOW:
        print('button 2 pushed', t)
