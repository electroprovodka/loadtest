import asyncio
import aiohttp


from runner import Runner


async def coroutine(session):
    async with session.get('http://example.com') as response:
        data = await response.content.read(1024)
        return response.status == 200


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    runner = Runner(1600, coroutine, duration=120, max_runs=150000, loop=loop)
    result = runner.run()
    print(result.full_stats())
