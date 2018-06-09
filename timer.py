import time


class Timer:
    def __init__(self, duration=None):
        self._duration = duration
        self._time = time.time()

    @property
    def finished(self):
        if self._duration is None:
            return False
        return time.time() - self._time > self._duration

    @property
    def start_time(self):
        return self._time

    @property
    def duration(self):
        return self._duration

    @property
    def current_duration(self):
        return time.time() - self._time
