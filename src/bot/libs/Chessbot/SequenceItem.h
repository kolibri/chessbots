#ifndef SequenceItem_h
#define SequenceItem_h

class SequenceItem
{
  public:
    SequenceItem(int speedLeft, int speedRight, int millisEnd):
        _speedLeft(speedLeft),
        _speedRight(speedRight),
        _millisEnd(millisEnd)
        {};
    int _speedLeft;
    int _speedRight;
    int _millisEnd;
};

#endif