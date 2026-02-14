from snake_core import Direction, Snake, make_body


def test_snake_step_moves_head_and_shifts_body():
    snake = Snake(
        initial_body=make_body((5, 5), (4, 5), (3, 5)),
        initial_direction=Direction.RIGHT,
    )

    snake.step(grid_w=30, grid_h=20)

    assert list(snake.body) == [(6, 5), (5, 5), (4, 5)]


def test_snake_step_wraps_around_edges():
    snake = Snake(
        initial_body=make_body((29, 19), (28, 19), (27, 19)),
        initial_direction=Direction.RIGHT,
    )

    snake.step(grid_w=30, grid_h=20)

    assert snake.head == (0, 19)


def test_set_direction_prevents_instant_reversal():
    snake = Snake(
        initial_body=make_body((5, 5), (4, 5), (3, 5)),
        initial_direction=Direction.RIGHT,
    )

    snake.set_direction(Direction.LEFT)

    assert snake.direction == Direction.RIGHT


def test_set_direction_accepts_non_opposite_change():
    snake = Snake(
        initial_body=make_body((5, 5), (4, 5), (3, 5)),
        initial_direction=Direction.RIGHT,
    )

    snake.set_direction(Direction.UP)

    assert snake.direction == Direction.UP
