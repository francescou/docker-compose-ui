var http = require('http');
var redis = require("redis"),
  client = redis.createClient(6379, 'redis');

client.on("error", function (err) {
  console.log("Error " + err);
});

http.createServer(function (req, res) {
  res.writeHead(200, {'Content-Type': 'text/plain'});
  var ip = req.connection.remoteAddress;
  console.log('access from IP ' + ip);
  client.multi().rpush('ip', ip);
  res.end('Hello ' + ip);
}).listen(8080, '0.0.0.0');
