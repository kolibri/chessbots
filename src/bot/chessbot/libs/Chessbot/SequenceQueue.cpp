#include "SequenceQueue.h"
#include <QueueArray.h>
#include <Sequence.h>


void SequenceQueue::add(int millis, Sequence sequence) {
  if (_queue.isEmpty()) {
    _nextChangeMillis = millis + sequence._millisEnd;
  }

  _queue.enqueue(sequence);
}

Sequence SequenceQueue::current(){
  return _queue.front();
}

bool SequenceQueue::isFinished(int millis) {
  if (!_queue.isEmpty()) {
    return false;
  }

  if (millis > _nextChangeMillis) {
    return true;
  }

  return false;
  // return _queue.isEmpty() && millis > _nextChangeMillis
}

bool SequenceQueue::hasItems(int millis){
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
