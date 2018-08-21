var http = require('http');
var io = require('socket.io')(http);
var fs = require("fs");

var path = require('path');

http.createServer(function (request, response) {
    console.log('request ', request.url);

    var filePath = '.' + request.url;
    if (filePath == './') {
        filePath = './index.html';
    }

    var extname = String(path.extname(filePath)).toLowerCase();
    var mimeTypes = {
        '.html': 'text/html',
        '.js': 'text/javascript',
        '.css': 'text/css'
    };

    var contentType = mimeTypes[extname] || 'application/octet-stream';

    fs.readFile(filePath, function(error, content) {
        if (error) {
            if(error.code == 'ENOENT') {
                response.writeHead(404);
                response.end('Not found', 'utf-8');
            } else {
                response.writeHead(500);
                response.end('Server error');
                response.end();
            }
        }
        else {
            response.writeHead(200, { 'Content-Type': contentType });
            response.end(content, 'utf-8');
        }
    });
}).listen(8030);

io.sockets.on('connection', function (socket) {
    socket.on('stop', function(data) {
    });
});

process.on('SIGINT', function () {
// turn everything off

process.exit();
});
