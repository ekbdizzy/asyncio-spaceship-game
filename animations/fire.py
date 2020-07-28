from tools import sleep
from tools.game_state import obstacles_in_last_collisions, obstacles, coroutines
from animations.explosion import explode


async def fire(canvas, start_row: int, start_column: int, rows_speed=-0.3, columns_speed=0) -> None:
    """Display animation of gun shot, direction and speed can be specified."""

    row, column = start_row, start_column

    canvas.addstr(round(row), round(column), '*')
    await sleep()

    canvas.addstr(round(row), round(column), 'O')
    await sleep()
    canvas.addstr(round(row), round(column), ' ')

    row += rows_speed
    column += columns_speed

    symbol = '-' if columns_speed else '|'

    rows, columns = canvas.getmaxyx()
    max_row, max_column = rows - 1, columns - 1

    # curses.beep()

    while 0 < row < max_row and 0 < column < max_column:

        for obstacle in obstacles:
            if obstacle.has_collision(row, column):
                obstacles_in_last_collisions.append(obstacle)
                coroutines.append(explode(canvas, row, column))
                return

        canvas.addstr(round(row), round(column), symbol)
        await sleep()
        canvas.addstr(round(row), round(column), ' ')
        row += rows_speed
        column += columns_speed