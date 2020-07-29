import asyncio


async def sleep(tics=10):
    for _ in range(tics):
        await asyncio.sleep(0)
