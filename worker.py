import aiohttp


class Worker:
    def __init__(self, loop, id, coroutine, canceler, report, timer):
        self.id = id
        self.coroutine = coroutine
        self.canceler = canceler
        self.report = report
        self.loop = loop
        self.timer = timer

    def is_active(self):
        return not (self.canceler.cancelled or self.timer.finished)

    async def run(self):
        async with aiohttp.ClientSession(loop=self.loop) as session:
            while self.is_active():
                result = await self.coroutine(session)
                if result is True:
                    self.report.success()
                else:
                    self.report.fail()
                self.report.set(self.id, (self.loop.time(), result))
