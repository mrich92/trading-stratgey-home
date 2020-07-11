from collections import deque

class MovingAverage():
    def __init__(self, lookback):
        self._queue = deque()
        self._lookback = lookback
        self._running_sum = 0

        self.current_avg = None

    def update(self, price):
        if (len(self._queue) < self._lookback):
            self._queue.append(price)
            self._running_sum += price
        else:
            self._queue.append(price)
            self._running_sum += price
            holder = self._queue.popleft()
            self._running_sum -= holder
            self.current_avg = self._running_sum / self._lookback
