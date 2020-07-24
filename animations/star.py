import asyncio
import curses
import random
from tools import sleep


async def blink(canvas, row: int, column: int, symbol='*') -> None:
    """Star animation."""

    while True:
        canvas.addstr(row, column, symbol, curses.A_DIM)
        await sleep(random.randint(1, 20))
        canvas.refresh()

        canvas.addstr(row, column, symbol)
        await sleep(random.randint(1, 3))
        canvas.refresh()

        canvas.addstr(row, column, symbol, curses.A_BOLD)
        await sleep(random.randint(1, 5))
        canvas.refresh()

        canvas.addstr(row, column, symbol)
        await sleep(random.randint(1, 3))
        canvas.refresh()
