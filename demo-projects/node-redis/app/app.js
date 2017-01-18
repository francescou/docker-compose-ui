const express = require('express');
const redis = require("redis");

const app = express();
const client = redis.createClient(6379, 'redis');

app.get('/', (req, res) => {
  const ip = req.connection.remoteAddress;
  console.log(`access from IP ${ip}`);
  client.multi().rpush('ip', ip);
  res.send(`hello ${ip}`);
});

app.get('/health', (req, res) => {
  const redisVersion = client.server_info.redis_version;
  if (redisVersion.startsWith('3')) {
    res.send({status: 'UP'});
  } else {
    res.status(500).send(`version ${redisVersion}`);
  }
});

app.listen(8080, () => {
  console.log('Example app listening on port 8080!');
});