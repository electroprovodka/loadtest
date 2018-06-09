from collections import defaultdict


class Report:
    def __init__(self, timer, counter):
        self._timer = timer
        self._counter = counter
        self._report = defaultdict(int)

    def set(self, wid):
        self._report[wid] += 1

    def __str__(self):
        workers_stats = sorted(self._report.items(), key=lambda x: x[0])
        workers_str = '\n'.join(map(lambda x: f'Worker #{x[0]}: {x[1]}', workers_stats))
        duration = self._timer.current_duration
        count = self._counter.count
        success_count = self._counter.success_count
        if not count:
            return 'Total runs: 0'
        return f"Total runs: {count}\n" + \
            f"Duration: {duration}\n" + \
            f"RPS: {int(count/duration)}\n" + \
            f"Successes: {success_count}\n" + \
            f"Success Rate: {round(success_count/count, 2)}\n" + \
            f"Runs per worker:\n" + \
            f"{workers_str}"
