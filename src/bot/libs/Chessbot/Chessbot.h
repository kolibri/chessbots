#ifndef Chessbot_h
#define Chessbot_h

#include <Motor.h>
#include <ESP8266WebServer.h>
#include <CardReader.h>
#include <Sequence.h>

class Chessbot
{
    Motor _motorLeft;
    Motor _motorRight;
    CardReader _cardReader;
    ESP8266WebServer _server;
    char* _wifiSsid;
    char* _wifiPass;
    String jsontext = "[]";
    Sequence _sequence;
    int _nextChangeMillis;
    String _expectedTag;

public:
    Chessbot(
        int pinMotorLeftA,
        int pinMotorLeftB,
        int pinMotorLeftPwm,
        int pinMotorRightA,
        int pinMotorRightB,
        int pinMotorRightPwm,
        int pinSS,
        int pinRst,
        int serverPort,
        char*,
        char*
        );
    void setup();
    void loop();
    void handleRequest();
};

#endif