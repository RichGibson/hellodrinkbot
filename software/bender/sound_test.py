import vlc
import pdb
from time import sleep


def try1():
    ''' plays the media, but needs to reload the file, which seems off. '''
    media = vlc.MediaPlayer('sound/bite.mpg')
    media.play()
    i=0
    while True:
        sleep(.1)
        i+=1
        print("%i -" %  i)
        if i % 40 == 0:
            print("\nPlay")
            media = vlc.MediaPlayer('sound/bite.mpg')
            media.play()


try1()
