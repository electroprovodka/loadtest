import aiohttp
import asyncio


class Worker:
    def __init__(self, loop, id, coroutine, manager, session_setup):
        self.id = id
        self.coroutine = coroutine
        self.loop = loop
        self.manager = manager

        if session_setup is not None:
            session_data = session_setup()
            if not isinstance(session_data, dict):
                raise ValueError('Session setup should return dict')
        else:
            session_data = {}

        self.session_data = session_data

    def is_active(self):
        return not self.manager.finished(self.id)

    def get_session_data(self):
        options = self.session_data.copy()
        options.update({
            'loop': self.loop,
            'connector': aiohttp.TCPConnector(limit=0)
        })
        return options

    async def run(self):
        options = self.get_session_data()

        async with aiohttp.ClientSession(**options) as session:
            # We schedule coroutine until any of the exit conditions is reached
            while self.is_active():
                # Increment before scheduling to notify the counter that it should increment immediately
                # done to prevent the case when 999 of 1000 total runs was done, and multiple workers
                # are trying to schedule the next task as 1000th
                self.manager.inc(self.id)
                result = await self.coroutine(session)
                self.manager.store_result(result)
