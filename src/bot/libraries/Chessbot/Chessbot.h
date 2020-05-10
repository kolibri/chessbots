#ifndef Chessbot_h
#define Chessbot_h

#include <ESP8266WebServer.h>
#include <CardReader.h>

class Chessbot
{
    char* _wifiSsid;
    char* _wifiPass;
    char* _serverUrl;
    ESP8266WebServer _server;
    CardReader cardReaderLeft;
    CardReader cardReaderRight;

public:
    Chessbot(
        char*,
        char*,
        char*,
        int cardReaderRstPin,
        int cardReaderLeftSSPin,
        int cardReaderRightSSPin
        );
    void setup();
    void loop();
    void registerBot();
    void handleTagsRequest();
};

#endif