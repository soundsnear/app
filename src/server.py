import os
from flask import Flask, redirect, url_for, request
from refreshImage import refresh_image
from refreshImage import set_image_from_uri
from playChime import playChime
from spotify import SpotifyController
from oledDisplay import turn_off_screen

spotifyController = SpotifyController()
app = Flask(__name__)

@app.route('/refreshImage')
def refreshImage():
   refresh_image(spotifyController)
   return 'success'

@app.route('/turnOffScreen')
def turnOffScreen():
   turn_off_screen()
   return 'success'

@app.route('/play',methods = ['POST'])
def play():
   uri = request.json['play_uri']
   print(uri)
   playChime()
   set_image_from_uri(spotifyController, uri)
   spotifyController.play_url(uri)
   return  'success'

@app.route('/restart')
def restart():
  os.system('systemctl restart raspotify.service')

if __name__ == '__main__':
   app.run(debug = False, host='0.0.0.0')
