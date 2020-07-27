import random
from tools import draw_frame, read_animation_frames, get_frame_size, sleep
from tools.game_state import obstacles, coroutines
from tools.obstacles import Obstacle, show_obstacles

frames = read_animation_frames('graphic/garbage/')


async def fly_garbage(canvas, column, garbage_frame, speed=0.5):
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

        await sleep()

        draw_frame(canvas, row, column, garbage_frame, negative=True)
        row += speed

        obstacles.remove(obstacle)


async def fill_orbit_with_garbage(canvas, columns: int):
    while True:
        await sleep(random.randint(1, 50))
        await fly_garbage(canvas, column=random.randint(1, columns - 20), garbage_frame=random.choice(frames))
