from spotify import SpotifyController
import sys
import oledDisplay
from oledDisplay import display_image_url

url = sys.argv[1]

print(f'playing {url}')

spotifyCotroller = SpotifyController()
# spotifyCotroller.play_url(url)

playing = spotifyCotroller.cur_playing()

images = playing['item']['album']['images']
print(images)

display_size=128
closest_target_image=next((x for x in images if  x['width'] > display_size), None)
print(closest_target_image)
display_image_url(closest_target_image['url'])







