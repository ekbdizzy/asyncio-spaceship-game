from itertools import cycle, chain
from typing import List

from animations.fire import fire
from animations.game_over import game_over
from animations.explosion import explode

from tools import limit_axis_coord
from tools.physics import update_speed
from settings import game_state
from settings import settings

from tools import (
    draw_frame,
    sleep,
    read_controls,
    get_canvas_size,
    get_object_size,
    read_animation_frames
)


async def rocket(canvas, row: int, column: int, frames: List, speed_of_rocket=1, speed_animation_divider=1):
    canvas_rows_size, canvas_columns_size = get_canvas_size(canvas)

    animation_groups = [[frame] * speed_animation_divider for frame in frames]
    animation = chain(*animation_groups)
    frames_infinite_cycle = cycle(animation)

    current_frame = ''
    row_speed, column_speed = 0, 0
    for frame in frames_infinite_cycle:

        object_row_size, object_column_size = get_object_size(frames)

        for obstacle in game_state.obstacles:
            if obstacle.has_collision(row, column, object_row_size, object_column_size):
                draw_frame(canvas, row, column, current_frame, negative=True)
                game_state.coroutines.append(game_over(canvas, read_animation_frames(settings.GAME_OVER_FRAME)[0]))
                game_state.coroutines.append(explode(canvas, row + 2, column))
                return

        draw_frame(canvas, row, column, current_frame, negative=True)

        rocket_rows_direction, rocket_column_direction, space_pressed = read_controls(canvas)

        row_speed, column_speed = update_speed(
            row_speed,
            column_speed,
            rocket_rows_direction,
            rocket_column_direction
        )
        row += row_speed * speed_of_rocket
        column += column_speed * speed_of_rocket

        row = limit_axis_coord(row, object_row_size, canvas_rows_size)
        column = limit_axis_coord(column, object_column_size, canvas_columns_size)

        if space_pressed and game_state.year > settings.CANNON_APPEARS_YEAR:
            game_state.coroutines.append(fire(canvas, row - 1, column + object_column_size // 2))

        draw_frame(canvas, row, column, frame)
        current_frame = frame
        canvas.refresh()
        await sleep(1)
