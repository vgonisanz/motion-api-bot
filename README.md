# Bot for telegram using motion library

This bot use a submodule with [motion repository](https://github.com/Motion-Project/motion)

This code has been tested with motion in:

* Fedora distro
* Raspberry pi **TODO**

# Installation

*TODO* requirements.txt

## 3rdParty

This bot and server use motion source code. You can find it in the original github project page or use it as submodule.

1. Get the code (Currently use v4.0)

```
git submodule init
git submodule update
```

1. Compile the code

```
autoreconf -fiv
./configure
make
make install
```

# Files

This bot use a token to be used by telegram api. Make http requests to server if is running.

## Client related

This code shall be used to create a bot using a valid id from fatherbot. vgonisanz use it to create its own motion-api-bot to be used by anyone.
You can get another id and create a similar bot with your own changes.

* **client**: Main script to manage bot. Contain usage and use api file to make all calls to the server.
* **api**: Client to manage telegram python api and make calls to core. Is used by bot script. Use HTTP request to get info from a running server.

## Server related

This code is used to have a server with motion installed to start and stop getting data and other operations.

* **server**: Main script to manage server based on linkero.
* **core**: Client api of linkero to feed bot http requests.

# Design v1

All services can be requested using ```/api/v1```.

# Bot usage

Bot is an instance running in bot computer. It can be host by anyone. You will need to register your server in order to use it thought telegram.

```
cd bot
python client.py
```

# Server usage

Server is an instance running in host computer to manage motion library and using its webcam as defined into configuration file.

Launch server with command:

```
cd server
python server.py
```

Output logs from server example:
```
INFO:werkzeug: * Running on http://0.0.0.0:5000/ (Press CTRL+C to quit)
INFO:werkzeug:127.0.0.1 - - [01/Oct/2017 13:38:42] "GET /cmds HTTP/1.1" 200 -
```

* First line: Where is the server running
* Second line: A GET HTTP request was caught to cmds URL.

# How make client requests

Exist several ways to use the server.

* Curl: This executable (it can be used as library too) have a lot of options to make HTTP requests.
* Python client script: Running client.py sample script, parse args to make requests.

## Curl

### Get request with JSON

* Just running:
```
curl -i -X GET http://localhost:5000/v1/help
```
* More info:
```
curl -i -H "Accept: application/json" -H "Content-Type: application/json" -X GET http://localhost:5000/todos/todo1
```

### Port request

* Just running:
```
curl -i -X POST http://localhost:5000/todos/todo1
```

### put

Put is used to:
```
curl -X PUT -d arg=val -d arg2=val2 localhost:8080
```

### delete

Delete is used to:
```
curl -i -X DELETE http://localhost:3001/api/v1/projects/559a328d8e67197a1c00d6dd
```

#### Using parameters

curl --data "param1=value1&param2=value2" http://hostname/resource

#### File upload

curl --form "fileupload=@filename.txt" http://hostname/resource

# Extra Data

## Curl

* -X: Specifies a custom request method to use when communicating with the HTTP server. Valid: GET, POST, PUT, DELETE
* -H: Extra header to include in the request when sending HTTP to a server.
* -i: Include the HTTP-header in the output.

# Bibliography

* [Python telegram bot wiki](https://github.com/python-telegram-bot/python-telegram-bot/wiki)
* [Introduction to python bot API](https://github.com/python-telegram-bot/python-telegram-bot/wiki/Introduction-to-the-API)
* [My first bot](https://github.com/python-telegram-bot/python-telegram-bot/wiki/Extensions-%E2%80%93-Your-first-Bot)
