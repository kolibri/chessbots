#include <ESP8266WiFi.h>

const char* ssid = "Trochilidae";
const char* password = "humm!ngb!rd31";
#define MOTOR1_A D1
#define MOTOR1_B D2
#define MOTOR2_A D5
#define MOTOR2_B D6

char* state = "stop";
WiFiServer server(80);

void setup() {
  Serial.begin(115200);
  pinmode(MOTOR1_A, OUTPUT);
  pinmode(MOTOR1_B, OUTPUT);
  pinmode(MOTOR2_A, OUTPUT);
  pinmode(MOTOR2_B, OUTPUT);
  delay(10);

  Serial.print("Connecting to ");
  Serial.println(ssid);
  WiFi.begin(ssid, password);
  
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("WiFi connected");
  
  server.begin();
  Serial.println("Server started");

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
  
  if (req.indexOf("/forward") != -1)
    digitalWrite(MOTOR1_A,HIGH);
    digitalWrite(MOTOR1_B,LOW);
    digitalWrite(MOTOR2_A,HIGH);
    digitalWrite(MOTOR2_B,LOW);
    state = "forward";
  else if (req.indexOf("/backward") != -1)
    digitalWrite(MOTOR1_A,LOW);
    digitalWrite(MOTOR1_B,HIGH);
    digitalWrite(MOTOR2_A,LOW);
    digitalWrite(MOTOR2_B,HIGH);
    state = "backward";
  else if (req.indexOf("/spinleft") != -1)
    digitalWrite(MOTOR1_A,LOW);
    digitalWrite(MOTOR1_B,HIGH);
    digitalWrite(MOTOR2_A,HIGH);
    digitalWrite(MOTOR2_B,LOW);
    state = "spinleft";
  else if (req.indexOf("/spinright") != -1)
    digitalWrite(MOTOR1_A,HIGH);
    digitalWrite(MOTOR1_B,LOW);
    digitalWrite(MOTOR2_A,LOW);
    digitalWrite(MOTOR2_B,HIGH);
    state = "sprinright";
  else if (req.indexOf("/stop") != -1)
    digitalWrite(MOTOR1_A,LOW);
    digitalWrite(MOTOR1_B,LOW);
    digitalWrite(MOTOR2_A,LOW);
    digitalWrite(MOTOR2_B,LOW);
    state = "stop";
  else {
    Serial.println("invalid request");
    client.stop();
    return;
  }

  client.flush();

  // Prepare the response
  String s = "HTTP/1.1 200 OK\r\n";
  s += "Content-Type: application/json\r\n\r\n";
  s += "{\"state\": \"";
  s += state;
  s += "\"}\n";

  // Send the response to the client
  client.print(s);
  delay(1);
  Serial.println("Client disonnected");

  // The client will actually be disconnected 
  // when the function returns and 'client' object is detroyed
}
