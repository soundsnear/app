from spotify import SpotifyController
import sys

url = sys.argv[1]

print(f'playing {url}')

spotifyCotroller = SpotifyController()
spotifyCotroller.play_url(url)
spotifyCotroller.play_url(url)