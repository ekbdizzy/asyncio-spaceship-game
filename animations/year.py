from tools import sleep, draw_frame, game_state


async def update_year():
    while True:
        game_state.year += 1
        await sleep(10)


async def show_year(canvas, year):
    # Note that canvas.getmaxyx() return a tuple: width and height of the window, not a max y and max x values.
    canvas_rows_size, canvas_columns_size = canvas.getmaxyx()

    while True:
        draw_frame(canvas, canvas_rows_size - 2, 0, f"Year: {str(game_state.year)}")
        canvas.syncup()
        await sleep(5)
