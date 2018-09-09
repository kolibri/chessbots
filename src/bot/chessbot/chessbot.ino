#include <ESP8266HTTPClient.h>
#include <ESP8266WiFi.h>
#include <ESP8266WebServer.h>
#include <ArduinoJson.h>
#include <SPI.h>
#include <MFRC522.h>

const char* ssid = "Trochilidae";
const char* password = "humm!ngb!rd31";
String jsontext = "[]";

#define MOTOR1_A 10    // SD3
#define MOTOR1_B 15    // D8
#define MOTOR1_PWM 0  // D3

#define MOTOR2_A 3     // rx
#define MOTOR2_B 16     // d0
#define MOTOR2_PWM 2   // D4

#define SS_PIN 4  //D2
#define RST_PIN 5 //D1


MFRC522 mfrc522(SS_PIN, RST_PIN);   // Create MFRC522 instance.
int statuss = 0;
int out = 0;

ESP8266WebServer server(80);

void setup() {
    Serial.begin(115200);

    pinMode(MOTOR1_A, OUTPUT);
    pinMode(MOTOR1_B, OUTPUT);
    pinMode(MOTOR1_PWM, OUTPUT);
    pinMode(MOTOR2_A, OUTPUT);
    pinMode(MOTOR2_B, OUTPUT);
    pinMode(MOTOR2_PWM, OUTPUT);

    digitalWrite(MOTOR1_A, LOW);
    digitalWrite(MOTOR1_B, LOW);
    analogWrite(MOTOR1_PWM, 0);
    digitalWrite(MOTOR2_A, LOW);
    digitalWrite(MOTOR2_B, LOW);
    analogWrite(MOTOR2_PWM, 0);

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
    int l = sequence["l"];
    int t = sequence["t"];

    controlMotor(r, MOTOR2_A, MOTOR2_B, MOTOR2_PWM);
    controlMotor(l, MOTOR1_A, MOTOR1_B, MOTOR1_PWM);

    server.send(200, "text/plain", "ok");
}

void controlMotor(int val, int ma, int mb, int mpwm) {
    analogWrite(mpwm,abs(val));
    digitalWrite(ma,LOW);
    digitalWrite(mb,LOW);

    if (0 < val) {
        digitalWrite(ma,HIGH);
    }

    if (0 > val) {
        digitalWrite(mb,HIGH);
    }
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
