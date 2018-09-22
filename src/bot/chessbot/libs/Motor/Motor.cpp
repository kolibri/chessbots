#include <ESP8266WiFi.h>
#include "Motor.h"

Motor::Motor(int pinA, int pinB, int pinPwm)
{
  _pinA = pinA;
  _pinB = pinB;
  _pinPwm = pinPwm;
}

void Motor::setup(){
  pinMode(_pinA, OUTPUT);
  pinMode(_pinB, OUTPUT);
  pinMode(_pinPwm, OUTPUT);

  digitalWrite(_pinA, LOW);
  digitalWrite(_pinB, LOW);
  analogWrite(_pinPwm, 0);
}

void Motor::control(int val)
{
    analogWrite(_pinPwm,abs(val));
    digitalWrite(_pinA,LOW);
    digitalWrite(_pinB,LOW);

    if (0 < val) {
        digitalWrite(_pinA,HIGH);
    }

    if (0 > val) {
        digitalWrite(_pinB,HIGH);
    }
}
