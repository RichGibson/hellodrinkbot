# Common Open Cocktail Robotics Stack

Description: A Raspberry pi dispensing robot with four pumps, controlled 
either from the command line or Node Red. 


Electrical

- Raspberry Pi 
- Motor Shield (will work with the older ones with a 2x13 header from adafruit) there are lots of underutilized older raspberry pi's!
- wires to the pumps
- Peristaltic Pumps

Physical

- Laser cut case
- fluid aggregation point, hose management


Software

- Command line interface-exists
- Node Red interface with RESTful endpoints  (tk)

Design files

- frame_2019-02-10.dxf


Assembly

- customize the case design as desired
- laser cut it onto 1/4"/6mm plywood or acrylic

- copy Raspberry Pi SD card image, put in pi
- boot up and customize it as desired (probably the wifi essid is the main thing)

default login username pi password raspberry

powering pi: you need to connect the pi to usb power, it is not recommended to 
use the motor power for the pi.


- [Assemble the motor hat](https://learn.adafruit.com/adafruit-dc-and-stepper-motor-hat-for-raspberry-pi/overview)

- mount the pi onto the back plate
Todo: need to figure this out. possibly plastic screws, untapped spacers, and 
plastic nuts on the top? there is not really clearance for nuts on all four 
positions on the top`o

- attach the 12 volt power to the motor shield

- install pumps into face plate with 8 screws and nuts (m3-12mm would work fine

- crimp connectors, or solder, 8 wires onto the pumps

- attach motor wires to motor hat, and put the hat on the pi

Motor hat needs 1 or two standoffs or spacers of its' own 

- power up and test before assembling the case

- assemble the case with m3-12mm screws and nuts

- attach tubing and figure out where to dispense

- connect to the pi as an access point

- design something entertaining.

- write some software...(a simple matter of programming)
