from time import sleep
from picamera import PiCamera

def startCamera():
	camera = PiCamera()
	camera.resolution = (800, 600)
	camera.start_preview()
	sleep(0.1)

def imageCapture(name):
	jpgName = 'images/' + str(name) + '.jpg'
	camera.capture(jpgName)
