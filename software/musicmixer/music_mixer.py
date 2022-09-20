# The Music Mixer - A cocktail robot. 
# A microphone is put under a toy Xylophone.
# As you hit notes little bits of a cocktail are 
# served for you.
#
# I (Rich Gibson/hellodrinkbot) based my code on:
# https://github.com/katrinamo/RPiPitch
# I ripped out all of the parts I didn't need, and updated it to 
#run under python3
# And that code was: HEAVILY BASED ON: 
# https://benchodroff.com/2017/02/18/using-a-raspberry-pi-with-a-microphone-to-hear-an-audio-alarm-using-fft-in-python/

"""
9/19/2022 We are flying tomorrow so, er...make it work more?

Next:
- don't use bartendro, just call motorhat directly

8/21/2022
I can reasonably recognize nine notes. I only need eight. So what next?

- set bartendro ingredients appropriately.
- set shot size to something small
- use shots API


todo: F has stopped working. Not sure why.

"""
import urllib.request

#/usr/bin/env python
import pyaudio
import os
from numpy import zeros,linspace,short,fromstring,frombuffer,hstack,transpose,log2, log
from scipy import fft, signal
from time import sleep
from scipy.signal import hamming, convolve
#import matplotlib.pyplot as plt
#import RPi.GPIO as GPIO
import sys
import pdb

from hellodrinkbot import HelloDrinkbot

#from findfundfreq import *
#Volume Sensitivity, 0.05: Extremely Sensitive, may give false alarms
#             0.1: Probably Ideal volume
#             1: Poorly sensitive, will only go off for relatively loud
# Music Mixer will be in loud places. Fiddling with this seems important.


pumptime = 1 # how long a pump dispenses for a note
frequencyoutput=True

# on the xylophone some notes are more solid than others. 
#E-F, G-A are solid. Lowest G is good.

# it is mod 12, so 12 and 0 shouldn't both appear. But they do. Oh well.
# 'pump' is a pump id
notes = {
0:{'note':'A','pump':1},
1:{'note':'G#/Ab','pump':0},
2:{'note':'G','pump':2},
3:{'note':'F#/Db','pump':0},
4:{'note':'F','pump':3},
5:{'note':'E','pump':4},
6:{'note':'F#/Db','pump':0},
7:{'note':'D','pump':5},
8:{'note':'C#/Db','pump':0},
9:{'note':'C','pump':6},
10:{'note':'B','pump':7},
11:{'note':'A#/Bb',  'pump':8},
12:{'note':'A','pump':1} }
"""

D - 1172, has some G - 3164 overtones
E - 1336
F
G
A
B
C

next octave - identify as proper notes
D
E
F
G
A - 3539

So...seven notes plus these seem to work
G#/Ab works
Bb works

Some others bars on the top row work, but we only need eight pumps.
"""



#holds previous frequency
prevFreq = 0
z1 = 10
z2 = 0
z0 = 0
MIN_FREQUENCY = 60
MIN_FREQUENCY = 400 
MAX_FREQUENCY = 1500
MAX_FREQUENCY = 3550
# the bottom left repots as 4171, and I assume that is an overtone and I don't
# understand, nor have time for overtones!
# I want some notes which work mostly reliably.

#Max & Min cent value we care about
MAX_CENT = 11
MIN_CENT = 0
RELATIVE_FREQ = 440.0
RELATIVE_FREQ = 880.0
#RELATIVE_FREQ = 1790
if len(sys.argv) > 1:
    if (sys.argv[1] >= 415.0 and sys.argv[1] <= 445.0):
        RELATIVE_FREQ = sys.argv[1]

hd= HelloDrinkbot()

#Set up audio sampler - 
NUM_SAMPLES = 2048
SAMPLING_RATE = 48000
pa = pyaudio.PyAudio()
_stream = pa.open(format=pyaudio.paInt16,
                  channels=1, rate=SAMPLING_RATE,
                  input=True,
                  frames_per_buffer=NUM_SAMPLES)

MIN_INTENSITY = 1
MAX_INTENSITY = 10 
os.system('clear')
print("Music Mixer")
print("MIN_INTENSITY: %d MAX_INTENSITY: %d " % (MIN_INTENSITY, MAX_INTENSITY))
print("MIN_FREQUENCY: %d MAX_FREQUENCY: %d " % (MIN_FREQUENCY, MAX_FREQUENCY))
print("If you set the intensities low you can make drinks from ambient music")
print("Detecting Frequencies. Press CTRL-C to quit.")
lastfreq=0
lastintensity=0
while True:
    # wait until we have  NUM_SAMPLES in the stream
    while _stream.get_read_available()< NUM_SAMPLES: 
        sleep(0.01)

    audio_data  = frombuffer(_stream.read(
        _stream.get_read_available(), exception_on_overflow=False), dtype=short)[-NUM_SAMPLES:]

    # Each data point is a signed 16 bit number, so we can normalize by dividing 32*1024
    normalized_data = audio_data / 32768.0

    w = hamming(2048)  
    intensity = abs(w*fft.fft(normalized_data))[:NUM_SAMPLES//2]
    maxintensity=max(intensity)
    maxintensity=round(maxintensity, 4)
    if max(intensity) < MIN_INTENSITY or max(intensity)>MAX_INTENSITY:
        # Either too quiet or too loud
        continue

    if frequencyoutput:
        which = intensity[1:].argmax()+1
        # use quadratic interpolation around the max
        adjfreq = 1
    if which != len(intensity)-1:
            y0,y1,y2 = log(intensity[which-1:which+2:])
            x1 = (y2 - y0) * .5 / (2 * y1 - y2 - y0)
        # find the frequency and output:w it
            thefreq = (which+x1)*SAMPLING_RATE/NUM_SAMPLES
            if thefreq < MIN_FREQUENCY or thefreq > MAX_FREQUENCY:
                adjfreq = -9999
            else:
                thefreq = which*SAMPLING_RATE/NUM_SAMPLES
            if thefreq > MIN_FREQUENCY and thefreq < MAX_FREQUENCY:
                adjfreq = thefreq
            else:
                print('\t%d hz is out of range of %d hz - %d hz' % (thefreq, MIN_FREQUENCY, MAX_FREQUENCY, )) 
            if adjfreq != -9999:
                # todo: this eliminates duplicates, but I want to allow repeated strikes on the 
                # same note. But not as 'keybounces' Maybe a little delay.
                # if you are the same note, and within a given time then ignore, otherwise allow the duplicate.
                # or be more clever?
                # ignore when intensity is less than last intensity. 

                maxintensity=max(intensity)
                if not (thefreq >= lastfreq-(lastfreq*.03) and thefreq <= lastfreq+(lastfreq*0.03) and maxintensity<lastintensity):
                    #print('adjfreq %f min intensity: %f max intensity %f' % (adjfreq,min(intensity), max(intensity)))
                    adj = 1200 *log2(RELATIVE_FREQ/adjfreq)/100
                    adj = round(adj % 12)
                    pump =notes[adj]['pump']
                    if pump > 0:
                        hd.dispense(pump, pumptime)
                    else:
                        pass

                    print("%s - %f hz  intensity: %f pump : %s" % (notes[adj]['note'],  adjfreq, maxintensity, pump)) 
                    #'adjfreq %f min intensity: %f max intensity %f' % (adjfreq,min(intensity), max(intensity)))

                    #with urllib.request.urlopen('http://192.168.1.196:8080/%s' % apicall) as response:
                    #   html = response.read()
                    lastfreq=adjfreq
                else:
                    print("\tDuplicate, not dispensing %s -  %f hz  intensity: %f " % (notes[adj]['note'],  adjfreq, maxintensity)) 
                    #print('.', end='')
                    pass
    lastintensity=maxintensity


