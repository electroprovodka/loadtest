from collections import defaultdict

import time


class Report:
    def __init__(self):
        self._report = defaultdict(list)
        self._success = 0
        self._fail = 0
        self._counter = 0
        self._start = time.time()

    def success(self):
        self._counter += 1
        self._success += 1

    def fail(self):
        self._fail += 1
        self._counter += 1

    def set(self, key, value):
        self._report[key].append(value)

    def __str__(self):
        workers_stats = sorted([(key, len(value)) for key, value in self._report.items()], key=lambda x: x[0])
        workers_str = '\n'.join(map(lambda x: f'Worker #{x[0]}: {x[1]}', workers_stats))
        duration = time.time() - self._start
        return f"Total runs: {self._counter}\n" + \
            f"Duration: {duration}\n" + \
            f"RPS: {int(self._counter/duration)}\n" + \
            f"Successes: {self._success}\n" + \
            f"Success Rate: {round(self._success/self._counter, 4)}\n" + \
            f"Stats per worker:\n" + \
            f"{workers_str}"
