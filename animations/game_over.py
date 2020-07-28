from tools import draw_frame, sleep, get_frame_size


async def game_over(canvas, frame: str):
    row_size, column_size = get_frame_size(frame)

    # Note that canvas.getmaxyx() return a tuple: width and height of the window, not a max y and max x values.
    canvas_rows_size, canvas_columns_size = canvas.getmaxyx()

    row = (canvas_rows_size - row_size) // 2
    column = (canvas_columns_size - column_size) // 2

    while True:
        draw_frame(canvas, row, column, frame)
        await sleep()
