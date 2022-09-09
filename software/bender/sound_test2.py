import pdb
import requests
import vlc
import time
import os

bad_files = [
        "file:////home/pi/hellodrinkbot/software/bender/sound/NOSE BLOW - AUDIO FROM JAYUZUMI.COM.mp3",
        "file:////home/pi/hellodrinkbot/software/bender/sound/bite.mp3",
    ]
good_files = [
        "file:////home/pi/hellodrinkbot/software/bender/sound/GOT IT - AUDIO FROM JAYUZUMI.COM.mp3",
        "file:////home/pi/hellodrinkbot/software/bender/sound/HEY, HERE'S AN IDEA - AUDIO FROM JAYUZUMI.COM.mp3",
        "file:///home/pi/hellodrinkbot/software/bender/sound/YOU GOT IT GENIUS - AUDIO FROM JAYUZUMI.COM.mp3",
        "file:///home/pi/hellodrinkbot/software/bender/sound/THIS PLACE HAS CLASS - AUDIO FROM JAYUZUMI.COM.mp3",
        "file:///home/pi/hellodrinkbot/software/bender/sound/THIS WILL TEACH THOSE FILTHY BASTARDS WHO'S LOVEABLE - AUDIO FROM JAYUZUMI.COM.mp3",
        "file:///home/pi/hellodrinkbot/software/bender/sound/MAYBE IF YOU CLEAN UP FIRST - AUDIO FROM JAYUZUMI.COM.mp3",
    ]

#Define playlist extensions
playlists = set(['pls','m3u'])

#Define vlc playing Status values
playing = set([1,2,3,4])

Instance = vlc.Instance()

def load_media(files):
    media = []
    # try preloading files
    for file in files:
        print ("\n\nLooking for:", file)
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

player = Instance.media_player_new()
good_media = load_media(good_files)
bad_media = load_media(bad_files)

# So media is now a list, with the mp3 files listed in files[]
# and we can do player.set_media(media[index]) and then play that.
# so clean it up and ship it?
# maybe good_media and bad_media
for media in good_media:
    # media is an array. And we can select any element, and play it.
    player.set_media(media)
    if player.play() == -1:
        print('error')
    print ('Sampling  for a few seconds')
    time.sleep(2)
    player.stop()

for media in bad_media:
    # media is an array. And we can select any element, and play it.
    player.set_media(media)
    if player.play() == -1:
        print('error')
    print ('Sampling  for a few seconds')
    time.sleep(2)
    player.stop()

#=========================================================#

#        #Use this code to play audio until it stops
#        print ('Playing ', url, ' until it stops')
#        time.sleep(5) #Give it time to get going
#        while True:
#            if ext in playlists:
#                state = list_player.get_state()
#                if state not in playing:
#                    break
#            else:
#                state = player.get_state()
#                if state not in playing:
#                    break
#=========================================================#


