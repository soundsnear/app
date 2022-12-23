import pygame

sound_path="/home/tyler/app/chime.wav"

pygame.mixer.init()
chime_sound = pygame.mixer.Sound(sound_path)
chime_sound.set_volume(1) # full volume

def playChime ():
  pygame.mixer.Sound.play(chime_sound)