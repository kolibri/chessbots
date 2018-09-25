#ifndef Sequence_h
#define Sequence_h

#include "Arduino.h"

class Sequence
{
  public:
    Sequence(int speedLeft, int speedRight, int millisEnd):
        _speedLeft(speedLeft),
        _speedRight(speedRight),
        _millisEnd(millisEnd)
        {};
    int _speedLeft;
    int _speedRight;
    int _millisEnd;
};

#endif