import random
from typing import Union
from tools import draw_frame, read_animation_frames, get_frame_size, sleep
from settings.game_state import obstacles, obstacles_in_last_collisions, coroutines
from tools.obstacles import Obstacle
from settings import game_state

frames = read_animation_frames('graphic/garbage/')


def get_tics(year: int) -> Union[int, float]:
    if year < 1980:
        return 5
    elif 1980 <= year <= 2000:
        return 4
    elif 2001 <= year <= 2020:
        return 3
    elif 2021 <= year <= 2040:
        return 2
    elif 2040 <= year <= 2060:
        return 1
    else:
        return 0.4


async def fly_garbage(canvas, column: int, garbage_frame: str, tics: Union[int, float], speed: float = 0.5) -> None:
    """Animate garbage, flying from top to bottom. Сolumn position will stay same, as specified on start.
    """
    rows_number, columns_number = canvas.getmaxyx()

    column = max(column, 0)
    column = min(column, columns_number - 1)

    row = 0

    frame_rows, frame_columns = get_frame_size(garbage_frame)

    while row < rows_number:
        draw_frame(canvas, row, column, garbage_frame)
        obstacle = Obstacle(row, column, frame_rows, frame_columns)

        obstacles.append(obstacle)

        await sleep(tics)

        if obstacle in obstacles_in_last_collisions:
            draw_frame(canvas, row, column, garbage_frame, negative=True)
            obstacles_in_last_collisions.remove(obstacle)
            obstacles.remove(obstacle)
            return

        draw_frame(canvas, row, column, garbage_frame, negative=True)
        row += speed

        obstacles.remove(obstacle)


async def fill_orbit_with_garbage(canvas, columns: int) -> None:
    while True:
        tics = get_tics(game_state.year)
        coroutines.append(fly_garbage(
            canvas,
            column=random.randint(1, columns - 20),
            garbage_frame=random.choice(frames),
            tics=int(tics) or 1))
        await sleep(int(tics * 5))
