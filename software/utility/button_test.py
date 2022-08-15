# Test buttons 

import sys


try:
    import RPi.GPIO as GPIO # Import Raspberry Pi GPIO library

    GPIO.setwarnings(True) # 
    GPIO.setmode(GPIO.BCM)

    left=12
    right=6
    # Set pins left and right to be an input pin and set initial value to be pulled low (off)
    GPIO.setup(left, GPIO.IN, pull_up_down=GPIO.PUD_UP) 
    GPIO.setup(right, GPIO.IN, pull_up_down=GPIO.PUD_UP) 

    GPIO.setup(left, GPIO.IN, pull_up_down=GPIO.PUD_UP) 
    GPIO.setup(right, GPIO.IN, pull_up_down=GPIO.PUD_UP) 

except:
    print('Raspberry pi not responding, continuing in emulation mode')
    emulation=1

print("Starting loop. Press a button")
while True: # Run forever
    if GPIO.input(left) == GPIO.LOW:
        print(' button 1 pushed ')
    if GPIO.input(right) == GPIO.LOW:
        print('button 2 pushed')
