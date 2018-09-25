#ifndef CardReader_h
#define CardReader_h

#include <MFRC522.h>

class CardReader
{
    MFRC522 _mfrc522;

public:
    CardReader(
        int pinSS,
        int pinRst
    );
    void setup();
    void loop();
    void readCard();
};

#endif