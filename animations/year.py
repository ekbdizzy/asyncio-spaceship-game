from tools import sleep, draw_frame, get_canvas_size
from settings import game_state, settings


async def you_have_a_gun_info(canvas):
    canvas_rows_size, canvas_columns_size = get_canvas_size(canvas)
    draw_frame(canvas, canvas_rows_size - 3, 0, "You have a gun! Press SPACE to fire")
    await sleep(4)

    draw_frame(canvas, canvas_rows_size - 3, 0, "You have a gun! Press SPACE to fire", negative=True)
    await sleep(2)

    draw_frame(canvas, canvas_rows_size - 3, 0, "You have a gun! Press SPACE to fire")
    await sleep(4)

    draw_frame(canvas, canvas_rows_size - 3, 0, "You have a gun! Press SPACE to fire", negative=True)
    await sleep(2)

    draw_frame(canvas, canvas_rows_size - 3, 0, "You have a gun! Press SPACE to fire")
    await sleep(30)

    draw_frame(canvas, canvas_rows_size - 3, 0, "You have a gun! Press SPACE to fire", negative=True)

    while True:
        draw_frame(canvas, canvas_rows_size - 3, 0, "Press SPACE to fire")
        await sleep(2)


async def update_year(canvas, tic):
    """Increase by 1 global settings.YEAR every tic."""
    while True:
        game_state.year += 1
        if game_state.year == settings.CANNON_APPEARS_YEAR:
            game_state.coroutines.append(you_have_a_gun_info(canvas.derwin(10, 4)))
        await sleep(tic)


async def show_year(canvas):
    """Show current year from global game_state.year on left bottom of canvas."""
    canvas_rows_size, canvas_columns_size = get_canvas_size(canvas)

    while True:
        draw_frame(canvas, canvas_rows_size - 2, 0, f"Year: {str(game_state.year)}")
        canvas.syncup()
        await sleep(2)
