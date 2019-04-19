# http-server
Simple multi-connection http server

Start the server by running
```
$ python http_server1.py [port]
```
where "port" is a port number >= 1024. 

You can then fetch files from the server using any http client (e.g. browser, telnet, or http-client.py). These files must be .html or .htm and in the same directory as http_server.py. For example, if you start running the server from http://my.server.com on port 10002, and put mypage.html in the same directory, then you can access it on a browser by visiting http://my.server.com:10002/mypage.html

If the file doesn’t exist, the server returns a 404 Not Found HTTP error response. If the file exists but doesn't end with ".htm" or "html", then it responds with 403 Forbidden.

TIP: If you are running the server locally, then you can use the special hostname "localhost" to refer to your own machine, as in: "http://localhost:8000/mypage.html".
