#include <Arduino.h>

// pin to whats on the board mapping for motor controls
#define P_M1_S 15
#define P_M1_A 13
#define P_M1_B 12
//#define P_M2_S 16
//#define P_M2_A 2
//#define P_M2_B 14


const int freq1 = 5000;
const int motor1Channel = 3;
//const int freq2 = 20000;
//const int motor2Channel = 1;

void setup() {
  Serial.begin(115200);
  Serial.setDebugOutput(true);
  Serial.println();
Serial.println("1 loaded");

  // setup pwm pins
  ledcSetup(motor1Channel, freq1, 8);
Serial.println("2 ledcsetup");
  ledcAttachPin(P_M1_S, motor1Channel);
Serial.println("3 atach");

    // register motor pins
  pinMode(P_M1_A, OUTPUT);
  pinMode(P_M1_B, OUTPUT);
Serial.println("4 pinmodes");

    // setup all of
  ledcWrite(motor1Channel, 0);
  digitalWrite(P_M1_A, LOW); // red
  digitalWrite(P_M1_B, LOW); // yellow
Serial.println("register complete");
  delay(1000);


Serial.println("now 1");
  ledcWrite(motor1Channel, 255);
  digitalWrite(P_M1_A, HIGH); // red
  digitalWrite(P_M1_B, LOW); // yellow
  delay(1000);
Serial.println("now 1 end");

Serial.println("now 2");
  ledcWrite(motor1Channel, 127);
  digitalWrite(P_M1_A, HIGH); // red
  digitalWrite(P_M1_B, LOW); // yellow
//  ledcWrite(motor2Channel, 127);
//  digitalWrite(P_M2_A, HIGH); // red
//  digitalWrite(P_M2_B, LOW); // yellow
  delay(1000);


Serial.println("now 3");
  ledcWrite(motor1Channel, 127);
  digitalWrite(P_M1_A, LOW); // red
  digitalWrite(P_M1_B, HIGH); // yellow
//  ledcWrite(motor2Channel, 255);
//  digitalWrite(P_M2_A, LOW); // red
//  digitalWrite(P_M2_B, HIGH); // yellow
  delay(1000);


Serial.println("now 4");
  ledcWrite(motor1Channel, 63);
  digitalWrite(P_M1_A, LOW); // red
  digitalWrite(P_M1_B, HIGH); // yellow
//  ledcWrite(motor2Channel, 63);
//  digitalWrite(P_M2_A, LOW); // red
//  digitalWrite(P_M2_B, HIGH); // yellow
  delay(1000);


Serial.println("now 5");
  ledcWrite(motor1Channel, 31);
  digitalWrite(P_M1_A, LOW); // red
  digitalWrite(P_M1_B, HIGH); // yellow
//^  ledcWrite(motor2Channel, 31);
//^  digitalWrite(P_M2_A, LOW); // red
//^  digitalWrite(P_M2_B, HIGH); // yellow
  delay(1000);



}

void loop() {
  // put your main code here, to run repeatedly:
  delay(10000);
}
