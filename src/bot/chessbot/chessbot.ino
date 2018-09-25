#include <ESP8266WebServer.h>
#include <MFRC522.h>
#include <Motor.h>
#include <Chessbot.h>

Motor motorLeft(10,15,0);
Motor motorRight(3,16,2);
//MFRC522 mfrc522(4,5);
//ESP8266WebServer server(80);

//Chessbot chessbot = {server};

Chessbot chessbot(
    3, 16, 2,
    10, 15, 0,
    4, 5, 
    80,
    "Trochilidae", "humm!ngb!rd31"
);


void setup() {
    Serial.begin(115200);

    chessbot.setup();
}

void loop() {
    chessbot.loop();
}
