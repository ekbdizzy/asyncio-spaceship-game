import asyncio
import curses

from itertools import cycle, chain
from tools import draw_frame, get_object_position
from typing import List


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
    animation_groups = [[frame] * speed_animation_divider for frame in frames]
    animation = chain(*animation_groups)
    frames_infinite_cycle = cycle(animation)

    current_frame = ''
    for frame in frames_infinite_cycle:
        draw_frame(canvas, row, column, current_frame, negative=True)
        row, column = get_object_position(canvas, row, column, frames, speed=speed_of_rocket)
        draw_frame(canvas, row, column, frame)
        current_frame = frame
        canvas.refresh()
        await asyncio.sleep(0)
