#!/usr/bin/env python

import redis
import uuid
import time
import json
import sys

from elasticsearch import Elasticsearch

with open(sys.argv[1]) as f:
    config = json.load(f)

print config

rClient = redis.Redis(config['redis']['host'],config['redis']['port'])
esClient = Elasticsearch(config['elasticsearch']['hosts'],verify_certs=False)
rKey = config['redis']['key']

timestamp = time.time()

bulkDoc = {}

counter = 0

while True:

    list = rClient.zrangebyscore(rKey + '_es_ts', '-inf', '+inf', 0, 1)

    if len(list) == 0:
        break

    counter = counter + 1
    print 'Index [' + str(counter) + '] => ' + list[0]
    print list[0]

    bulkDoc = json.loads(rClient.hget(rKey + '_es_msg', list[0]))

    print bulkDoc

    r = esClient.index(index=config['elasticsearch']['index'], doc_type=config['elasticsearch']['index'], body=bulkDoc)

    rClient.zrem(rKey + '_es_ts',list[0])
    rClient.hdel(rKey + '_es_msg',list[0])
