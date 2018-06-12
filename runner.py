import asyncio
from collections import defaultdict
import signal
from contextlib import suppress

from counter import Counter
from report import Report
from utils import Cancel
from worker import Worker
from timer import Timer
from manager import Manager


class Runner:
    def __init__(self, workers_count, coroutine, duration=None, max_runs=None, max_runs_per_worker=None,
                 until_first_fail = False, loop=None):
        self.workers_count = workers_count
        self.coroutine = coroutine
        self.workers = []
        self.tasks = []
        self.manager = Manager(duration, max_runs, max_runs_per_worker, until_first_fail)
        self.loop = loop or asyncio.get_event_loop()

    def shutdown(self, signal, frame):
        self.manager.cancel()
        for task in self.tasks:
            with suppress(asyncio.CancelledError):
                task.cancel()
        self.tasks = []

    def ensure_future(self, coro):
        return asyncio.ensure_future(coro, loop=self.loop)

    def gather(self, *tasks):
        return asyncio.gather(*tasks, loop=self.loop, return_exceptions=True)

    def create_worker(self, wid):
        return Worker(self.loop, wid, self.coroutine, self.manager)

    def run(self):
        signal.signal(signal.SIGINT, self.shutdown)
        signal.signal(signal.SIGTERM, self.shutdown)
        self.workers = [self.create_worker(i) for i in range(self.workers_count)]
        tasks = [self.ensure_future(w.run()) for w in self.workers]
        tasks.append(self.ensure_future(self.manager.print_stats()))
        self.tasks = tasks
        try:
            self.loop.run_until_complete(self.gather(*tasks))
        finally:
            self.loop.run_until_complete(self.ensure_future(asyncio.sleep(0, loop=self.loop)))
            self.loop.close()
        return self.manager.report
