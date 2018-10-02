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
}

String CardReader::readCard() 
{
  // Look for new cards
  if ( ! _mfrc522.PICC_IsNewCardPresent()) 
  {
    return "";
  }
  // Select one of the cards
  if ( ! _mfrc522.PICC_ReadCardSerial()) 
  {
    return "";
  }

  String content= "";
  byte letter;
  for (byte i = 0; i < _mfrc522.uid.size; i++) 
  {
     content.concat(String(_mfrc522.uid.uidByte[i] < 0x10 ? " 0" : " "));
     content.concat(String(_mfrc522.uid.uidByte[i], HEX));
  }
  content.toUpperCase();
  content.trim();

  return content;
}

