from counter import Counter
from timer import Timer
from utils import Cancel
from report import Report


class Manager:
    def __init__(self, duration=None, max_runs=None, max_runs_per_worker=None, until_first_fail=False):
        self._counter = Counter(max_runs=max_runs, max_runs_per_worker=max_runs_per_worker)
        self._until_first_fail = until_first_fail

        self._timer = Timer(duration=duration)
        self._cancel = Cancel()
        self._report = Report(self._timer, self._counter)

    @property
    def report(self):
        return self._report

    def inc(self, wid):
        self._counter.inc(wid)

    def success(self, wid):
        self._counter.success()
        self._report.set(wid)

    def fail(self, wid):
        self._counter.fail()
        self._report.set(wid)
        if self._until_first_fail:
            self._cancel.cancel()

    def cancel(self):
        self._cancel.cancel()

    def finished(self, wid=None):
        return self._counter.reached(wid) or self._timer.finished or self._cancel.cancelled

    async def print_stats(self):
        while not self.finished():
            await self._report.current_stats()
