import os
from flask import Flask, redirect, url_for, request
from refreshImage import refresh_image
from refreshImage import set_image_from_uri
from playChime import playChime
from oledDisplay import turn_off_screen
import asyncio
from spotify import SpotifyController
from aiohttp import web
from buttonHandler import listen_for_events
import contextlib
from  playPauseButton import init_playpause_button

spotifyController = SpotifyController()

def refreshImage(_request):
   refresh_image(spotifyController)
   return web.json_response({'success': True})


def turnOffScreen(_request):
   turn_off_screen()
   return web.json_response({'success': True})

async def play(request):
   jsonBody = await request.json()
   uri = jsonBody.get('play_uri')
   print(uri)
   set_image_from_uri(spotifyController, uri)
   print('got image successfully')
   # playChime()
   spotifyController.play_url(uri)
   return web.json_response({'success': True})


def restart(_request):
  os.system('systemctl restart raspotify.service')
  return web.json_response({'success': True})


app = web.Application()
app.add_routes([
   web.get('/restart', restart),
   web.get('/turnOffScreen', turnOffScreen),
   web.get('/refreshImage', refreshImage),
   web.post('/play', play)
   ])


async def run_other_task(_app):
    task = listen_for_events()

    yield

    task.cancel()
    with contextlib.supress(asyncio.CancelledError):
        await task  # Ensure any exceptions etc. are raised.

if __name__ == '__main__':
   print('starting whats next')
   init_playpause_button()
   app.cleanup_ctx.append(run_other_task)
   web.run_app(app, port=5000)
   print('starting whats there')
    

