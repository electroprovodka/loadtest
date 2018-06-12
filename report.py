import asyncio
from collections import defaultdict
import time


class Report:
    def __init__(self, timer, counter, update_period=1):
        self._timer = timer
        self._counter = counter
        self._report = defaultdict(int)
        self._print_time = time.time()
        self._period = update_period

    def set(self, wid):
        self._report[wid] += 1

    async def current_stats(self):
        count = self._counter.period_count
        success = self._counter.period_success
        current_time = time.time()
        period = current_time - self._print_time
        rps = count / period
        success_rate = round(success / count, 2) if count > 0 else 0

        print(f'\rRPS: {int(rps)} | SUCCESS RATE: {success_rate}', end='')
        self._counter.clear_period_values()
        self._print_time = current_time
        await asyncio.sleep(self._period)

    def full_stats(self):
        workers_stats = sorted(self._report.items(), key=lambda x: x[0])
        workers_str = '\n'.join(map(lambda x: f'Worker #{x[0]}: {x[1]}', workers_stats))
        duration = round(self._timer.current_duration, 3)
        count = self._counter.count
        success_count = self._counter.success_count
        if not count:
            return 'Total runs: 0'
        return f"\nTotal runs: {count}\n" + \
            f"Duration: {duration}\n" + \
            f"RPS: {int(count/duration)}\n" + \
            f"Successes: {success_count}\n" + \
            f"Success Rate: {round(success_count/count, 2)}\n" #+ \
            #f"Runs per worker:\n" + \
            #f"{workers_str}"
