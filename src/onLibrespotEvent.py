#!/usr/bin/env python

import requests
import os

eventName = os.environ.get('PLAYER_EVENT', "no event")

if eventName == 'changed' or eventName == 'playing':
  url = 'http://localhost:5000/refreshImage'
  x = requests.get(url)
  print(x.text)
elif eventName == 'stopped' or eventName == 'paused':
  url = 'http://localhost:5000/turnOffScreen'
  x = requests.get(url)
  print(x.text)

