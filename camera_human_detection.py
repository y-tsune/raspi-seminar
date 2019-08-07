import RPi.GPIO as GPIO
from picamera import PiCamera
from time import sleep

GPIO.setmode(GPIO.BCM)
GPIO.setup(18, GPIO.IN)

camera = PiCamera()

while True:
    GPIO.wait_for_edge(18, GPIO.BOTH)
    if GPIO.input(18):
        camera.start_preview()
        sleep(1)
        camera.capture('/home/pi/image.jpg')
        camera.stop_preview()
    sleep(1)

GPIO.cleanup()


