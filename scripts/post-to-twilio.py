#!/usr/bin/env python

import redis
import uuid
import time
import json
import sys

from twilio.rest import Client

with open(sys.argv[1]) as f:
    config = json.load(f)

rClient = redis.Redis(config['redis']['host'],config['redis']['port'])
rKey = config['redis']['key']

tClient = Client(config['twilio']['accountSid'], config['twilio']['authToken'])
sendToPhoneNumberList = config['twilio']['sendToPhoneNumber']
twilioPhoneNumber = config['twilio']['twilioPhoneNumber']

timestamp = time.time()

bulkDoc = {}

counter = 0


while True:

    list = rClient.zrangebyscore(rKey + '_twilio_ts', '-inf', '+inf', 0, 1)

    if len(list) == 0:
        break

    counter = counter + 1
    print 'Index [' + str(counter) + '] => ' + list[0]
    print list[0]

    bulkDoc = json.loads(rClient.hget(rKey + '_twilio_msg', list[0]))

    msg = "[" + bulkDoc['timestamp'] + "][" + bulkDoc['event_type'] + "]\n\n" + bulkDoc['event_message']

    x = 0
    while x < len(sendToPhoneNumberList):

        message = tClient.messages.create(
            to=sendToPhoneNumberList[x],
            from_=twilioPhoneNumber,
            body=msg)
        x += 1

    rClient.zrem(rKey + '_twilio_ts',list[0])
    rClient.hdel(rKey + '_twilio_msg',list[0])
