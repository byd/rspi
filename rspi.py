#!/usr/bin/env python
# encoding: utf-8

import time

import RPi.GPIO

port = 15
RPi.GPIO.setmode(RPi.GPIO.BCM)
RPi.GPIO.setup(port, RPi.GPIO.IN)
RPi.GPIO.setwarnings(False)

while True:
    try:
        print 'val: ', RPi.GPIO.input(port)
        time.sleep(0.4)
    except Exception, e:
        pass
RPi.GPIO.cleanup()
