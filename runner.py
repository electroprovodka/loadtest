import asyncio
from collections import defaultdict
import signal
from contextlib import suppress

from counter import Counter
from report import Report
from utils import Cancel
from worker import Worker
from timer import Timer


class Runner:
    def __init__(self, workers_count, coroutine, duration=None, max_runs=None, loop=None):
        self.workers_count = workers_count
        self.coroutine = coroutine
        self.workers = []
        self.tasks = []
        self.canceler = Cancel()
        self.timer = Timer(duration=duration)
        self.counter = Counter(max_runs=max_runs)
        self.report = Report(self.timer, self.counter)
        self.loop = loop or asyncio.get_event_loop()

    def shutdown(self, signal, frame):
        self.canceler.cancel()
        for task in self.tasks:
            with suppress(asyncio.CancelledError):
                task.cancel()
        self.tasks = []

    def ensure_future(self, coro):
        return asyncio.ensure_future(coro, loop=self.loop)

    def gather(self, *tasks):
        return asyncio.gather(*tasks, loop=self.loop, return_exceptions=True)

    def create_worker(self, wid):
        return Worker(self.loop, wid, self.coroutine, self.canceler, self.timer, self.counter, self.report)

    def run(self):
        signal.signal(signal.SIGINT, self.shutdown)
        self.workers = [self.create_worker(i) for i in range(self.workers_count)]
        self.tasks = [self.ensure_future(w.run()) for w in self.workers]
        try:
            self.loop.run_until_complete(self.gather(*self.tasks))
        finally:
            self.loop.run_until_complete(self.ensure_future(asyncio.sleep(0, loop=self.loop)))
            self.loop.close()
        return self.report
