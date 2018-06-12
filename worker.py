import aiohttp
import asyncio


class Worker:
    def __init__(self, loop, id, coroutine, manager):
        self.id = id
        self.coroutine = coroutine
        self.loop = loop
        self.manager = manager

    def is_active(self):
        return not self.manager.finished(self.id)

    async def run(self):
        async with aiohttp.ClientSession(loop=self.loop) as session:
            while self.is_active():
                self.manager.inc(self.id)
                result = await self.coroutine(session)
                if result is True:
                    self.manager.success(self.id)
                else:
                    self.manager.fail(self.id)
                await asyncio.sleep(0, loop=self.loop)
