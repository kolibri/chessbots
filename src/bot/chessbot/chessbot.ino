#include <ESP8266WiFi.h>
#include <ESP8266WebServer.h>
#include <ArduinoJson.h>

const char* ssid = "Trochilidae";
const char* password = "humm!ngb!rd31";

#define MOTOR1_A D6
#define MOTOR1_B D8
#define MOTOR1_PWM 14
#define MOTOR2_A D1
#define MOTOR2_B D4
#define MOTOR2_PWM 4

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
}

void loop() {
    server.handleClient();
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
