#include "Chessbot.h"
#include <ESP8266WiFi.h>
#include <ESP8266HTTPClient.h>
#include <ESP8266WebServer.h>
#include <CardReader.h>

Chessbot::Chessbot(
  char* wifiSsid,
  char* wifiPass,
  char* serverUrl,
  int cardReaderRstPin,
  int cardReaderLeftSSPin,
  int cardReaderRightSSPin
  ):
_wifiSsid(wifiSsid),
_wifiPass(wifiPass),
_serverUrl(serverUrl),
_server(80),
cardReaderLeft(cardReaderLeftSSPin, cardReaderRstPin),
cardReaderRight(cardReaderRightSSPin, cardReaderRstPin)
{}

void Chessbot::setup() {
  cardReaderLeft.setup();
  cardReaderRight.setup();


  Serial.print("Connecting to ");
  Serial.println(_wifiSsid);
  WiFi.begin(_wifiSsid, _wifiPass);

  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }


  _server.on("/tags", std::bind(&Chessbot::handleTagsRequest, this)); 
  _server.onNotFound(std::bind(&Chessbot::handleTagsRequest, this));        // When a client requests an unknown URI (i.e. something other than "/"), call function "handleNotFound"

  _server.begin();

  Serial.println("Wifi connected & Server started");
  Serial.println(WiFi.localIP());

  delay(1000);
  registerBot();
}

void Chessbot::loop()
{
      _server.handleClient();


  String tagLeft = cardReaderLeft.readCard();
  String tagRight = cardReaderRight.readCard();

  //Serial.print("Tag left");
  //Serial.println(tagLeft);

  //Serial.print("Tag right");
  //Serial.println(tagRight);

}

void Chessbot::registerBot() {
  Serial.println("Registering bot");
  HTTPClient http;
  http.begin(_serverUrl);
  
  int httpCode = http.GET();

  if (httpCode > 0) {
    Serial.printf("Response from register: %s\n", http.getString().c_str());
  }
  else {
    Serial.printf("Request failed: %s\n", http.errorToString(httpCode).c_str());
  }
  
  http.end();
  Serial.println("Bot registered");
}


void Chessbot::handleTagsRequest() {
  Serial.println("Reqested tags");

  _server.send(200, "application/json", "{\"left_tag\": \"left_tag\",\"right_tag\": \"right_tag\" }");
}
