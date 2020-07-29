from tools import draw_frame, sleep, get_frame_size, get_canvas_size


async def game_over(canvas, frame: str) -> None:
    canvas_rows_size, canvas_columns_size = get_canvas_size(canvas)
    row_size, column_size = get_frame_size(frame)

    row = (canvas_rows_size - row_size) // 2
    column = (canvas_columns_size - column_size) // 2

    while True:
        draw_frame(canvas, row, column, frame)
        await sleep()
