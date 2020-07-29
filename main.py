import time
import curses
import random
from animations import blink, rocket, fill_orbit_with_garbage
from tools import read_animation_frames
from tools.game_state import coroutines, year
from typing import List

from animations.year import show_year, update_year

TIC_TIMEOUT: float = 0.05




# stars
SYMBOLS: str = '+*.:'
STARS: List[str] = [symbol for symbol in SYMBOLS]
STARS_QUANTITY: int = 50

# rocket
ROCKET_ANIMATIONS_FRAMES = 'graphic/rocket_frames/'
SPEED_OF_ROCKET = 3
ROCKET_ANIMATION_SPEED_DIVIDER = 2


def draw(canvas):
    curses.curs_set(0)
    canvas.nodelay(True)
    canvas.border()

    # Note that canvas.getmaxyx() return a tuple: width and height of the window, not a max y and max x values.
    canvas_rows_size, canvas_columns_size = canvas.getmaxyx()

    # added stars
    coroutines.append(show_year(canvas.derwin(10, 4), year))

    for n in range(STARS_QUANTITY):
        coroutines.append(blink(canvas,
                                row=random.randint(2, canvas_rows_size - 2),
                                column=random.randint(2, canvas_columns_size - 2),
                                symbol=random.choice(STARS)))

    # added rocket
    coroutines.append(rocket(canvas,
                             row=canvas_rows_size // 2, column=canvas_columns_size // 2,
                             speed_of_rocket=SPEED_OF_ROCKET,
                             speed_animation_divider=ROCKET_ANIMATION_SPEED_DIVIDER,
                             frames=read_animation_frames(ROCKET_ANIMATIONS_FRAMES)))

    coroutines.append(fill_orbit_with_garbage(canvas, canvas_columns_size))
    coroutines.append(update_year())

    while True:
        for coroutine in coroutines.copy():
            try:
                coroutine.send(None)
            except StopIteration:
                coroutines.remove(coroutine)
        time.sleep(TIC_TIMEOUT)
        canvas.refresh()


if __name__ == '__main__':
    curses.update_lines_cols()
    curses.wrapper(draw)
