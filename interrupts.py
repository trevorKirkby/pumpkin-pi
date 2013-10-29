#!/usr/bin/env python

import time
import random
import RPi.GPIO as GPIO  
import pygame

# initialize pygame sound
pygame.mixer.pre_init(frequency=22050, size=-16, channels=2, buffer=1024)
pygame.init()
print 'using ',pygame.mixer.get_num_channels(),' audio channels'

# load our streaming background soundtrack
pygame.mixer.music.load("soundeffects/HalloweenBackgroundLoopNew.mp3")
pygame.mixer.music.set_volume(0.5)

# load the sound effects we will use
wolf = pygame.mixer.Sound("soundeffects/WolfCry.wav")
thunder = pygame.mixer.Sound("soundeffects/Thundercrack.wav")
wolf.set_volume(1.0)
thunder.set_volume(1.0)

# give each effect its own channel
wolfChannel = pygame.mixer.Channel(5)
thunderChannel = pygame.mixer.Channel(6)

# initialize GPIO
GPIO.setmode(GPIO.BCM)

# configure LED output
GPIO.setup(4, GPIO.OUT)
GPIO.output(4,0)

# configure switch inputs
for pin in (23,24,25,26):
	GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
time.sleep(1)

# define a global idle counter, initialized to a large value
idle = 1000

def lightning(nflashes = 5):
	for flashes in range(nflashes):
		delay = random.randint(5,30)
		time.sleep(0.01*delay)
		GPIO.output(4,1)
		time.sleep(0.01)
		GPIO.output(4,0)

def floorswitch(channel):
	print 'floorswitch pressed! %r' % channel
	# is the background soundtrack playing yet?
	if not pygame.mixer.music.get_busy():
		# turn the porch light off
		GPIO.output(4,0)
		# start the background soundtrack now
		pygame.mixer.music.play()
	# otherwise, is the wolf sound effect already playing?
	elif not wolfChannel.get_busy():
		# start the wolf sound effect now
		wolfChannel.play(wolf)
	# always reset our idle counter
	idle = 0

def doorbell(channel):
	print 'doorbell pressed! %r' % channel
	if not thunderChannel.get_busy():
		thunderChannel.play(thunder)
		lightning()
	# always reset our idle counter
	idle = 0

# add switch interrupt handlers
GPIO.add_event_detect(23, GPIO.RISING, callback = floorswitch)
GPIO.add_event_detect(24, GPIO.RISING, callback = floorswitch)
GPIO.add_event_detect(25, GPIO.RISING, callback = doorbell)

# turn on the light
GPIO.output(4,1)

# go into main loop, waiting for control-C
try:
	while True:
		time.sleep(1)
		musicPlaying = pygame.mixer.music.get_busy()
		if not musicPlaying:
			if idle < 30:
				# turn the porch light off
				GPIO.output(4,0)
				# restart the background music if any switches were recently active		
				pygame.mixer.music.play()
			else:
				# turn the porch light on
				GPIO.output(4,1)
		# print a periodic update
		print 'tick',idle,musicPlaying,wolfChannel.get_busy(),thunderChannel.get_busy()
		# update our idle counter
		idle += 1
except KeyboardInterrupt:
	print 'bye'

# cleaup
GPIO.cleanup()
pygame.mixer.quit()
