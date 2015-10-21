#!/usr/bin/env python
# encoding=utf8
import time
from threading import Thread

import RPi.GPIO


def singleton(cls, *args, **kw):
    instances = {}

    def _singleton():
        if cls not in instances:
            instances[cls] = cls(*args, **kw)
        return instances[cls]

    return _singleton

class Worker(Thread):
    def __init__(self):
        Thread.__init__(self)
        self.d = 0
        self.running = True
        self.PORT = 15
        RPi.GPIO.setmode(RPi.GPIO.BCM)
        RPi.GPIO.setup(self.PORT, RPi.GPIO.OUT)
        RPi.GPIO.setwarnings(False)

    def run(self):
        while self.running:
            self.repeat(10, self.d)
            #time.sleep(0.05)
        self.clean()

    def clean(self):
        RPi.GPIO.cleanup()

    def loop(self, d):
        """本函数执行一个周期，即20ms，d：范围[-10,10]，脉冲宽度[0.5ms, 2.5ms]"""
        d += 14
        RPi.GPIO.output(self.PORT, True)
        time.sleep(0.0001 * d)
        RPi.GPIO.output(self.PORT, False)
        time.sleep(0.02 - 0.0001 * d)

    def repeat(self, n, d):
        while n > 0:
            self.loop(d)
            n -= 1


class Shrief(Thread):
    def __init__(self, worker, t, d):
        Thread.__init__(self)
        self.worker = worker
        self.t = t
        self.d = d

    def run(self):
        self.worker.d = self.d
        time.sleep(self.t)
        self.worker.d = 0


@singleton
class MoterManager():
    def __init__(self):
        self.worker = None

    def start(self):
        self.worker = Worker()
        self.worker.start()

    def stop(self):
        self.worker.running = False
        self.worker.join()

    def isrunning(self):
        return self.worker.running

    def runfor(self, t, d):
        if not self.worker or not self.worker.running:
            print "need to start worker first."
            return
        Shrief(self.worker, t, d).start()




if __name__ == '__main__':
    m = MoterManager()
    m.start()
    print 'starting, run for 3s'
    m.runfor(2, 1)
    print 'main now sleep 6s'
    time.sleep(4)

    m.runfor(2, -1)
    time.sleep(4)

    print "main said stop"
    m.stop()
    print 'stopped'


