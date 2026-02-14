from __future__ import annotations

from collections import deque
from enum import Enum
from typing import Deque, Tuple

from grid_utils import wrap_position

Vec2 = Tuple[int, int]


class Direction(Enum):
    UP = (0, -1)
    DOWN = (0, 1)
    LEFT = (-1, 0)
    RIGHT = (1, 0)

    @property
    def vec(self) -> Vec2:
        return self.value


def opposite_of(direction: Direction) -> Direction:
    """Return the opposite cardinal direction."""
    opposites = {
        Direction.UP: Direction.DOWN,
        Direction.DOWN: Direction.UP,
        Direction.LEFT: Direction.RIGHT,
        Direction.RIGHT: Direction.LEFT,
    }
    return opposites[direction]


class Snake:
    """Represents a snake body and movement rules on a wrapping grid."""

    def __init__(self, initial_body: Deque[Vec2], initial_direction: Direction) -> None:
        if not initial_body:
            raise ValueError("Snake body cannot be empty")
        self.body: Deque[Vec2] = initial_body
        self.direction: Direction = initial_direction

    @property
    def head(self) -> Vec2:
        return self.body[0]

    def set_direction(self, new_direction: Direction) -> None:
        """Prevent instant 180-degree reversals to avoid self-collisions."""
        if new_direction != opposite_of(self.direction):
            self.direction = new_direction

    def step(self, grid_w: int, grid_h: int) -> None:
        if grid_w <= 0 or grid_h <= 0:
            raise ValueError("Grid dimensions must be positive")

        hx, hy = self.head
        dx, dy = self.direction.vec
        nx, ny = wrap_position(hx + dx, hy + dy, grid_w, grid_h)

        self.body.appendleft((nx, ny))
        self.body.pop()


def make_body(*coords: Vec2) -> Deque[Vec2]:
    return deque(coords)
