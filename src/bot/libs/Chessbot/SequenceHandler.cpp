#include "SequenceHandler.h"
#include <Sequence.h>
#include <Motor.h>
#include <ESP8266HTTPClient.h>
#include <ArduinoJson.h>

void SequenceHandler::handle(int millis, Sequence sequence, String currentTag){
  if (sequence._expectedTag == "") {
    Serial.println("no expected target (init state)");
      // do nothing, wait for sequence income
    return;
  }

  if (currentTag == sequence._expectedTag) {
    // Lucky case, we are, where we belong
    return;
  }

  int speedLeft = 0;
  int speedRight = 0;

  if(sequence.hasItems(millis)) {
    speedLeft = sequence.current()._speedLeft;
    speedRight = sequence.current()._speedRight;
  } else if(sequence.isFinished(millis)) {
    if (currentTag == "") {
      Serial.println("lost");
        // drive forward until new tag
      sequence.add(millis, SequenceItem(1000,1000,500));
    } else {
      Serial.print("wrong at: ");
      // send request with currentTag to get new sequence
      SequenceHandler::sendPosition(currentTag);
    }
  }

  _motorLeft.control(speedLeft);
  _motorRight.control(speedRight);
}



void SequenceHandler::sendPosition(String tagId){
  StaticJsonBuffer<200> jsonBuffer;
  JsonObject& tagInfo = jsonBuffer.createObject();
  tagInfo["id"] = tagId;

  //debug
  String jsontext;
  tagInfo.printTo(jsontext);
  Serial.println(jsontext);

   HTTPClient http;
 
   http.begin("http://192.168.178.20:8008/tag");
   http.addHeader("Content-Type", "application/json");
 
   int httpCode = http.POST(jsontext);
   String payload = http.getString();
 
   Serial.println(httpCode);
   Serial.println(payload);

  Sequence _sequence(payload);

   http.end();
}

