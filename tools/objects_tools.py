import os
from tools import read_controls, get_frame_size
from typing import List, Tuple


def get_object_size(frames: List[str]) -> Tuple[int, int]:
    """Return max size of object."""

    if not frames:
        return 0, 0
    object_row_size = max([get_frame_size(frame, rows_only=True) for frame in frames])
    object_column_size = max([get_frame_size(frame, columns_only=True) for frame in frames])
    return object_row_size, object_column_size


def read_animation_frames(path_to_frames: str) -> List[str]:
    """Get all frames for animation from folder 'path_to_frames'."""

    frames = []
    for file_name in os.listdir(path_to_frames):
        with open(os.path.join(path_to_frames, file_name)) as file_data:
            frames.append(file_data.read())
    return frames


def set_axis_position(next_axis_position: int, object_axis_size: int, canvas_axis_size: int) -> int:
    """Return value of axis_position between 1 and canvas_axis_size."""

    if next_axis_position < 0:
        return max(1, next_axis_position)
    return min(next_axis_position, canvas_axis_size - object_axis_size - 1)


def change_object_position(canvas,
                           current_row: int, current_column: int,
                           frames: List[str],
                           speed=1) -> Tuple[int, int]:
    """Moves object according 'read_controls' actions if object inside canvas."""

    rocket_rows_controls, rocket_column_controls, fire_control = read_controls(canvas)

    next_row_position = current_row + rocket_rows_controls * speed
    next_column_position = current_column + rocket_column_controls * speed

    object_row_size, object_column_size = get_object_size(frames)
    canvas_max_x, canvas_max_y = canvas.getmaxyx()

    current_row = set_axis_position(next_row_position, object_row_size, canvas_max_x)
    current_column = set_axis_position(next_column_position, object_column_size, canvas_max_y)

    return current_row, current_column


def set_animation_speed_divider(speed_divider: int) -> List[bool]:
    """
    Using:
    for i in set_animation_speed_divider(speed_divider):
        if i:
           do something

    :param: speed_divider (int): value, in how much times animation will be slowly. Max speed = 1.
    :return list of False with the last element=True
    """
    list_with_bool = [False for _ in range(speed_divider)]
    list_with_bool[-1] = True
    return list_with_bool
