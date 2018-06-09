import time


class Timer:
    def __init__(self, duration=None):
        self.duration = duration
        self.time = time.time()

    @property
    def finished(self):
        if self.duration is None:
            return False
        return time.time() - self.time > self.duration
