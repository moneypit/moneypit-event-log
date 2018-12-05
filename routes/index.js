var express = require('express');
var child_process = require('child_process');
const bodyParser = require("body-parser");
var router = express.Router();
const crypto = require('crypto');
var _ = require('lodash');


router.get('/', function(req, res, next) {
  res.json(swagger);
});

router.get('/config', function(req, res, next) {
  res.json(config);
});

router.get('/events', function(req, res, next) {

  rClient.hgetall(config.redis.key, function (err, obj) {
    if (err) {
      res.json(err);
    } else {
      var eventList = [];

      for (var k in obj) {
        var parsedObj = JSON.parse(obj[k]);
        parsedObj.timestamp_epoch = Date.parse(parsedObj.timestamp);
        eventList.push(parsedObj);
      }

      var sortedEventList = _.sortBy(eventList, 'timestamp_epoch');

      res.json(sortedEventList.reverse());

    }
  });

});

router.post('/events', function(req, res, next) {

  var stateBody = req.body;
  var date = new Date();
  var timestamp = date.getTime();

  stateBody.timestamp = date;

  var uid = crypto.createHmac('sha256',JSON.stringify(stateBody)).digest('hex');
  stateBody.id = uid;

  rClient.hset(config.redis.key, uid, JSON.stringify(stateBody), function (err, reply) {

  })

  rClient.hset(config.redis.key + '_es_msg', uid, JSON.stringify(stateBody), function (err, reply) {

    var args = [ config.redis.key + '_es_ts', timestamp, uid ];
    rClient.zadd(args, function (err, response) {

    });

  });

  rClient.hset(config.redis.key + '_twilio_msg', uid, JSON.stringify(stateBody), function (err, reply) {

    var args = [ config.redis.key + '_twilio_ts', timestamp, uid ];
    rClient.zadd(args, function (err, response) {

    });

  });

  res.json(stateBody);
});


module.exports = router;
