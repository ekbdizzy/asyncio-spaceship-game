import time
import curses
import random

from tools import read_animation_frames, get_canvas_size
from settings import game_state
from settings import settings

from animations.star import blink
from animations.rocket import rocket
from animations.space_garbage import fill_orbit_with_garbage
from animations.year import show_year, update_year


def draw(canvas):
    curses.curs_set(0)
    canvas.nodelay(True)
    canvas.border()

    canvas_rows_size, canvas_columns_size = get_canvas_size(canvas)

    # added current year
    game_state.coroutines.append(show_year(canvas.derwin(10, 4)))

    # added stars
    border = settings.BORDER_WIDTH
    for n in range(settings.STARS_QUANTITY):
        game_state.coroutines.append(blink(canvas,
                                           row=random.randint(border, canvas_rows_size - border),
                                           column=random.randint(border, canvas_columns_size - border),
                                           symbol=random.choice(settings.STARS)))

    # added rocket
    game_state.coroutines.append(rocket(canvas,
                                        row=canvas_rows_size // 2, column=canvas_columns_size // 2,
                                        speed_of_rocket=settings.SPEED_OF_ROCKET,
                                        speed_animation_divider=settings.ROCKET_ANIMATION_SPEED_DIVIDER,
                                        frames=read_animation_frames(settings.ROCKET_ANIMATIONS_FRAMES)))

    game_state.coroutines.append(fill_orbit_with_garbage(canvas, canvas_columns_size))
    game_state.coroutines.append(update_year(canvas, settings.UPDATE_YEAR_TICS))

    while True:
        for coroutine in game_state.coroutines.copy():
            try:
                coroutine.send(None)
            except StopIteration:
                game_state.coroutines.remove(coroutine)
        time.sleep(settings.TIC_TIMEOUT)
        canvas.refresh()


if __name__ == '__main__':
    curses.update_lines_cols()
    curses.wrapper(draw)
