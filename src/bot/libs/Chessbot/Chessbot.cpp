#include "Chessbot.h"
#include <ESP8266WiFi.h>
#include <ESP8266WebServer.h>
#include <ArduinoJson.h>
#include <CardReader.h>
#include <Motor.h>
#include <SequenceQueue.h>

Chessbot::Chessbot(
    int pinMotorLeftA,
    int pinMotorLeftB,
    int pinMotorLeftPwm,
    int pinMotorRightA,
    int pinMotorRightB,
    int pinMotorRightPwm,
    int pinSS,
    int pinRst,
    int serverPort,
    char* wifiSsid,
    char* wifiPass
):
_motorLeft(pinMotorLeftA, pinMotorLeftB, pinMotorLeftPwm),
_motorRight(pinMotorRightA, pinMotorRightB, pinMotorRightPwm),
_cardReader(pinSS, pinRst),
_server(serverPort),
_wifiSsid(wifiSsid),
_wifiPass(wifiPass),
_nextChangeMillis(0),
_expectedTag("")
{}

void Chessbot::setup() {
    _motorLeft.setup();
    _motorRight.setup();
    _cardReader.setup();

      Serial.print("Connecting to ");
      Serial.println(_wifiSsid);
      WiFi.begin(_wifiSsid, _wifiPass);

      while (WiFi.status() != WL_CONNECTED) {
          delay(500);
          Serial.print(".");
      }

      _server.on("/sequence", std::bind(&Chessbot::handleRequest, this)); 
      _server.begin();

      Serial.println("Wifi connected & Server started");
      Serial.println(WiFi.localIP());
}

void Chessbot::loop()
{
    _server.handleClient();
    String tagId = _cardReader.readCard();

    int speedLeft = 0;
    int speedRight = 0;

    if(_sequenceQueue.hasItems(millis())) {
      speedLeft = _sequenceQueue.current()._speedLeft;
      speedRight = _sequenceQueue.current()._speedRight;
    } else if(_sequenceQueue.isFinished(millis())) {
      if (_expectedTag == "") {
        Serial.println("no expected target (init state)");
        // do nothing, wait for sequence income
        return;
      }

      if (tagId == "") {
//        Serial.println("lost");
        // drive forward until new tag
      }

      if (tagId == _expectedTag) {
        Serial.print("right at: ");
        return;
      }

      Serial.print("wrong at: ");
      // send request with tagId to get new sequence
    }

    Serial.print("'");
    Serial.print(tagId);
    Serial.print("'");
    Serial.println();
    Serial.print("Should be at ");
    Serial.print("'");
    Serial.print(_expectedTag);
    Serial.print("'");
    Serial.println();

    _motorLeft.control(speedLeft);
    _motorRight.control(speedRight);
}

void Chessbot::handleRequest() {
      if (_server.hasArg("plain")== false){
        _server.send(400, "text/plain", "Client Error: Empty body");

        return;
    }


    StaticJsonBuffer<2000> jsonBuffer;
    JsonObject& request = jsonBuffer.parseObject(_server.arg("plain"));

    if (!request.success()) {
        Serial.println("parseObject() failed");
        return;
    }
    const char* targetTag = request["tag"];
    _expectedTag = targetTag;
//    _expectedTag = request["tag"];
    JsonArray& sequences = request["sequence"];

    for(auto sequence: sequences) {
        int r = sequence["r"];
        int l = sequence["l"];
        int t = sequence["t"];
        Serial.println("Add new sequence");
        Serial.print(l);
        Serial.print(":");
        Serial.print(r);
        Serial.print(":");
        Serial.print(t);

        Sequence newSequence(l, r, t);
        _sequenceQueue.add(millis(), newSequence);
    }
    _server.send(200, "text/plain", "ok");
}
