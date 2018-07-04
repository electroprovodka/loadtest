async def coroutine(session):
    async with session.get('http://127.0.0.1:8001/') as response:
        return response.status


def session_setup():
    return {}
