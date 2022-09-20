# Music Mixer 


This is the Music Mixer code. It is based on a Raspberry Pi guitar tuner.
See README-old.md for information on it.


- run `python freqDetect.py` in a linux terminal.

The original frequency detection algorithm can be found here https://benchodroff.com/2017/02/18/using-a-raspberry-pi-with-a-microphone-to-hear-an-audio-alarm-using-fft-in-python/



## Requirements
* Python 3.+
* scipy Python modules. 
* numpy Python modules.
* pyaudio

## Instructions 

I had some troubles. I had the code running, and then I had to go through 
a different process on a new Raspberry Pi. This seemed to work.

Sept 19, 2022

- pip install --upgrade pip
- sudo apt-get install portaudio19-dev
(on my Mac it was brew install portaudio)
- sudo apt-get install python3-scipy
- pip install pyaudio

Possibly also libatlas-base-dev?



