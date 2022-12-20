import mixAudio
import sys



volume=sys.argv[1]
print(f'Setting volume to {volume}')
mixAudio.set_speaker_volume(volume)
