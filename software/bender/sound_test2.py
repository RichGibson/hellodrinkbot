import requests
import vlc
import time
import os

#Test data a local file, a couple of radio stations and a video to cover all the bases
urls = [
        "file:///Users/richgibson/todo/projects/cocktail_robots/roboexotica/bender/sounds/GOT IT - AUDIO FROM JAYUZUMI.COM.mp3",
        "file:///Users/richgibson/todo/projects/cocktail_robots/roboexotica/bender/sounds/HEY, HERE'S AN IDEA - AUDIO FROM JAYUZUMI.COM.mp3",
    ]

#Define playlist extensions
playlists = set(['pls','m3u'])

#Define vlc playing Status values
playing = set([1,2,3,4])

Instance = vlc.Instance()
# try preloading files
for url in urls:
    print ("\n\nLooking for:", url)
    # Grab file extension
    ext = (url.rpartition(".")[2])[:3]
    found = False
    # Test if url is a local file or remote
    if url[:4] == 'file':
        if os.path.isfile(url[7:]):
            found = True
        else:
            print ('Error: File ', url[7:], ' Not found')
            continue
    else:
        try:
            r = requests.get(url, stream=True)
            found = r.ok
        except ConnectionError as e:
            print('failed to get stream: {e}'.format(e=e))
            continue
    if found:
        player = Instance.media_player_new()
        Media = Instance.media_new(url)
        Media_list = Instance.media_list_new([url])
        Media.get_mrl()
        player.set_media(Media)

    if player.play() == -1:
        print('error')
    print ('Sampling ', url, ' for 15 seconds')
    time.sleep(5)

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

    if ext in playlists:
        list_player.stop()
    else:
        player.stop()

