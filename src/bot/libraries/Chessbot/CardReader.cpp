#include "CardReader.h"
#include <SPI.h>
#include <MFRC522.h>

CardReader::CardReader(
    int pinSS,
    int pinRst
):
_mfrc522(pinSS, pinRst)
{}

void CardReader::setup() {
    SPI.begin();
    _mfrc522.PCD_Init();


     _mfrc522.PCD_SetAntennaGain(MFRC522::PCD_RxGain::RxGain_max);

    // Dump some debug information to the serial monitor
    Serial.print(F("Reader #"));
    Serial.print(F(". Antenna strength: "));
    Serial.print(_mfrc522.PCD_GetAntennaGain());
    Serial.print(F(". Version : "));
    _mfrc522.PCD_DumpVersionToSerial();

    delay(100);
}

String CardReader::readCard() 
{
  Serial.println("rc");
  // Look for new cards
  if ( ! _mfrc522.PICC_IsNewCardPresent()) 
  {
    return "";
  }

  Serial.println("pisnc");
  // Select one of the cards
  if ( ! _mfrc522.PICC_ReadCardSerial()) 
  {
    return "";
  }
  Serial.println("prcs");

  String content= "";
  byte letter;
  for (byte i = 0; i < _mfrc522.uid.size; i++) 
  {
     content.concat(String(_mfrc522.uid.uidByte[i] < 0x10 ? " 0" : " "));
     content.concat(String(_mfrc522.uid.uidByte[i], HEX));
  }
  content.toUpperCase();
  content.trim();

      Serial.println(content);

delay(100);

  return content;
}

