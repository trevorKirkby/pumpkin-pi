#!/usr/bin/env python

import time
import RPi.GPIO as GPIO  
import pygame

# initialize pygame sound
pygame.mixer.pre_init(frequency=22050, size=-16, channels=2, buffer=1024)
pygame.init()

# load the sound effects we will use
wolf = pygame.mixer.Sound("soundeffects/WolfCry.wav")
thunder = pygame.mixer.Sound("soundeffects/Thundercrack.wav")

# initialize GPIO
GPIO.setmode(GPIO.BCM)

# configure LED output
GPIO.setup(4, GPIO.OUT)

# configure switch inputs
for pin in (23,24,25,26):
	GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
time.sleep(1)

def floorswitch(channel):
	print 'floorswitch pressed! %r' % channel
	wolf.play()

def doorbell(channel):
	print 'doorbell pressed! %r' % channel
	thunder.play()

# add switch interrupt handlers
GPIO.add_event_detect(23, GPIO.RISING, callback = floorswitch)
GPIO.add_event_detect(24, GPIO.RISING, callback = floorswitch)
GPIO.add_event_detect(25, GPIO.RISING, callback = doorbell)

# go into main loop, waiting for control-C
try:
	while True:
		time.sleep(1)
		print 'tick'
except KeyboardInterrupt:
	print 'bye'

# cleaup
GPIO.cleanup()
pygame.mixer.quit()