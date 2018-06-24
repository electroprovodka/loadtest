async def coroutine(session):
    async with session.get('http://example.com') as response:
        data = await response.content.read(1024)
        return response.status == 200


def session_setup():
    return {}
