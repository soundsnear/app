import signal                   
import sys
import RPi.GPIO as GPIO
from spotify import SpotifyController

spotifyController = SpotifyController()

BUTTON_GPIO = 26


def signal_handler(sig, frame):
    GPIO.cleanup()
    sys.exit(0)

is_playing=False

def handle_button_press_event(_channel):
  global is_playing
  button_is_pressed = GPIO.input(BUTTON_GPIO)
  if button_is_pressed == 0:
    if is_playing :
      spotifyController.pause()
      is_playing=False
      print('pause')
    else :
      spotifyController.play(True)
      is_playing=True
      print('play')
      
def button_callback(channel):
    print(GPIO.input(BUTTON_GPIO))
    if not GPIO.input(BUTTON_GPIO):
        print("Button pressed!")
    else:
        print("Button released!")


def init_playpause_button() :
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(BUTTON_GPIO, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    
    GPIO.add_event_detect(BUTTON_GPIO, GPIO.RISING, 
            callback=handle_button_press_event, bouncetime=50)
    
    signal.signal(signal.SIGINT, signal_handler)


if __name__ == '__main__':
  init()
  signal.pause()