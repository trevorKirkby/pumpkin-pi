#!/usr/bin/env python2.7

import RPi.GPIO as GPIO
import sys
import random
import time
import playsound
import pygame

pygame.mixer.pre_init(frequency=22050, size=-16, channels=2, buffer=1024)
pygame.init()
playsound.init()

board_type = sys.argv[-1]

GPIO.setmode(GPIO.BCM)                  # initialise RPi.GPIO
for i in (23,24,25,26):                  # set up ports 23-25 
    GPIO.setup(i, GPIO.IN, pull_up_down=GPIO.PUD_UP)  # as inputs pull-ups high      

GPIO.setup(4, GPIO.OUT)

GPIO.output(4, 0)

# Print  Instructions appropriate for the selected board
if board_type == "m":
    print "That's not a gertboard. This program requires a gertboard."

else:
    print "These are the connections for the Gertboard sound interface:"
    print "GP25 in J2 --- B1 in J3"
    print "GP24 in J2 --- B2 in J3"
    print "GP23 in J2 --- B3 in J3"
    print "Optionally, if you want the LEDs to reflect button state do the following:"
    print "jumper on U3-out-B1"
    print "jumper on U3-out-B2"
    print "jumper on U3-out-B3"

button_press = 0        # set intial values for variables
previous_status = ''

wolf = playsound.load("soundeffects/WolfCry.wav")
thunder = playsound.load("soundeffects/Thundercrack.wav")
doorbell = playsound.load("soundeffects/doorbell.wav")

class DualState():
    def __init__(self):
	self.input = 0
    def stateDormant(self):
	self.input = 0
	if playsound.busy():
	    playsound.fade()
	GPIO.output(4, 1)
	while self.input == 0:
	    time.sleep(1)
	self.stateActive()
    def stateActive(self):
	GPIO.output(4, 0)
	playsound.background("soundeffects/HalloweenbackgroundLoopNew.mp3")
	while self.input > 0:
	    self.input -= 1
	    time.sleep(1)
	self.stateDormant()

system = DualState()

try:
    while True:
        status_list = [GPIO.input(25), GPIO.input(24), GPIO.input(23)]
        for i in range(0,3):
            if status_list[i]:
                status_list[i] = "1"
            else:
                status_list[i] = "0"
        # dump current status values in a variable
        current_status = ''.join((status_list[0],status_list[1],status_list[2]))
        # if that variable not same as last time 
        if current_status != previous_status:
            print current_status                # print the results 
            if current_status != "111":
                  if current_status == "110":
			#pressureplate 1
		  	playsound.play("soundeffects/"+random.choice(["CrowCaw.wav","OwlHoot.wav"]))
			system.input = 30
                  elif current_status == "011":
			#doorbell
			system.input = 30
                        thunder.play()
			GPIO.output(4, 1)
                        time.sleep(0.01)
                        GPIO.output(4, 0)
			for flashes in range(5):
			    delay = random.randint(5,30)
			    time.sleep(0.01*delay)
			    GPIO.output(4, 1)
			    time.sleep(0.01)
        		    GPIO.output(4, 0)
                  elif current_status == "101":
			#pressureplate 2
			system.input = 30
                        wolf.play()
                  else:
                        pass
            # update status variable for next comparison
            previous_status = current_status
            button_press += 1                   # increment button_press counter

except KeyboardInterrupt:          # trap a CTRL+C keyboard interrupt
    GPIO.cleanup()                 # resets all GPIO ports used by this program
    playsound.close()
playsound.close()
GPIO.cleanup()                     # on exit, reset all GPIO ports 
