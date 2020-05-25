import os
from tools import read_controls, get_frame_size
from typing import List, Tuple


def get_object_size(frames: List) -> Tuple[int, int]:
    """ Return max size of object """

    if not frames:
        return 0, 0
    object_row_size = max([get_frame_size(frame)[0] for frame in frames])
    object_column_size = max([get_frame_size(frame)[1] for frame in frames])
    return object_row_size, object_column_size


def read_animation_frames(path_to_frames: str) -> List[str]:
    """ Get all frames for animation from folder 'path_to_frames' """

    frames = []
    frames_directory = os.path.join(os.getcwd(), path_to_frames)
    for file in os.listdir(frames_directory):
        with open(os.path.join(frames_directory, file)) as frame:
            frames.append(frame.read())
    return frames


def change_object_position(canvas,
                           current_row: int, current_column: int,
                           frames: List[str]) -> Tuple[int, int]:

    """ Moves object according 'read_controls' actions if object inside canvas """

    rocket_controls = read_controls(canvas)
    next_row_position = current_row + rocket_controls[0]
    next_column_position = current_column + rocket_controls[1]

    object_row_size, object_column_size = get_object_size(frames)

    if 0 < next_row_position < canvas.getmaxyx()[0] - object_row_size:
        current_row = next_row_position

    if 0 < next_column_position < canvas.getmaxyx()[1] - object_column_size:
        current_column = next_column_position

    return current_row, current_column
