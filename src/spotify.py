import errno
import tempfile
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from dotenv import load_dotenv
import os

load_dotenv()


scopes_list = [
  "app-remote-control",
  "streaming",
  "user-read-playback-state",
  "user-modify-playback-state",
  "user-read-currently-playing",
]

scope = " ".join(scopes_list)
REDIRECT_URI = "http://localhost"
CLIENT_ID = os.getenv('SPOTIFY_CLIENT_ID')
CLIENT_SECRET = os.getenv('SPOTIFY_CLIENT_SECRET')
REFRESH_TOKEN = os.getenv('SPOTIFY_REFRESH_TOKEN')
DEVICE_NAME = 'soundsnearone'


class TokenManager:
    def __init__(self, auth_manager, refresh_token):
        self.refresh_token = refresh_token
        self.auth_manager = auth_manager
        self.token_info = None

    def get_access_token(self):
        if self.token_info is None or self.auth_manager.is_token_expired(self.token_info):
            self.token_info = self.auth_manager.refresh_access_token(self.refresh_token)
        return self.token_info["access_token"]

class SpotifyController:
    def _find_device(self):
        print(f'Looking for device {DEVICE_NAME}')
        for device in self.sp.devices()["devices"]:
            if device["name"] == DEVICE_NAME:
                return device["id"]
        return None

    def __init__(self):
        # spotipy uses cache to save the access token (on refresh_access_token) and it can't be disabled
        # since we don't care about this cache just use a temp file
        tmp_cache = tempfile.NamedTemporaryFile()
        auth_manager=SpotifyOAuth(scope=scope, client_id=CLIENT_ID, client_secret=CLIENT_SECRET, redirect_uri=REDIRECT_URI, open_browser=False, cache_path=tmp_cache.name)
        self.sp = spotipy.Spotify(auth_manager=TokenManager(auth_manager, REFRESH_TOKEN))

        self.device_id = None
        while self.device_id is None:
            self.device_id = self._find_device()

    def get_progress_ms(self):
        return self.sp.currently_playing()["progress_ms"]

    def seek_track(self, progress_ms):
        if progress_ms > 0:
            self.sp.seek_track(progress_ms)
    
    def play_url(self, url):
        print(f'adding {url}')
        payload = {'uris': [url]} if 'track' in url or 'episode' in url else {'context_uri': url}
        url = f'me/player/play?device_id={self.device_id}'
        self.sp._put(url, payload=payload)

    def play(self):
        self.sp.transfer_playback(self.device_id, False)

    def pause(self):
        self.sp.pause_playback(self.device_id)

    def next(self):
        self.sp.next_track(self.device_id)

    def prev(self):
        self.sp.previous_track(self.device_id)
        
    def cur_playing(self):
        return self.sp.currently_playing()
