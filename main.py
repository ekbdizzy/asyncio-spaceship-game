import asyncio
import time
import curses
import random
from typing import Callable, List

TIC_TIMEOUT: float = 0.1
SYMBOLS: str = '+*.:'
STARS: List[str] = [symbol for symbol in SYMBOLS]
STARS_QUANTITY: int = 50


async def blink(canvas, row: int, column: int, symbol='*') -> None:
    """ Star animation """

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


def draw(canvas):
    curses.curs_set(0)
    canvas.border()
    canvas.refresh()

    canvas_x_size, canvas_y_size = canvas.getmaxyx()
    canvas_center = (canvas_x_size // 2, canvas_y_size // 2)

    coroutines: List[Callable[...]] = [
        blink(canvas,
              random.randint(2, canvas_x_size - 2),
              random.randint(2, canvas_y_size - 2),
              symbol=random.choice(STARS)) for _ in range(STARS_QUANTITY)
    ]

    coroutines.append(fire(canvas, start_row=canvas_center[0], start_column=canvas_center[1]))

    while True:
        for coroutine in coroutines.copy():
            try:
                coroutine.send(None)
                canvas.refresh()
            except StopIteration:
                coroutines.remove(coroutine)
        time.sleep(TIC_TIMEOUT)


if __name__ == '__main__':
    curses.update_lines_cols()
    curses.wrapper(draw)
