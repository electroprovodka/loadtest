from counter import Counter
from timer import Timer
from utils import Cancel
from report import Report


class Manager:
    def __init__(self, duration=None, max_runs=None, max_runs_per_worker=None, until_first_fail=False):
        self.counter = Counter(max_runs=max_runs, max_runs_per_worker=max_runs_per_worker)
        self.until_first_fail = until_first_fail

        self.timer = Timer(duration=duration)
        self.cancel = Cancel()
        self.report = Report(self.timer, self.counter)

    def inc(self, wid):
        self.counter.inc(wid)

    def success(self, wid):
        self.counter.success()
        self.report.set(wid)

    def fail(self, wid):
        self.counter.fail()
        self.report.set(wid)
        if self.until_first_fail:
            self.cancel.cancel()

    def cancel(self):
        self.cancel.cancel()

    def finished(self, wid=None):
        return self.counter.reached(wid) or self.timer.finished or self.cancel.cancelled

    async def print_stats(self):
        while not self.finished():
            await self.report.current_stats()
