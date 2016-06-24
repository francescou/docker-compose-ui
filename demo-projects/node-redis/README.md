IP Logger
---
Simple **NodeJS** application that logs visitor IP address on a **Redis db**.

open <http://localhost:8080/> and check the logs


```
http.createServer(function (req, res) {
  res.writeHead(200, {'Content-Type': 'text/plain'});
  var ip = req.connection.remoteAddress;
  redis.createClient(6379, 'redis').multi().rpush('ip', ip);
}).listen(8080, '0.0.0.0');
```
