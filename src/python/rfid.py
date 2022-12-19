from pirc522 import RFID
from readntag215 import readNtag215Data
from spotify import SpotifyController

rdr = RFID()

spotifyCotroller = SpotifyController()

the_last_url = ""

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
          print(f"read: {new_url}")
          if new_url != the_last_url :
            spotifyCotroller.play_url(new_url)
          # Always stop crypto1 when done working
          rdr.stop_crypto()
# Calls GPIO cleanup
rdr.cleanup()
