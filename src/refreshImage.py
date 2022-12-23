from spotify import SpotifyController
from oledDisplay import display_image_url

display_size=128


def get_image_url_from_images(images):
    closest_target_image=next((x for x in images if  x['width'] > display_size), images[0])
    return closest_target_image.get('url')

def set_image_from_uri(spotifyController, uri):
    print('uri')
    print(uri)
    image_url=None
    images = None
    if "album" in uri:
        response = spotifyController.sp.album(uri)
        images = response.get('images')
    elif "track" in uri:
        response = spotifyController.sp.track(uri)
        images = response['album']['images']
    elif "episode" in uri:
        response = spotifyController.sp.episode(uri)
        print(response)
        images = response.get('images')
    elif "playlist" in uri:
        response = spotifyController.sp.playlist(uri)
        images = response.get('images')
    else: 
        print(f'what type of uri is this? {uri}')
    if images is not None:
        image_url = get_image_url_from_images(images)
    if image_url is not None:
        display_image_url(image_url)

def refresh_image(spotifyController):
    playing = spotifyController.cur_playing()
    print(playing)
    print(playing)
    images = None
    type = playing.get('type')
    print(f'type: {type}')
    if type == 'episode' :
        images = images = playing.get('images')
    else:
        images = playing['item']['album']['images']
    print(images)
    closest_target_image_url=get_image_url_from_images(images)
    display_image_url(closest_target_image_url)
