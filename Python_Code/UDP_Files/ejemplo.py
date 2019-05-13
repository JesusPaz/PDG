import pygame, mutagen.mp3, time

song_file = "Audio\\60-bpm-metronome.mp3"

mp3 = mutagen.mp3.MP3(song_file)
pygame.mixer.init(frequency=mp3.info.sample_rate)
pygame.mixer.music.load(song_file)
pygame.mixer.music.play()
time.sleep(30)