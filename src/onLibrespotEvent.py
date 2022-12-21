#!/usr/bin/env python

import os



eventName = os.environ.get('PLAYER_EVENT', "no event")

f = open("/home/tyler/app/src/python/librespot.txt", "a")
f.write(f" this is the event {eventName} \n ")
f.close()
if eventName == 'changed' or eventName == 'playing':
    from spotify import SpotifyController
    import sys
    import oledDisplay
    from oledDisplay import display_image_url

    spotifyCotroller = SpotifyController()
    # spotifyCotroller.play_url(url)

    playing = spotifyCotroller.cur_playing()

    images = playing['item']['album']['images']
    print(images)

    display_size=128
    closest_target_image=next((x for x in images if  x['width'] > display_size), None)
    print(closest_target_image)
#    display_image_url(closest_target_image['url'])

