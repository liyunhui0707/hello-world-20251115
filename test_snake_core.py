from snake_core import Direction, Snake, make_body


def test_snake_step_moves_head_and_shifts_body():
    snake = Snake(
        initial_body=make_body((5, 5), (4, 5), (3, 5)),
        initial_direction=Direction.RIGHT,
    )

    snake.step(grid_w=30, grid_h=20)

    assert list(snake.body) == [(6, 5), (5, 5), (4, 5)]


def test_move_snake_can_grow():
    snake = Snake(
        initial_body=make_body((5, 5), (4, 5), (3, 5)),
        initial_direction=Direction.RIGHT,
    )

    snake.move_snake(grid_w=30, grid_h=20, grow=True)

    assert list(snake.body) == [(6, 5), (5, 5), (4, 5), (3, 5)]


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

    changed = snake.set_direction(Direction.LEFT)

    assert changed is False
    assert snake.direction == Direction.RIGHT


def test_set_direction_accepts_non_opposite_change():
    snake = Snake(
        initial_body=make_body((5, 5), (4, 5), (3, 5)),
        initial_direction=Direction.RIGHT,
    )

    changed = snake.set_direction(Direction.UP)

    assert changed is True
    assert snake.direction == Direction.UP


def test_check_collision_reports_head_overlap():
    snake = Snake(
        initial_body=make_body((5, 5), (4, 5), (3, 5)),
        initial_direction=Direction.RIGHT,
    )

    assert snake.check_collision({(1, 1), (5, 5)}) is True
    assert snake.check_collision({(1, 1), (2, 2)}) is False
