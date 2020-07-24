import asyncio
import curses
import random
from animations import blink, fire, rocket, fill_orbit_with_garbage
from tools import read_animation_frames
from typing import List

TIC_TIMEOUT: float = 0.1

# stars
SYMBOLS: str = '+*.:'
STARS: List[str] = [symbol for symbol in SYMBOLS]
STARS_QUANTITY: int = 50

# rocket
ROCKET_ANIMATIONS_FRAMES = 'graphic/rocket_frames/'
SPEED_OF_ROCKET = 3
ROCKET_ANIMATION_SPEED_DIVIDER = 2


def draw(canvas):
    loop = asyncio.get_event_loop()

    curses.curs_set(0)
    canvas.nodelay(True)
    canvas.border()

    # Note that canvas.getmaxyx() return a tuple: width and height of the window, not a max y and max x values.
    canvas_rows_size, canvas_columns_size = canvas.getmaxyx()
    canvas_x_center = canvas_rows_size // 2
    canvas_y_center = canvas_columns_size // 2

    # added stars
    for n in range(STARS_QUANTITY):
        loop.create_task(blink(canvas,
                               row=random.randint(2, canvas_rows_size - 2),
                               column=random.randint(2, canvas_columns_size - 2),
                               symbol=random.choice(STARS)))

    # added fire
    loop.create_task(fire(canvas, start_row=canvas_x_center, start_column=canvas_y_center))

    # added rocket
    loop.create_task(rocket(canvas,
                            row=2, column=2,
                            speed_of_rocket=SPEED_OF_ROCKET,
                            speed_animation_divider=ROCKET_ANIMATION_SPEED_DIVIDER,
                            frames=read_animation_frames(ROCKET_ANIMATIONS_FRAMES)))

    # added garbage
    for i in range(5):
        loop.create_task(fill_orbit_with_garbage(canvas, canvas_columns_size))

    loop.run_forever()


if __name__ == '__main__':
    curses.update_lines_cols()
    curses.wrapper(draw)
