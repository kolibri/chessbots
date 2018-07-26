var http = require('http').createServer(handler); //require http server, and create server with function handler()
var fs = require('fs'); //require filesystem module
var io = require('socket.io')(http) //require socket.io module and pass the http object (server)
var Gpio = require('onoff').Gpio; //include onoff to interact with the GPIO

var motorLeftPin1  = new Gpio(17, 'out');
var motorLeftPin2  = new Gpio(27, 'out');
var motorRightPin1 = new Gpio(23, 'out');
var motorRightPin2 = new Gpio(24, 'out');

http.listen(80);

function handler (req, res) { //create server
    fs.readFile(__dirname + '/index.html', function(err, data) { //read file index.html in public folder
        if (err) {
            res.writeHead(404, {'Content-Type': 'text/html'}); //display 404 on error
            return res.end("404 Not Found");
        } 

        res.writeHead(200, {'Content-Type': 'text/html'}); //write HTML
        res.write(data); //write data from index.html
        return res.end();
    });
}

io.sockets.on('connection', function (socket) {
    socket.on('stop', function(data) {
        motorLeftPin1.writeSync(0);
        motorLeftPin2.writeSync(0);
        motorRightPin1.writeSync(0);
        motorRightPin2.writeSync(0);
    });
    socket.on('forward', function(data) {
        motorLeftPin1.writeSync(0);
        motorLeftPin2.writeSync(1);
        motorRightPin1.writeSync(0);
        motorRightPin2.writeSync(1);
    });
    socket.on('backward', function(data) {
        motorLeftPin1.writeSync(1);
        motorLeftPin2.writeSync(0);
        motorRightPin1.writeSync(1);
        motorRightPin2.writeSync(0);
    });
    socket.on('turnleft', function(data) {
        motorLeftPin1.writeSync(1);
        motorLeftPin2.writeSync(0);
        motorRightPin1.writeSync(0);
        motorRightPin2.writeSync(1);
    });
    socket.on('turnright', function(data) {
        motorLeftPin1.writeSync(0);
        motorLeftPin2.writeSync(1);
        motorRightPin1.writeSync(1);
        motorRightPin2.writeSync(0);
    });
});

process.on('SIGINT', function () { //on ctrl+c
    // turn everything off
    motorLeftPin1.writeSync(0);
    motorLeftPin1.unexport();
    motorLeftPin2.writeSync(0);
    motorLeftPin2.unexport();
    motorRightPin1.writeSync(0);
    motorRightPin1.unexport();
    motorRightPin2.writeSync(0);
    motorRightPin2.unexport();

  process.exit(); //exit completely
});

