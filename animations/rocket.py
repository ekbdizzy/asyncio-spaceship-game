import asyncio
import curses

from tools import draw_frame, change_object_position
from typing import List
from itertools import cycle


async def fire(canvas, start_row: int, start_column: int, rows_speed=-0.3, columns_speed=0) -> None:
    """Display animation of gun shot, direction and speed can be specified."""

    row, column = start_row, start_column

    canvas.addstr(round(row), round(column), '*')
    await asyncio.sleep(0)

    canvas.addstr(round(row), round(column), 'O')
    await asyncio.sleep(0)
    canvas.addstr(round(row), round(column), ' ')

    row += rows_speed
    column += columns_speed

    symbol = '-' if columns_speed else '|'

    rows, columns = canvas.getmaxyx()
    max_row, max_column = rows - 1, columns - 1

    curses.beep()

    while 0 < row < max_row and 0 < column < max_column:
        canvas.addstr(round(row), round(column), symbol)
        await asyncio.sleep(0)
        canvas.addstr(round(row), round(column), ' ')
        row += rows_speed
        column += columns_speed


async def rocket(canvas, row: int, column: int, frames: List):
    iterator = cycle(frames)
    frame = next(iterator)

    while True:
        draw_frame(canvas, row, column, frame, negative=True)
        frame = next(iterator)

        # change position of rocket if arrows pushed
        row, column = change_object_position(canvas, row, column, frames)

        draw_frame(canvas, row, column, frame)
        canvas.refresh()

        await asyncio.sleep(0)
