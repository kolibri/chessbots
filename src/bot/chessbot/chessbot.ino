#include <ESP8266HTTPClient.h>
#include <ESP8266WiFi.h>
#include <ESP8266WebServer.h>
#include <ArduinoJson.h>
#include <SPI.h>
#include <MFRC522.h>
#include <Motor.h>

const char* ssid = "Trochilidae";
const char* password = "humm!ngb!rd31";
String jsontext = "[]";

#define SS_PIN 4  //D2
#define RST_PIN 5 //D1

Motor motorLeft(10, 15, 0);
Motor motorRight(3, 16, 2);

MFRC522 mfrc522(SS_PIN, RST_PIN);   // Create MFRC522 instance.
int statuss = 0;
int out = 0;

ESP8266WebServer server(80);

void setup() {
    Serial.begin(115200);
    Serial.print("Connecting to ");
    Serial.println(ssid);
    WiFi.begin(ssid, password);

    while (WiFi.status() != WL_CONNECTED) {
        delay(500);
        Serial.print(".");
    }
    
    server.on("/sequence", handleRequest); 
    server.begin();
    Serial.println("Wifi connected & Server started");

    Serial.println(WiFi.localIP());

    SPI.begin();      // Initiate  SPI bus
    mfrc522.PCD_Init();   // Initiate MFRC522

}

void loop() {
    server.handleClient();
    readCard();
}

void handleRequest() {
      if (server.hasArg("plain")== false){ //Check if body received
        server.send(400, "text/plain", "Client Error: Empty body");

        return;
    }

    StaticJsonBuffer<200> jsonBuffer;

    JsonObject& sequence = jsonBuffer.parseObject(server.arg("plain"));

    if (!sequence.success()) {
        Serial.println("parseObject() failed");
        return;
    }      

    int r = sequence["r"];
    int t = sequence["t"];
    int l = sequence["l"];

    motorLeft.control(l);
    motorRight.control(r);

    server.send(200, "text/plain", "ok");
}

void readCard() 
{
  // Look for new cards
  if ( ! mfrc522.PICC_IsNewCardPresent()) 
  {
    return;
  }
  // Select one of the cards
  if ( ! mfrc522.PICC_ReadCardSerial()) 
  {
    return;
  }
  //Show UID on serialM monitor
  Serial.println();
  Serial.print(" UID tag :");
  String content= "";
  byte letter;
  for (byte i = 0; i < mfrc522.uid.size; i++) 
  {
     Serial.print(mfrc522.uid.uidByte[i] < 0x10 ? " 0" : " ");
     Serial.print(mfrc522.uid.uidByte[i], HEX);
     content.concat(String(mfrc522.uid.uidByte[i] < 0x10 ? " 0" : " "));
     content.concat(String(mfrc522.uid.uidByte[i], HEX));
  }
  content.toUpperCase();

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
