# Martini or fuck you.

# Todo: 
# - play bite my shiny metal ass if you pick the 'fuck you' button
# - hook pump or two pumps up to pour martini if you press the martini button

import pdb
import sys
import vlc
import os
from time import sleep
import board
import digitalio
from adafruit_seesaw.seesaw import Seesaw
from adafruit_seesaw.digitalio import DigitalIO
from adafruit_seesaw.pwmout import PWMOut
import random

from threading import Thread, Event
import urllib.request

# For most boards.
i2c = board.I2C()

# The Seesaw board fails on start up, so just retry up to five times.
# The error I get:
# RuntimeError: Seesaw hardware ID returned (0xc3) is not correct! Expected 0x55 or 0x87. Please check your wiring.

print('Initializing Seesaw board')
cnt = 0
while cnt < 5:
    try:
        arcade_qt = Seesaw(i2c, addr=0x3A)
        cnt = 99
    except:
        cnt+=1
        print('\tSeesaw hardware error...waiting to try again. cnt: ', cnt) 
        sleep(2)
        pass

# what is played when you press 'make it dirty'

dirty_files = [
        "file:////home/pi/hellodrinkbot/software/bender/sound/HERE COMES VIOLENCE - AUDIO FROM JAYUZUMI.COM.mp3",
        "file:///home/pi/hellodrinkbot/software/bender/sound/YOU DON'T HEAR ME NOT COMPLAINING - AUDIO FROM JAYUZUMI.COM.mp3",

    ]

# what is played for the 'fuck you' button
bad_files = [
        "file:////home/pi/hellodrinkbot/software/bender/sound/NOSE BLOW - AUDIO FROM JAYUZUMI.COM.mp3",
        "file:////home/pi/hellodrinkbot/software/bender/sound/bite.mp3",
    ]

# nice things, supportive things, dialoque you get when you make the correct choice.
good_files = [
        "file:////home/pi/hellodrinkbot/software/bender/sound/GOT IT - AUDIO FROM JAYUZUMI.COM.mp3",
        "file:////home/pi/hellodrinkbot/software/bender/sound/HEY, HERE'S AN IDEA - AUDIO FROM JAYUZUMI.COM.mp3",
        "file:///home/pi/hellodrinkbot/software/bender/sound/YOU GOT IT GENIUS - AUDIO FROM JAYUZUMI.COM.mp3",
        "file:///home/pi/hellodrinkbot/software/bender/sound/THIS PLACE HAS CLASS - AUDIO FROM JAYUZUMI.COM.mp3",
        "file:///home/pi/hellodrinkbot/software/bender/sound/THIS WILL TEACH THOSE FILTHY BASTARDS WHO'S LOVEABLE - AUDIO FROM JAYUZUMI.COM.mp3",
        "file:///home/pi/hellodrinkbot/software/bender/sound/MAYBE IF YOU CLEAN UP FIRST - AUDIO FROM JAYUZUMI.COM.mp3",
    ]




def load_media(files):
    media = []
    # try preloading files
    for file in files:
        # Grab file extension
        ext = (file.rpartition(".")[2])[:3]
        found = False
        # Test if url is a local file or remote
        if file[:4] == 'file':
            if os.path.isfile(file[7:]):
                found = True
            else:
                print ('Error: File ', file[7:], ' Not found')
                continue
        else:
            try:
                r = requests.get(file, stream=True)
                found = r.ok
            except ConnectionError as e:
                print('failed to get stream: {e}'.format(e=e))
                continue
        if found:
            #Media = Instance.media_new(file)
            media.append(Instance.media_new(file))
            Media_list = Instance.media_list_new([file])
            media[0].get_mrl()
            player.set_media(media[0])
    return media

Instance = vlc.Instance()
player = Instance.media_player_new()
player.audio_set_volume(200)

print ("Loading audio files")
good_media = load_media(good_files)
bad_media = load_media(bad_files)
dirty_media = load_media(dirty_files)

# So media is now a list, with the mp3 files listed in files[]
# and we can do player.set_media(media[index]) and then play that.
# so clean it up and ship it?
# maybe good_media and bad_media


def play(name, lst):
    # pick an audio file from the passed list and play it
    x = random.randint(0,len(lst)-1)
    print('\twhat %s media to play %i' % (name, x))
    media = lst[x]
    player.set_media(media)
    player.audio_set_volume(200)
    if player.play() == -1:
        print('error playing %s',name)



# initialize buttons[] and leds[]
# Button pins in order (1, 2, 3, 4)
button_pins = (18, 19, 20, 2)
buttons = []
for button_pin in button_pins:
    button = DigitalIO(arcade_qt, button_pin)
    button.direction = digitalio.Direction.INPUT
    button.pull = digitalio.Pull.UP
    buttons.append(button)

# LED pins in order (1, 2, 3, 4)
led_pins = (12, 13, 0, 1)
leds = []
for led_pin in led_pins:
    led = PWMOut(arcade_qt, led_pin)
    leds.append(led)

try:
    from adafruit_motorkit import MotorKit
    emulation=0
except:
    # no motorkit
    emulation=1 

from bender_lib import Bender as Bender    
bender = Bender(emulation=0)

# Todo: want to turn off the light of a dispenser that is not dispensing
# there is a race condition, which is why in this loop I turn the led off
# and then on, so when it is interrupted it doesn't interfere with dispense()
# turning the light on.
def blink(foo):
    '''blink leds until stopped. Why? '''
    while True:
        if event.is_set():
            sleep(1)
            continue
        for num in (0,1):
            sleep(.4)
            leds[num].duty_cycle = 0 
            leds[num+2].duty_cycle = 0 
            sleep(.4)
            leds[num].duty_cycle = 65535
            leds[num+2].duty_cycle = 65535 

event = Event()
ledthread = Thread(target=blink, args=(0,))
ledthread.start()

def dispense(num, bender):
    # whoops, race condition
    event.set()
    print('\tstart dispense: ', num)
    leds[num].duty_cycle = 65535
    # todo: does urllib block? yes. So it is perfect

    # todo: need to determine the pump.
    # my 1,3,5,7 maps to dispensers 0,2,4,6
    # 0,2 - good stuff
    # 4,6 - You never expect the Malort
    # map 0 and 1 to good and bad

    # which pump should we use? 
    # for bender it is pump 1 or 'fuck you'

    if num==0:
        pump = 0
        play('good', good_media)
        print('\tdispensing  a martini to pump %i ' % pump)

        # TODO: move this somewhere reasonable
        ml = 10 # how big is the drink? 10 is tiny for testing.
        SECONDS_PER_ML = 18/100. # huh?
        delay = ml*SECONDS_PER_ML

        # dispense our beverage...
        bender.m[pump].throttle=-1
        sleep(delay)
        bender.m[pump].throttle=0
    if num==1:
        play('bad', bad_media)
        print('\tNo Martini!')
    if num==2:
        pump = 1
        play('dirty', dirty_media)
        print('\tdispensing  some olive juice pump %i ' % pump)

        # TODO: move this somewhere reasonable
        ml = 10 # how big is the drink? 10 is tiny for testing.
        SECONDS_PER_ML = 18/100. # huh?
        delay = ml*SECONDS_PER_ML

        # dispense our beverage...
        bender.m[pump].throttle=-1
        sleep(delay)
        bender.m[pump].throttle=0

    leds[num].duty_cycle = 0 
    print('\tend dispense: ', num)
    flags[num]=0
    # I want to restart ledthread
    event.clear()
       
flags=[0,0,0]


# The case LED is on one of the extra motor ports
bender.m[3].throttle=-1

first_pour=True
if __name__ == '__main__':
    print('Bender is ready for buttons...')

    while True:
        for led_number, button in enumerate(buttons):
            if led_number > 2:
                continue
            if not button.value:
                if first_pour:
                    #ledthread.stop()
                    first_pour=False

                # had two buttons, now have three.
                #print(led_number, button)
                if flags[led_number] == 1:
                    #print('sorry already pressed')
                    pass
                else:
                    flags[led_number] = 1
                    print("Button pressed %i: value: %r" % (led_number, button.value))
                    x = Thread(target=dispense, args=(led_number,bender))
                    x.start()


