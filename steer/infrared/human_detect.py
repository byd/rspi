__author__ = 'byd'

import time

import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)
GPIO.setup(12, GPIO.IN)
while True:
    in_value = GPIO.input(12)
    if in_value == False:
        GPIO.output(11, False)
        time.sleep(1)
        GPIO.output(11, True)
        while in_value == False:
            in_value = GPIO.input(12)
