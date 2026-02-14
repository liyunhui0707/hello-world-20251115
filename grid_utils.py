from typing import Tuple

Vec2 = Tuple[int, int]


def wrap_position(x: int, y: int, width: int, height: int) -> Vec2:
    """Wrap a grid position at rectangular boundaries."""
    return (x % width, y % height)
