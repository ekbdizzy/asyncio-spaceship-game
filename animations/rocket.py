import asyncio
import curses

from tools import draw_frame, change_object_position, set_animation_speed_divider
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


async def rocket(canvas, row: int, column: int, frames: List, speed_of_rocket=1, speed_animation_divider=1):
    frames_infinite_cycle = cycle(frames)

    current_frame = ''
    for frame in frames_infinite_cycle:
        for i in set_animation_speed_divider(speed_animation_divider):
            if i:
                draw_frame(canvas, row, column, current_frame, negative=True)
                row, column = change_object_position(canvas, row, column, frames, speed=speed_of_rocket)
                draw_frame(canvas, row, column, frame)
                current_frame = frame
                canvas.refresh()
            await asyncio.sleep(0)
