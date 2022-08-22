# I (Rich Gibson/hellodrinkbot) based my code on:
# https://github.com/katrinamo/RPiPitch
# I ripped out all of the parts I didn't need, and updated it to run under python3
# And that code was: HEAVILY BASED ON: 
# https://benchodroff.com/2017/02/18/using-a-raspberry-pi-with-a-microphone-to-hear-an-audio-alarm-using-fft-in-python/

"""
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
from numpy import zeros,linspace,short,fromstring,frombuffer,hstack,transpose,log2, log
from scipy import fft, signal
from time import sleep
from scipy.signal import hamming, convolve
import matplotlib.pyplot as plt
import RPi.GPIO as GPIO
import sys
import pdb
#from findfundfreq import *
#Volume Sensitivity, 0.05: Extremely Sensitive, may give false alarms
#             0.1: Probably Ideal volume
#             1: Poorly sensitive, will only go off for relatively loud
SENSITIVITY= 1.0
#Bandwidth for detection (i.e., detect frequencies within this margin of error of the TONE)
BANDWIDTH = 1
# Show the most intense frequency detected (useful for configuration)
frequencyoutput=True

# on the xylophone some notes are more solid than others. 
#E-F, G-A are solid. Lowest G is good.

# it is mod 12, so 12 and 0 shouldn't both appear. But they do. Oh well.
notes = {0:{'note':'A','api':'1'},
1:{'note':'G#/Ab','api':''},
2:{'note':'G','api':'2'},
3:{'note':'F#/Db','api':''},
4:{'note':'F','api':'3'},
5:{'note':'E','api':'4'},
6:{'note':'F#/Db','api':''},
7:{'note':'D','api':'5'},
8:{'note':'C#/Db','api':''},
9:{'note':'C','api':'6'},
10:{'note':'B','api':'7'},
11:{'note':'A#/Bb',  'api':'8'},
12:{'note':'A','api':'1'} }
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
MIN_FREQUENCY = 700 
MAX_FREQUENCY = 1500
MAX_FREQUENCY = 3550
#Max & Min cent value we care about
MAX_CENT = 11
MIN_CENT = 0
RELATIVE_FREQ = 440.0
RELATIVE_FREQ = 880.0
#RELATIVE_FREQ = 1790
if len(sys.argv) > 1:
    if (sys.argv[1] >= 415.0 and sys.argv[1] <= 445.0):
        RELATIVE_FREQ = sys.argv[1]


#Set up audio sampler - 
NUM_SAMPLES = 2048
SAMPLING_RATE = 48000
pa = pyaudio.PyAudio()
_stream = pa.open(format=pyaudio.paInt16,
                  channels=1, rate=SAMPLING_RATE,
                  input=True,
                  frames_per_buffer=NUM_SAMPLES)

print("Detecting Frequencies. Press CTRL-C to quit.")
lastfreq=0
lastintensity=0
#notes =
while True:
    while _stream.get_read_available()< NUM_SAMPLES: sleep(0.01)
    # this sometimes generates input overflowed. So maybe just wrap it.
    audio_data  = frombuffer(_stream.read(
         _stream.get_read_available()), dtype=short)[-NUM_SAMPLES:]
    
    # Each data point is a signed 16 bit number, so we can normalize by dividing 32*1024
    normalized_data = audio_data / 32768.0

    w = hamming(2048)  
    # scipy.fft? is a module. But in python3 it is not callable.
    # it perhaps was fft, but now you want fft.fft
    # and / on integers was floor division, but in python 3 it is not. // is floor division
    intensity = abs(w*fft.fft(normalized_data))[:NUM_SAMPLES//2]
    maxintensity=max(intensity)
    if max(intensity) < 1.5 or max(intensity)>10:
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
                    apicall=''
                    if len(notes[adj]['api']) > 0:
                        apicall='/ws/shots/%s' % notes[adj]['api']
                    else:
                        pass

                    print("%s - %f - %f  intensity: %f api call: %s" % (notes[adj]['note'], adj, adjfreq, maxintensity, apicall)) 
                    #'adjfreq %f min intensity: %f max intensity %f' % (adjfreq,min(intensity), max(intensity)))

                    with urllib.request.urlopen('http://192.168.1.196:8080/%s' % apicall) as response:
                       html = response.read()
                    lastfreq=adjfreq
                else:
                    #print('.', end='')
                    pass
    lastintensity=maxintensity


