#!/usr/bin/env python
# encoding: utf-8

import time
import ConfigParser

import redis

import RPi.GPIO

'''检测是否有人存在，将状态数据发送到服务器'''

cf = ConfigParser.ConfigParser(allow_no_value=True)
try:
    cf.read("./conf.ini")
    port = cf.getint("rspi", 'port')
    interval = cf.getfloat('service', 'send_interval')

    redis_host = cf.get('service', 'host')
    redis_port = cf.getint('service', 'port')
    redis_db = cf.getint('service', 'db')
    desc = cf.get('service', 'description')
    id = cf.get('service', 'id')
    rds = redis.StrictRedis(host=redis_host, port=redis_port, db=redis_db)
    res = rds.hset('dev_info', id, desc)
    print 'new device added' if res == 1 else 'device already registered'

    RPi.GPIO.setmode(RPi.GPIO.BCM)
    RPi.GPIO.setup(port, RPi.GPIO.IN)
    RPi.GPIO.setwarnings(False)
    print 'ready sending detect result to', redis_host, 'at interval of', interval

    while True:
        try:
            rds.hset('dev_value', id, RPi.GPIO.input(port))
            time.sleep(interval)
        except Exception, e:
            print e
            pass
    RPi.GPIO.cleanup()
except Exception, e:
    print e
    exit(1)
