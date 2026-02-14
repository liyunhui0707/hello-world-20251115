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

    def set_direction(self, new_direction: Direction) -> bool:
        """Update direction unless it would cause an immediate 180° reversal.

        Returns True if direction changed, False if ignored.
        """
        if new_direction == opposite_of(self.direction):
            return False

        self.direction = new_direction
        return True

    def step(self, grid_w: int, grid_h: int) -> None:
        """Advance one logic tick by moving head forward and dropping tail."""
        self._validate_grid_size(grid_w, grid_h)

        next_head = self.next_head_position(grid_w, grid_h)

        # Insert new head and remove last tail segment to keep length constant.
        self.body.appendleft(next_head)
        self.body.pop()

    def next_head_position(self, grid_w: int, grid_h: int) -> Vec2:
        """Compute the wrapped head position for the next movement tick."""
        self._validate_grid_size(grid_w, grid_h)

        head_x, head_y = self.head
        delta_x, delta_y = self.direction.vec
        return wrap_position(head_x + delta_x, head_y + delta_y, grid_w, grid_h)

    @staticmethod
    def _validate_grid_size(grid_w: int, grid_h: int) -> None:
        if grid_w <= 0 or grid_h <= 0:
            raise ValueError("Grid dimensions must be positive")


def make_body(*coords: Vec2) -> Deque[Vec2]:
    """Convenience helper for tests and setup code."""
    return deque(coords)
