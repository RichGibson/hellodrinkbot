#THIS CODE IS HEAVILY BASED ON: 
# https://benchodroff.com/2017/02/18/using-a-raspberry-pi-with-a-microphone-to-hear-an-audio-alarm-using-fft-in-python/
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
notes = {0:'A',1:'G#/Ab',2:'G',3:'F#/Db',4:'F',5:'E',6:'F#/Db',7:'D',8:'C#/Db',9:'C-probably',10:'B',11:'A#/Bb',  12:'A'}



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
#notes =
while True:
    while _stream.get_read_available()< NUM_SAMPLES: sleep(0.01)
    audio_data  = frombuffer(_stream.read(
         _stream.get_read_available()), dtype=short)[-NUM_SAMPLES:]
    
    # Each data point is a signed 16 bit number, so we can normalize by dividing 32*1024
    normalized_data = audio_data / 32768.0

    w = hamming(2048)  
    # scipy.fft? is a module. But in python3 it is not callable.
    # it perhaps was fft, but now you want fft.fft
    # and / on integers was floor division, but in python 3 it is not. // is floor division
    intensity = abs(w*fft.fft(normalized_data))[:NUM_SAMPLES//2]
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
                if not (thefreq >= lastfreq-(lastfreq*.03) and thefreq <= lastfreq+(lastfreq*0.03)):
                    #print('adjfreq %f min intensity: %f max intensity %f' % (adjfreq,min(intensity), max(intensity)))
                    adj = 1200 *log2(RELATIVE_FREQ/adjfreq)/100
                    adj = round(adj % 12)
                    print("%s - %f - %f  intensity: %f" % (notes[adj], adj, adjfreq, max(intensity))) #'adjfreq %f min intensity: %f max intensity %f' % (adjfreq,min(intensity), max(intensity)))
                    lastfreq=adjfreq
                else:
                    #print('.', end='')
                    pass

    continue

          #adjfreq = 140    
    #print("Candidate Freq:  ", candidate_freq, which )
    #sys.stdout.write("Frequency: %d  \r" % (adjfreq))
    #sys.stdout.flush()
    #cents conversion
    if (adjfreq != -9999):
        print( "RAW FREQ:", adjfreq)
        adjfreq = 1200 *log2(RELATIVE_FREQ/adjfreq)/100
        adjfreq = adjfreq % 12
        print(adjfreq)

        #Case statements
        if abs(adjfreq - Note_E4 ) < 1:
            
            #In Tune E
            if abs(adjfreq - Note_E4) < 0.1  :
                print("You played an E!")
            #Sharp E
            elif (adjfreq - Note_E4) <  0  :
                print("You are sharp E!")
            #Flat E
            elif (adjfreq - Note_E4) > 0  :
                print("You are flat E!")
        elif abs(adjfreq - Note_E ) < 1:
                
            #In Tune E
            if abs(adjfreq - Note_E) < 0.1  :
                print("You played an E2!")
            #Sharp E
            elif (adjfreq - Note_E) < 0  :
                print("You are sharp E2!")
            #Flat E
            elif (adjfreq - Note_E) > 0  :
                print("You are flat E2!")
        elif abs(adjfreq - Note_B ) < 1:
            
            #In Tune B
            if abs(adjfreq - Note_B) < 0.1  :
                print("You played a B!")
            #Sharp B
            elif (adjfreq - Note_B) < 0  :
                print("You are sharp (B)!")
            #Flat B
            elif (adjfreq - Note_B)  >0  :
                print("You are flat (B)!")
        elif abs(adjfreq - Note_G ) < 1:
            
            #In Tune g
            if abs(adjfreq - Note_G) < 0.1  :
                print("You played a G!")
            #Sharp G
            elif (adjfreq - Note_G) < 0  :
                print("You are sharp (G)!")
            #Flat G
            elif (adjfreq - Note_G) > 0  :
                print("You are flat (G)!")
        
        elif abs(adjfreq - Note_D ) < 1:
    
            
            #In Tune D
            if abs(adjfreq - Note_D) < 0.1  :
                print("You played a D!")
            #Sharp D
            elif (adjfreq - Note_D) < 0  :
                print("You are sharp (D)!")
            #Flat D
            elif (adjfreq - Note_D) > 0  :
                print("You are flat (D)!")
        elif abs(adjfreq - Note_A ) < 1:
            
            #In tune A
            if abs(adjfreq - Note_A) < 0.2  :
                print("You played an A!")
            #Sharp A
            elif (adjfreq - Note_A) < 0  :
                print("You are sharp A!")
            #Flat A
            elif (adjfreq - Note_A)  > 0  :
                print("You are flat A!")
        elif abs(adjfreq - 12 ) < 1:
            
            #In tune A
            if abs(adjfreq - 12) < 0.2  :
                print("You played an A!")
            #Sharp A
            elif (adjfreq - 12) < 0  :
                print("You are sharp A!")
            #Flat A
            elif (adjfreq - 12)  > 0  :
                print("You are flat A!")
      #all off
    else:
        pass
    #sys.stdout.write("Cent: %s  \r" % adjfreq)
    #sys.stdout.flush()
        
    sleep(0.01)
