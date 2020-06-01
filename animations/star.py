import asyncio
import curses
import random


async def blink(canvas, row: int, column: int, symbol='*') -> None:
    """Star animation."""

    while True:

        for frame in range(random.randint(1, 20)):
            canvas.addstr(row, column, symbol, curses.A_DIM)
            await asyncio.sleep(0)

        for frame in range(random.randint(1, 3)):
            canvas.addstr(row, column, symbol)
            await asyncio.sleep(0)

        for frame in range(random.randint(1, 5)):
            canvas.addstr(row, column, symbol, curses.A_BOLD)
            await asyncio.sleep(0)

        for frame in range(random.randint(1, 3)):
            canvas.addstr(row, column, symbol)
            await asyncio.sleep(0)
