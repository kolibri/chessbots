#include <ESP8266WiFi.h>

const char* ssid = "Trochilidae";
const char* password = "humm!ngb!rd31";

#define MOTOR1_A D6
#define MOTOR1_B D8
#define MOTOR1_PWM D5
#define MOTOR2_A D1
#define MOTOR2_B D4
#define MOTOR2_PWM D2

WiFiServer server(80);

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

    server.begin();
    Serial.println("Wifi connected & Server started");

    Serial.println(WiFi.localIP());
}

void loop() {
    WiFiClient client = server.available();
    if (!client) {
        return;
    }

    Serial.println("new client");
    while(!client.available()){
        delay(1);
    }

    String req = client.readStringUntil('\r');
    Serial.println(req);
    client.flush();

    if (req.indexOf("/-255:-255") != -1) {
        controlMotor(-255, MOTOR1_A, MOTOR1_B, MOTOR1_PWM);
        controlMotor(-255, MOTOR2_A, MOTOR2_B, MOTOR2_PWM);
    } else if (req.indexOf("/255:255") != -1) {
        controlMotor(255, MOTOR1_A, MOTOR1_B, MOTOR1_PWM);
        controlMotor(255, MOTOR2_A, MOTOR2_B, MOTOR2_PWM);
    } else if (req.indexOf("/-255:255") != -1) {
        controlMotor(-255, MOTOR1_A, MOTOR1_B, MOTOR1_PWM);
        controlMotor(255, MOTOR2_A, MOTOR2_B, MOTOR2_PWM);
    } else if (req.indexOf("/255:-255") != -1) {
        controlMotor(255, MOTOR1_A, MOTOR1_B, MOTOR1_PWM);
        controlMotor(-255, MOTOR2_A, MOTOR2_B, MOTOR2_PWM);
  
    } else if (req.indexOf("/-127:-127") != -1) {
        controlMotor(-127, MOTOR1_A, MOTOR1_B, MOTOR1_PWM);
        controlMotor(-127, MOTOR2_A, MOTOR2_B, MOTOR2_PWM);
    } else if (req.indexOf("/127:127") != -1) {
        controlMotor(127, MOTOR1_A, MOTOR1_B, MOTOR1_PWM);
        controlMotor(127, MOTOR2_A, MOTOR2_B, MOTOR2_PWM);
    } else if (req.indexOf("/-127:127") != -1) {
        controlMotor(-127, MOTOR1_A, MOTOR1_B, MOTOR1_PWM);
        controlMotor(127, MOTOR2_A, MOTOR2_B, MOTOR2_PWM);
    } else if (req.indexOf("/127:-127") != -1) {
        controlMotor(127, MOTOR1_A, MOTOR1_B, MOTOR1_PWM);
        controlMotor(-127, MOTOR2_A, MOTOR2_B, MOTOR2_PWM);
  
    } else if (req.indexOf("/-64:-64") != -1) {
        controlMotor(-64, MOTOR1_A, MOTOR1_B, MOTOR1_PWM);
        controlMotor(-64, MOTOR2_A, MOTOR2_B, MOTOR2_PWM);
    } else if (req.indexOf("/64:64") != -1) {
        controlMotor(64, MOTOR1_A, MOTOR1_B, MOTOR1_PWM);
        controlMotor(64, MOTOR2_A, MOTOR2_B, MOTOR2_PWM);
    } else if (req.indexOf("/-64:64") != -1) {
        controlMotor(-64, MOTOR1_A, MOTOR1_B, MOTOR1_PWM);
        controlMotor(64, MOTOR2_A, MOTOR2_B, MOTOR2_PWM);
    } else if (req.indexOf("/64:-64") != -1) {
        controlMotor(64, MOTOR1_A, MOTOR1_B, MOTOR1_PWM);
        controlMotor(-64, MOTOR2_A, MOTOR2_B, MOTOR2_PWM);
 
    } else if (req.indexOf("/-192:-192") != -1) {
        controlMotor(-192, MOTOR1_A, MOTOR1_B, MOTOR1_PWM);
        controlMotor(-192, MOTOR2_A, MOTOR2_B, MOTOR2_PWM);
    } else if (req.indexOf("/192:192") != -1) {
        controlMotor(192, MOTOR1_A, MOTOR1_B, MOTOR1_PWM);
        controlMotor(192, MOTOR2_A, MOTOR2_B, MOTOR2_PWM);
    } else if (req.indexOf("/-192:192") != -1) {
        controlMotor(-192, MOTOR1_A, MOTOR1_B, MOTOR1_PWM);
        controlMotor(192, MOTOR2_A, MOTOR2_B, MOTOR2_PWM);
    } else if (req.indexOf("/192:-192") != -1) {
        controlMotor(192, MOTOR1_A, MOTOR1_B, MOTOR1_PWM);
        controlMotor(-192, MOTOR2_A, MOTOR2_B, MOTOR2_PWM);
    
    } else if (req.indexOf("/0:0") != -1) {
        controlMotor(0, MOTOR1_A, MOTOR1_B, MOTOR1_PWM);
        controlMotor(0, MOTOR2_A, MOTOR2_B, MOTOR2_PWM);
    } else {
        Serial.println("invalid request");
        client.stop();
        return;
    }

    client.flush();

// Prepare the response
    String s = "HTTP/1.1 200 OK\r\n";
    s += "Content-Type: application/json\r\n\r\n";
    s += "{\"state\": \"ok\"}\n";

// Send the response to the client
    client.print(s);
    delay(1);
    Serial.println("Client disonnected");

// The client will actually be disconnected 
// when the function returns and 'client' object is detroyed
}

void controlMotor(int val, int ma, int mb, int mpwm) {
    analogWrite(mpwm,val);

    if (0 < val) {
        digitalWrite(ma,HIGH);
        digitalWrite(mb,LOW);

        return;
    }

    if (0 > val) {
        digitalWrite(ma,LOW);
        digitalWrite(mb,HIGH);

        return;
    }

    digitalWrite(ma,LOW);
    digitalWrite(mb,LOW);

    return;
}

