import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)

GPIO.setup(4, GPIO.IN)

key = GPIO.input(4)
print(key)

GPIO.cleanup()
