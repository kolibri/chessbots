#ifndef Sequence_h
#define Sequence_h

#include <QueueArray.h>
#include <SequenceItem.h>

class Sequence
{
  QueueArray<SequenceItem> _queue;
  int _nextChangeMillis;
  public:
    Sequence(){};
    void add(int, SequenceItem);
    SequenceItem current();
    bool isFinished(int);
    bool hasItems(int);
};

#endif