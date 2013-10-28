import pygame
import sys
import time

#the queue expects a list of tuples: filenames,and number of repeats
queue = []

def init():
	pygame.mixer.init()

def load(target):
	X = pygame.mixer.Sound(target)
	return X

def play(target):
	if type(target) == str:
		X = pygame.mixer.Sound(target)
	else:
		X = target
	X.play()

def background(target):
	if type(target) == str:
		pygame.mixer.music.load(target)
		pygame.mixer.music.play(-1)
	elif type(target) == list:
		for item in target:
			queue.append(item)
		playing = pygame.mixer.music.get_busy()
		if playing == False:
			pygame.mixer.music.load(queue[0][0])
			pygame.mixer.music.play(queue[1][1])
			queue[0].append(queue)
			queue = queue[1:]
	else:
		print "Error: Sent the wrong type to playlist in background."
		close()
		raise SystemExit

def fade():
	pygame.mixer.music.fadeout(time)

def volume(new=None):
	if new != None:
		pygame.mixer.music.set_volume(new)
	else:
		return pygame.mixer.music.get_volume()

def busy():
	return pygame.mixer.music.get_busy()

def queue():
	playing = pygame.mixer.music.get_busy()
        if playing == False:
        	pygame.mixer.music.load(queue[0][0])
                pygame.mixer.music.play(queue[1][1])
                queue[0].append(queue)
                queue = queue[1:]

def close():
	pygame.mixer.quit()

if __name__ == "__main__":
	target = sys.argv[1]
	pygame.mixer.pre_init(frequency=22050, size=-16, channels=2, buffersize=1024)
	pygame.init()
	init()
	background(target)
	try:
		while True:
			time.sleep(5)
	except:
		close()
		raise SystemExit
	close()
