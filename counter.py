from collections import defaultdict


class Counter:
    def __init__(self, max_runs=None, max_runs_per_worker=False):
        self._max = max_runs
        self._max_runs_per_worker = max_runs_per_worker
        self._workers_count = defaultdict(int)

        self._count = 0
        self._results = defaultdict(int)

        self._period_count = 0
        self._period_results = defaultdict(int)

    @property
    def count(self):
        return self._count

    @property
    def results(self):
        return self._results

    @property
    def period_count(self):
        return self._period_count

    @property
    def period_results(self):
        return self._period_results

    def clear_period_values(self):
        self._period_count = 0
        self._period_results = defaultdict(int)

    def reached(self, wid):
        if self._max is None and self._max_runs_per_worker is None:
            return False
        # Check if has per-worker condition and if this condition is reached for worker
        if self._max_runs_per_worker and wid is not None and self._workers_count[wid] >= self._max_runs_per_worker:
            return True
        return self._count >= self._max

    def inc(self, wid):
        self._count += 1
        self._workers_count[wid] += 1
        self._period_count += 1

    def store_result(self, value):
        self._results[value] += 1
        self._period_results[value] += 1
