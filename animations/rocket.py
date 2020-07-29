from itertools import cycle, chain
from typing import List

from tools import draw_frame, sleep, read_controls, get_object_size, read_animation_frames

from animations.fire import fire
from animations.game_over import game_over
from animations.explosion import explode

from tools.game_state import coroutines
from tools.objects_tools import get_axis_position
from tools.physics import update_speed
from tools.game_state import obstacles


async def rocket(canvas, row: int, column: int, frames: List, speed_of_rocket=1, speed_animation_divider=1):
    # Note that canvas.getmaxyx() return a tuple: width and height of the window, not a max y and max x values.
    canvas_rows_size, canvas_columns_size = canvas.getmaxyx()

    animation_groups = [[frame] * speed_animation_divider for frame in frames]
    animation = chain(*animation_groups)
    frames_infinite_cycle = cycle(animation)

    current_frame = ''
    row_speed, column_speed = 0, 0
    for frame in frames_infinite_cycle:

        object_row_size, object_column_size = get_object_size(frames)

        for obstacle in obstacles:
            if obstacle.has_collision(row, column, object_row_size, object_column_size):
                draw_frame(canvas, row, column, current_frame, negative=True)
                coroutines.append(game_over(canvas, read_animation_frames('graphic/game_over/')[0]))
                coroutines.append(explode(canvas, row + 2, column))
                return

        draw_frame(canvas, row, column, current_frame, negative=True)

        rocket_rows_direction, rocket_column_direction, space_pressed = read_controls(canvas)

        row_speed, column_speed = update_speed(row_speed, column_speed, rocket_rows_direction, rocket_column_direction)
        row += row_speed * speed_of_rocket
        column += column_speed * speed_of_rocket

        row = get_axis_position(row, object_row_size, canvas_rows_size)
        column = get_axis_position(column, object_column_size, canvas_columns_size)

        if space_pressed:
            coroutines.append(fire(canvas, row - 1, column + object_column_size // 2))

        draw_frame(canvas, row, column, frame)
        current_frame = frame
        canvas.refresh()
        await sleep(1)
