var http = require('http').createServer(handler); //require http server, and create server with function handler()
var fs = require('fs'); //require filesystem module
var io = require('socket.io')(http) //require socket.io module and pass the http object (server)
var Gpio = require('onoff').Gpio; //include onoff to interact with the GPIO

const mfrc522 = require("mfrc522-rpi");
mfrc522.initWiringPi(0);

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


    socket.on('nfc_write', function(data){
        mfrc522.reset();
        let response = mfrc522.findCard();
        if (!response.status) {
            socket.emit('nfc_status', "No Card");
            return;
        }

        console.log("Card detected, CardType: " + response.bitSize);
        response = mfrc522.getUid();

        if (!response.status) {
            socket.emit('nfc_status', "UID Scan Error");
            return;
        }

        const uid = response.data;
        console.log("Card read UID: %s %s %s %s", uid[0].toString(16), uid[1].toString(16), uid[2].toString(16), uid[3].toString(16));

        data = [0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00];
        mfrc522.writeDataToBlock(8, data);

        socket.emit('nfc_status', "Data writen");
    });


/*
setInterval(function(){
mfrc522.reset();

let response = mfrc522.findCard();
if (!response.status) {
socket.emit('nfc_status', "No Card");
return;
}

response = mfrc522.getUid();
if (!response.status) {
socket.emit('nfc_status', "UID Scan Error");
return;
}

const uid = response.data;
socket.emit('nfc_status', 'Card read UID: ' + uid[0].toString(16) + ' ' + uid[1].toString(16) + ' ' + uid[2].toString(16) + ' ' + uid[3].toString(16));
socket.emit('nfc_read', "Block: 8 Data: " + mfrc522.getDataForBlock(8));
mfrc522.stopCrypto();
}, 500);
*/
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

