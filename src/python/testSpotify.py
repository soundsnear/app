from spotify import SpotifyController
import sys

url = sys.argv[1]

print(f'playing {url}')

spotifyCotroller = SpotifyController()
# spotifyCotroller.play_url(url)

playing = spotifyCotroller.cur_playing()

images = playing['item']['album']['images']
print(images)

display_size=128
closest_target_image=min(images, key=lambda x:abs(x['width']-display_size))
print(closest_target_image)






