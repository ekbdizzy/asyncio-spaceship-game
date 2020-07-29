from tools import sleep, draw_frame, get_canvas_size
from settings import game_state


async def update_year(tic):
    """Increase by 1 global settings.YEAR every tic."""
    while True:
        game_state.year += 1
        await sleep(tic)


async def show_year(canvas):
    """Show current year from global game_state.year on left bottom of canvas."""
    canvas_rows_size, canvas_columns_size = get_canvas_size(canvas)

    while True:
        draw_frame(canvas, canvas_rows_size - 2, 0, f"Year: {str(game_state.year)}")
        canvas.syncup()
        await sleep(1)
