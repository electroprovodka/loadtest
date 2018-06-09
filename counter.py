class Counter:
    def __init__(self, max_runs=None, until_first_exception=False):
        self._max = max_runs
        self._until_first_exception = until_first_exception
        self._count = 0
        self._success = 0
        self._fail = 0

    @property
    def finished(self):
        if self._max is None:
            return False
        if self._until_first_exception and self._fail:
            return True
        return self._count >= self._max

    def success(self):
        self._success += 1
        self._count += 1

    def fail(self):
        self._fail += 1
        self._count += 1

    @property
    def count(self):
        return self._count

    @property
    def success_count(self):
        return self._success
