from grid_utils import wrap_position


def test_wrap_position_inside_bounds():
    assert wrap_position(5, 7, 30, 20) == (5, 7)


def test_wrap_position_positive_overflow():
    assert wrap_position(30, 20, 30, 20) == (0, 0)
    assert wrap_position(31, 21, 30, 20) == (1, 1)


def test_wrap_position_negative_values():
    assert wrap_position(-1, -1, 30, 20) == (29, 19)
    assert wrap_position(-31, -21, 30, 20) == (29, 19)
