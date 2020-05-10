#include <Chessbot.h>

Chessbot chessbot(
    "Trochilidae",
    "humm!ngb!rd31",
    "http://192.168.178.34:8000/bot/register",
    5, // cardReaderRstPin
    2, // cardReaderLeftPin
    4  // cardReaderRightPin
);

void setup() {
    Serial.begin(9600);
    Serial.print("booting...");

    chessbot.setup();
}

void loop() {
    chessbot.loop();
}
