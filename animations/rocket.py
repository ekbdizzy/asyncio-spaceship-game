import os
import asyncio
import curses
import time

from tools import draw_frame
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


def read_rocket_frames() -> List[str]:
    """ Helper func to get frames for rocket animation """

    frames = []
    frames_directory = os.path.join(os.getcwd(), 'graphic/rocket_frames/')
    for file in os.listdir(frames_directory):
        with open(os.path.join(frames_directory, file)) as frame:
            frames.append(frame.read())
    return frames


async def animate_rocket(canvas, row: int, column: int, frames: List):
    iterator = cycle(frames)
    frame = next(iterator)

    while True:
        draw_frame(canvas, row, column, frame, negative=True)
        frame = next(iterator)
        draw_frame(canvas, row, column, frame)
        canvas.refresh()
        await asyncio.sleep(0)

