#include <Chessbot.h>

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
