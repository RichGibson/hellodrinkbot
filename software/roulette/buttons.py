# Test buttons

import RPi.GPIO as GPIO

def button_callback(channel):
	print("button was pushed channel: ", channel)

right_pin=6
left_pin=5
GPIO.setwarnings(False) # Ignore warning for now
#GPIO.setmode(GPIO.BOARD) # Use physical pin numbering




# this is important...like, super important.
GPIO.setmode(GPIO.BCM) 
GPIO.setup(left_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP) # Set pin to be an input pin and set initial value to be pulled low (off)
GPIO.setup(right_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP) # Set pin to be an input pin and set initial value to be pulled low (off)

#import pdb
#print(dir(GPIO))
#pdb.set_trace()

GPIO.add_event_detect(left_pin,GPIO.RISING,callback=button_callback) # Setup event on rising edge
GPIO.add_event_detect(right_pin,GPIO.RISING,callback=button_callback) # Setup event on rising edge

message = input("Press enter to quit\n\n") # Run until someone presses enter
GPIO.cleanup() # Clean up
