import curses
from tools import sleep, get_canvas_size
from settings.game_state import obstacles_in_last_collisions, obstacles, coroutines
from animations.explosion import explode


async def fire(canvas, start_row: int, start_column: int, rows_speed=-0.3, columns_speed=0) -> None:
    """Display animation of gun shot, direction and speed can be specified."""

    row, column = start_row, start_column
    canvas_rows, canvas_columns = get_canvas_size(canvas)
    max_row, max_column = canvas_rows - 1, canvas_columns - 1

    curses.beep()
    canvas.addstr(round(row), round(column), '*')
    await sleep(1)

    canvas.addstr(round(row), round(column), 'O')
    await sleep(1)
    canvas.addstr(round(row), round(column), ' ')

    symbol = '-' if columns_speed else '|'
    row += rows_speed
    column += columns_speed

    while 0 < row < max_row and 0 < column < max_column:

        for obstacle in obstacles:
            if obstacle.has_collision(row, column):
                obstacles_in_last_collisions.append(obstacle)
                coroutines.append(explode(canvas, row, column))
                return

        canvas.addstr(round(row), round(column), symbol)
        await sleep(1)
        canvas.addstr(round(row), round(column), ' ')
        row += rows_speed
        column += columns_speed
