#ifndef Motor_h
#define Motor_h

#include "Arduino.h"

class Motor
{
  public:
    Motor(int pinA, int pinB, int pinPwm):
        _pinA(pinA), _pinB(pinB), _pinPwm(pinPwm) {};

    void setup();
    void control(int val);
  private:
    int _pinA;
    int _pinB;
    int _pinPwm;
};

#endif