import asyncio
from evdev import InputDevice
import evdev
from drawArc import drawVolume
from oledDisplay import display_image_overlay, restore_last_image, display_image_url
import alsaaudio
from datetime import datetime
from spotify import SpotifyController

spotifyController = SpotifyController()


vol_device = "/dev/input/event0"
# play_button_device = "/dev/input/event2"

is_playing = True

MIN_UI_VOLUME=1
MAX_UI_VOLUME=10

MIN_SYSTEM_VOLUME=50
MAX_ACTUAL_VOLUME=80

FACTOR_UI_TO_SYSTEM = (MAX_ACTUAL_VOLUME-MIN_SYSTEM_VOLUME) / (MAX_UI_VOLUME - MIN_UI_VOLUME)

def system_to_ui_volume(system_volume):
  return int((system_volume - MIN_SYSTEM_VOLUME) /  FACTOR_UI_TO_SYSTEM )
  
def ui_to_system_volume(ui_volume):
  return int(ui_volume * FACTOR_UI_TO_SYSTEM + MIN_SYSTEM_VOLUME)


def display_volume (percent, number):
  image = drawVolume(percent, number)
  display_image_overlay(image)


mixer = alsaaudio.Mixer('Speaker', cardindex=1)

def set_speaker_volume(level):
    mixer.setvolume(level, alsaaudio.MIXER_CHANNEL_ALL)

def getCurrentVolume(): 
    vol = mixer.getvolume()
    return vol[0]


initialSystemVolume = getCurrentVolume()
uiVolume = system_to_ui_volume(initialSystemVolume)

print(f'starting at volume: {uiVolume} ({initialSystemVolume} system)')

def timestamp():
    return datetime.timestamp(datetime.now())
  
  
lastVolumeChangeTime = None
HIDE_AFTER_INACTIVITY_SECONDS = 2

async def restore_display():
    global lastVolumeChangeTime
    await asyncio.sleep(3)
    now=timestamp()
    if now - lastVolumeChangeTime > HIDE_AFTER_INACTIVITY_SECONDS:
      print('restoring image')
      restore_last_image()

async def handle_rotary_encoder_event(rel_event):
    event=rel_event.event
    global lastVolumeChangeTime
    lastVolumeChangeTime=timestamp()
    global retore_task
    global uiVolume
    direction = event.value
    uiVolume += direction
    if uiVolume < MIN_UI_VOLUME:
      uiVolume = 0
    if uiVolume > MAX_UI_VOLUME:
      uiVolume = MAX_UI_VOLUME
      
    percentVolume = uiVolume / MAX_UI_VOLUME
    display_volume(percentVolume, uiVolume)
    systemVolume = ui_to_system_volume(uiVolume)
    set_speaker_volume(systemVolume)
    # print(f'set volume to {systemVolume} ({uiVolume} in the UI)')
    asyncio.ensure_future(restore_display())

async def handle_button_press_event(key_event):
    global is_playing
    event=key_event.event
    if event.value == 1:
      if is_playing :
        spotifyController.pause()
        print('pause')
        is_playing=False
      else :
        spotifyController.play(True)
        print('play')
        is_playing=True

async def read_event(device):
    async for event in device.async_read_loop():
      categorized_event = evdev.categorize(event)
      if event.type == evdev.ecodes.EV_KEY :
        await handle_button_press_event(categorized_event)
      elif event.type == evdev.ecodes.EV_REL :
        await handle_rotary_encoder_event(categorized_event)          



def listen_for_events():
  volume_encoder = InputDevice(vol_device)
  # play_button = InputDevice(play_button_device)
  devices = [
    volume_encoder,
    # play_button,
  ]
  for device in devices:
    asyncio.ensure_future(read_event(device))

if __name__ == "__main__":
  display_image_url('https://i.pinimg.com/564x/bb/4d/8b/bb4d8b91caf68005ac8a02d849208416.jpg')
  listen_for_events()
  loop = asyncio.get_event_loop()
  loop.run_forever()