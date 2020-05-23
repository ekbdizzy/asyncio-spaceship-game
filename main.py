import time
import curses
import random
from animations import blink, fire, animate_rocket, read_rocket_frames
from typing import Callable, List

TIC_TIMEOUT: float = 0.1
SYMBOLS: str = '+*.:'
STARS: List[str] = [symbol for symbol in SYMBOLS]
STARS_QUANTITY: int = 50


def draw(canvas):
    curses.curs_set(0)
    canvas.nodelay(True)
    canvas.refresh()
    canvas.border()
    canvas_x_size, canvas_y_size = canvas.getmaxyx()
    canvas_center = (canvas_x_size // 2, canvas_y_size // 2)

    coroutines: List[Callable[...]] = []

    # added stars
    for n in range(STARS_QUANTITY):
        coroutines.append(blink(canvas,
                                random.randint(2, canvas_x_size - 2),
                                random.randint(2, canvas_y_size - 2),
                                symbol=random.choice(STARS)))

    # added fire
    coroutines.append(fire(canvas, start_row=canvas_center[0], start_column=canvas_center[1]))

    # added rocket
    coroutines.append(animate_rocket(canvas, canvas_center[0], canvas_center[1], read_rocket_frames()))

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
