from collections import defaultdict


class Counter:
    def __init__(self, max_runs=None, max_runs_per_worker=False):
        self._max = max_runs
        self._max_runs_per_worker = max_runs_per_worker
        self._count = 0
        self._success = 0
        self._fail = 0
        self._workers_count = defaultdict(int)
        self._period_count = 0
        self._period_success = 0

    @property
    def count(self):
        return self._count

    @property
    def success_count(self):
        return self._success

    @property
    def period_count(self):
        return self._period_count

    @property
    def period_success(self):
        return self._period_success

    def clear_period_values(self):
        self._period_count = 0
        self._period_success = 0

    def reached(self, wid):
        if self._max is None and self._max_runs_per_worker is None:
            return False
        if self._max_runs_per_worker and \
                wid is not None and \
                self._workers_count[wid] >= self._max_runs_per_worker:
            return True
        return self._count >= self._max

    def inc(self, wid):
        self._count += 1
        self._workers_count[wid] += 1
        self._period_count += 1

    def success(self):
        self._success += 1
        self._period_success += 1

    def fail(self):
        self._fail += 1
