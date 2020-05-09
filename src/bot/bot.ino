#include <Chessbot.h>

Chessbot chessbot(
    "Trochilidae",
    "humm!ngb!rd31",
    "http://192.168.178.36:8000/bot/register"
);

void setup() {
    Serial.begin(9600);
    Serial.print("booting...");

    chessbot.setup();
}

void loop() {
    chessbot.loop();
}
