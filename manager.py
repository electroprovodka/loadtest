import asyncio
import time

from counter import Counter
from timer import Timer
from utils import Cancel


class Manager:
    def __init__(self, duration=None, max_runs=None, max_runs_per_worker=None):
        self._counter = Counter(max_runs=max_runs, max_runs_per_worker=max_runs_per_worker)

        self._timer = Timer(duration=duration)
        self._cancel = Cancel()

        self._print_time = time.time()
        self._period = 1 #update_period

    def inc(self, wid):
        self._counter.inc(wid)

    def store_result(self, value):
        self._counter.store_result(value)

    def cancel(self):
        self._cancel.cancel()

    def finished(self, wid=None):
        return self._counter.reached(wid) or self._timer.finished or self._cancel.cancelled

    async def current_stats(self):
        while not self.finished():
            count = self._counter.period_count
            results = self._counter.period_results

            current_time = time.time()
            period = current_time - self._print_time
            rps = count / period

            items = sorted(results.items(), key=lambda item: -item[1])
            rates = [(item[0], round(item[1] / count, 2)) for item in items]
            rates_str = ' | '.join([f'{key}: {rate}' for key, rate in rates])

            print(f'RPS: {int(rps)} | {rates_str}'.ljust(60, ' '), end='\r')
            self._counter.clear_period_values()
            self._print_time = current_time
            await asyncio.sleep(self._period)

    def full_stats(self):
        duration = round(self._timer.current_duration, 3)
        count = self._counter.count
        results = self._counter.results

        if not count:
            return 'Total runs: 0'

        items = sorted(results.items(), key=lambda item: -item[1])
        rates = [(item[0], item[1], round(item[1] / count, 2)) for item in items]
        rates_str = '\n'.join([f'{key}: total: {count}, rate: {rate:.2f}' for key, count, rate in rates])

        return f"\nTotal runs: {count}\n" + \
            f"Duration: {duration}\n" + \
            f"RPS: {int(count/duration)}\n" + \
            f"Response rates:\n" + rates_str
