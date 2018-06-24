import aiohttp
import asyncio


class Worker:
    def __init__(self, loop, id, coroutine, manager, timeout, session_setup):
        self.id = id
        self.coroutine = coroutine
        self.loop = loop
        self.manager = manager
        self.timeout = timeout or 0
        if session_setup is not None:
            session_data = session_setup()
            if not isinstance(session_data, dict):
                raise ValueError('Session setup should return dict')
        else:
            session_data = {}
        self.session_data = session_data

    def is_active(self):
        return not self.manager.finished(self.id)

    async def run(self):
        options = self.session_data.copy()
        options.update({
            'loop': self.loop,
            'connector': aiohttp.TCPConnector(limit=0)
        })
        # if self.timeout:
        #     options['timeout'] = aiohttp.ClientTimeout(total=self.timeout)
        async with aiohttp.ClientSession(**options) as session:
            while self.is_active():
                self.manager.inc(self.id)
                result = await self.coroutine(session)
                if result is True:
                    self.manager.success(self.id)
                else:
                    self.manager.fail(self.id)
                await asyncio.sleep(0, loop=self.loop)
