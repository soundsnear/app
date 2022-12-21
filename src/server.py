from flask import Flask, redirect, url_for, request
app = Flask(__name__)
from refreshImage import refreshImage
import os

@app.route('/refreshImage')
def success(name):
   refreshImage()
   return 'success'

@app.route('/play',methods = ['POST'])
def play():
   if request.method == 'POST':
      user = request.form['spotify_uri']
      return redirect(url_for('success',name = user))

@app.route('/restart')
def restart():
  os.system('systemctl restart raspotify.service')

if __name__ == '__main__':
   app.run(debug = True, host='0.0.0.0')
