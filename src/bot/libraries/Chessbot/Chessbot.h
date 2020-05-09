#ifndef Chessbot_h
#define Chessbot_h


class Chessbot
{
    char* _wifiSsid;
    char* _wifiPass;
    char* _serverUrl;

public:
    Chessbot(
        char*,
        char*,
        char*
        );
    void setup();
    void loop();
    void registerBot();
};

#endif