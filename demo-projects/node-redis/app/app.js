var express = require('express');
var app = express();
var redis = require("redis"),
  client = redis.createClient(6379, 'redis');

app.get('/', function(req, res) {
  var ip = req.connection.remoteAddress;
  console.log('access from IP ' + ip);
  client.multi().rpush('ip', ip);
  res.send('hello ' + ip);
});

app.get('/health', function(req, res) {
  var redisVersion = client.server_info.redis_version;
  if (redisVersion === '3.2.6') {
    res.send({status: 'UP'});
  } else {
    res.status(500).send('v. ' + redisVersion);
  }
});

app.listen(8080, function () {
  console.log('Example app listening on port 8080!');
});