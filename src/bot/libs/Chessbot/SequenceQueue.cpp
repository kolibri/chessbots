#include "Sequence.h"
#include <QueueArray.h>
#include <SequenceItem.h>


void Sequence::add(int millis, SequenceItem sequenceItem) {
  if (_queue.isEmpty()) {
    _nextChangeMillis = millis + sequenceItem._millisEnd;
  }

  _queue.enqueue(sequenceItem);
}

SequenceItem Sequence::current(){
  return _queue.front();
}

bool Sequence::isFinished(int millis) {
  if (!_queue.isEmpty()) {
    return false;
  }

  if (millis > _nextChangeMillis) {
    return true;
  }

  return false;
  // return _queue.isEmpty() && millis > _nextChangeMillis
}

bool Sequence::hasItems(int millis){
  if (_queue.isEmpty()) {
    return false;
  }

  if (millis > _nextChangeMillis) {
    _queue.dequeue();

    if(!_queue.isEmpty()) {
      _nextChangeMillis = millis + _queue.front()._millisEnd;
    }
  }

  return !_queue.isEmpty();
}
