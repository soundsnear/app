from pirc522 import RFID
from readntag215 import readNtag215Data
import requests

rdr = RFID()
the_last_url = ""
play_url = 'http://localhost:5000/play'

def play(uri):
  headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
  try:
    response = requests.post(play_url, json = {'play_uri': uri}, headers=headers)
  except requests.exceptions.HTTPError as error:
    print(error)

while True:
  rdr.wait_for_tag()
  (error, tag_type) = rdr.request()
  if not error:
    print("Tag detected")
    (error, uid) = rdr.anticoll()
    if not error:
      print("UID: " + str(uid))
      # Select Tag is required before Auth
      if not rdr.select_tag(uid):
          new_url = readNtag215Data(rdr)
          if new_url != the_last_url:
            print(f'playing {new_url}')
            the_last_url = new_url
            play(new_url)
          else:
            print('skipping')
          # Always stop crypto1 when done working
          rdr.stop_crypto()
# Calls GPIO cleanup
rdr.cleanup()
