# Bender the Vender

- Do you want a Martini, or fuck off. 

## Installation

    $ sudo su 
    # Requirements, the requirements.txt has a lot of unneeded things.
    # So either install them, or just try running bender.py and install
    # libraries as they are missing.
    $ pip install -r requirements.txt
    $ pip install python-vlc (should be in requirements)
    $ sudo crontab -e 

    add: 

    @reboot python /home/pi/hellodrinkbot/software/bender/bender.py

(There is a bit of tension between writing docs to be a contemporaneous 
account of the process, and notes that will help someone else follow your
path. You don't know what you need to know when you write the notes. How
much of the journey do you keep? Depends on how much time you have to edit
the documents)

## Next Steps

### Electronics
- mount 3rd switch and wiring. Slightly harder because the 3rd button is installed on the front plate
- mount 2 pumps, towards sides to provide room for head mounting options
- mount pi and button board and connect to motors and buttons
- mount leds. They are going to be obscured a bit by the arms. Drill hole, it gets too hot for hot glue.
- pi and pump power
- speaker in the head. Can cut off the base of the speakers

### Case
- glue top and sides of case
- close up the button box
- mount dispenser holder and tubing

- Cover where arms enter body?
- do the arms need to come off for packing? If so need to do things a bit different.

- Figure out head mounting


- Make it dirty label
- (Christine) finish the body. I think the Mouth is the big remaining issue. 

### Final!

- calibrate martini and dirty dispense amounts. Light pours, let people adjust their cocktail size by the number of times they push the buttons

- Martini glass, toothpicks, olives
- Olive juice


## Software

Pour martini from one pump, and olive juice to make it dirty from a second, 
premixed martinis, so just use my own code, no Bartendro

## Hardware

Two pumps, three buttons, Raspberry Pi, motor hat, and button board. Amazing body 
of Bender made by Christine.

## Sounds

Bender sound clips from JAYUZUMI.COM.mp3. Assigned a few sound clips to 'good'
(played when the user selects 'Martini,' 'bad' (when they select Fuck off),
and 'dirty' (when they make it dirty).

I have ~89 sound clips. I've added the clips I am using to the github repository.

## Log

### Sept 13th, 2022

Three buttons work. Reasonable sounds are played. The pumps are probably
working.

### Sept 7th, 2022

Did brain surgery, Ukranian Roulette gets the old pi. Bender has a 3b,
and a motor hat with header pins soldered on for the buttons and led's.

And booted up into bender.py, a copy of ukr.py, and the buttons blink back 
and forth just as they should.

### Sept 5th, 2022

Soldered a hat for an old raspberry pi, and buttons and connected
pumps and it all worked using the ukr.py code. So, copy that code
and reconfigure it to be Martini or fuck you.

