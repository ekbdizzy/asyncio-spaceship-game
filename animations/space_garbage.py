import random
import asyncio
from tools import draw_frame, read_animation_frames

frames = read_animation_frames('graphic/garbage/')


async def fly_garbage(canvas, column, garbage_frame, speed=0.5):
    """Animate garbage, flying from top to bottom. Сolumn position will stay same, as specified on start."""
    rows_number, columns_number = canvas.getmaxyx()

    column = max(column, 0)
    column = min(column, columns_number - 1)

    row = 0

    while row < rows_number:
        draw_frame(canvas, row, column, garbage_frame)
        await asyncio.sleep(0)
        draw_frame(canvas, row, column, garbage_frame, negative=True)
        row += speed


async def fill_orbit_with_garbage(canvas, columns: int):
    while True:
        for i in range(random.randint(1, 50)):
            await asyncio.sleep(0)
        await fly_garbage(canvas, column=random.randint(1, columns - 20), garbage_frame=random.choice(frames))
