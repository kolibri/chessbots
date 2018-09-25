#ifndef SequenceQueue_h
#define SequenceQueue_h

#include <QueueArray.h>
#include <Sequence.h>

class SequenceQueue
{
  QueueArray<Sequence> _queue;
  int _nextChangeMillis;
  public:
    SequenceQueue(){};
    void add(int, Sequence);
    Sequence current();
    bool hasItems(int);
};

#endif