import asyncio
from typing import Union


async def sleep(tics=10):
    for _ in range(tics):
        await asyncio.sleep(0)


def get_canvas_size(canvas) -> Union[int, int]:
    # Note that canvas.getmaxyx() return a tuple: width and height of the window, not a max y and max x values.
    return canvas.getmaxyx()
