#include "Chessbot.h"
#include <ESP8266WiFi.h>
#include <ESP8266HTTPClient.h>

Chessbot::Chessbot(
    char* wifiSsid,
    char* wifiPass,
    char* serverUrl
):
_wifiSsid(wifiSsid),
_wifiPass(wifiPass),
_serverUrl(serverUrl)
{}

void Chessbot::setup() {
      Serial.print("Connecting to ");
      Serial.println(_wifiSsid);
      WiFi.begin(_wifiSsid, _wifiPass);

      while (WiFi.status() != WL_CONNECTED) {
          delay(500);
          Serial.print(".");
      }

      Serial.println("Wifi connected & Server started");
      Serial.println(WiFi.localIP());
      delay(1000);
      registerBot();
}

void Chessbot::loop()
{
}

void Chessbot::registerBot() {
  Serial.print("registerBot");
  HTTPClient http;
  http.begin(_serverUrl);
  
  int httpCode = http.GET();

  if (httpCode > 0) {
    Serial.println(http.getString());
  }
  else {
    Serial.printf("Request failed: %s\n", http.errorToString(httpCode).c_str());
  }
  
  http.end();
}