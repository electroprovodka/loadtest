import aiohttp


class Worker:
    def __init__(self, loop, id, coroutine, canceler, timer, counter, report):
        self.id = id
        self.coroutine = coroutine
        self.canceler = canceler
        self.report = report
        self.loop = loop
        self.timer = timer
        self.counter = counter

    def is_active(self):
        return not (self.canceler.cancelled or self.timer.finished or self.counter.finished)

    async def run(self):
        async with aiohttp.ClientSession(loop=self.loop) as session:
            while self.is_active():
                result = await self.coroutine(session)
                if result is True:
                    self.counter.success()
                else:
                    self.counter.fail()
                self.report.set(self.id)
