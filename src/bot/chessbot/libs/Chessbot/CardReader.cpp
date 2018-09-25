#include "CardReader.h"
#include <ESP8266HTTPClient.h>
#include <ArduinoJson.h>
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

void CardReader::loop()
{
    CardReader::readCard();
}

void CardReader::readCard() 
{
  // Look for new cards
  if ( ! _mfrc522.PICC_IsNewCardPresent()) 
  {
    return;
  }
  // Select one of the cards
  if ( ! _mfrc522.PICC_ReadCardSerial()) 
  {
    return;
  }
  //Show UID on serialM monitor
  Serial.println();
  Serial.print(" UID tag :");
  String content= "";
  byte letter;
  for (byte i = 0; i < _mfrc522.uid.size; i++) 
  {
     Serial.print(_mfrc522.uid.uidByte[i] < 0x10 ? " 0" : " ");
     Serial.print(_mfrc522.uid.uidByte[i], HEX);
     content.concat(String(_mfrc522.uid.uidByte[i] < 0x10 ? " 0" : " "));
     content.concat(String(_mfrc522.uid.uidByte[i], HEX));
  }
  content.toUpperCase();
  String jsontext;

  StaticJsonBuffer<200> jsonBuffer;
  JsonObject& tagInfo = jsonBuffer.createObject();
  tagInfo["id"] = content.substring(1);
  tagInfo.printTo(jsontext);

  Serial.println(jsontext);

   HTTPClient http;    //Declare object of class HTTPClient
 
   http.begin("http://192.168.178.20:8008/tag");      //Specify request destination
   http.addHeader("Content-Type", "application/json");  //Specify content-type header
 
   int httpCode = http.POST(jsontext);   //Send the request
   String payload = http.getString();                  //Get the response payload
 
   Serial.println(httpCode);   //Print HTTP return code
   Serial.println(payload);    //Print request response payload
 
   http.end();  //Close connection
} 
