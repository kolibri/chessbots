#ifndef Chessbot_h
#define Chessbot_h

#include <ESP8266WebServer.h>

class Chessbot
{
    char* _wifiSsid;
    char* _wifiPass;
    char* _serverUrl;
    ESP8266WebServer _server;

public:
    Chessbot(
        char*,
        char*,
        char*
        );
    void setup();
    void loop();
    void registerBot();
    void handleTagsRequest();
};

#endif