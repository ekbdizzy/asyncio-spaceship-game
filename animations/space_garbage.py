import random
from tools import draw_frame, read_animation_frames, get_frame_size, sleep
from tools.game_state import obstacles, obstacles_in_last_collisions, coroutines
from tools.obstacles import Obstacle
from tools import game_state

frames = read_animation_frames('graphic/garbage/')


def get_garbage_quantity():
    return 100 // (game_state.year - 1956) or 1


def get_freq(year):
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


async def fly_garbage(canvas, column, garbage_frame, frequency, speed=0.5):
    """Animate garbage, flying from top to bottom. Сolumn position will stay same, as specified on start."""
    rows_number, columns_number = canvas.getmaxyx()

    column = max(column, 0)
    column = min(column, columns_number - 1)

    row = 0

    frame_rows, frame_columns = get_frame_size(garbage_frame)

    while row < rows_number:
        draw_frame(canvas, row, column, garbage_frame)
        obstacle = Obstacle(row, column, frame_rows, frame_columns)

        obstacles.append(obstacle)

        await sleep(frequency)

        if obstacle in obstacles_in_last_collisions:
            draw_frame(canvas, row, column, garbage_frame, negative=True)
            obstacles_in_last_collisions.remove(obstacle)
            obstacles.remove(obstacle)
            return

        draw_frame(canvas, row, column, garbage_frame, negative=True)
        row += speed

        obstacles.remove(obstacle)


async def fill_orbit_with_garbage(canvas, columns: int):
    while True:
        freq = get_freq(game_state.year)
        coroutines.append(fly_garbage(
            canvas,
            column=random.randint(1, columns - 20),
            garbage_frame=random.choice(frames),
            frequency=int(freq) or 1))
        await sleep(int(freq * 5))
