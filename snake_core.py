from __future__ import annotations

from collections import deque
from enum import Enum
from typing import Deque, Iterable, Set, Tuple

from grid_utils import wrap_position

Vec2 = Tuple[int, int]


class Direction(Enum):
    """Cardinal movement directions represented as `(dx, dy)` deltas."""

    UP = (0, -1)
    DOWN = (0, 1)
    LEFT = (-1, 0)
    RIGHT = (1, 0)

    @property
    def vec(self) -> Vec2:
        """Return `(dx, dy)` vector for this direction."""
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
    """Snake movement model independent from rendering/input frameworks."""

    def __init__(self, initial_body: Deque[Vec2], initial_direction: Direction) -> None:
        if not initial_body:
            raise ValueError("Snake body cannot be empty")

        # Body order is head -> tail.
        self.body: Deque[Vec2] = initial_body
        self.direction: Direction = initial_direction

    @property
    def head(self) -> Vec2:
        """Current head coordinate."""
        return self.body[0]

    @property
    def body_positions(self) -> Set[Vec2]:
        """Fast lookup set of all occupied cells."""
        return set(self.body)

    def set_direction(self, new_direction: Direction) -> bool:
        """Change direction unless it is an immediate reversal.

        Returns:
            True when direction changed, otherwise False.
        """
        if new_direction == opposite_of(self.direction):
            return False

        self.direction = new_direction
        return True

    def next_head_position(self, grid_w: int, grid_h: int) -> Vec2:
        """Compute wrapped next head coordinate for current direction."""
        self._validate_grid_size(grid_w, grid_h)
        head_x, head_y = self.head
        delta_x, delta_y = self.direction.vec
        return wrap_position(head_x + delta_x, head_y + delta_y, grid_w, grid_h)

    def move_snake(self, grid_w: int, grid_h: int, grow: bool = False) -> Vec2:
        """Move snake by one step.

        Args:
            grid_w: Grid width in cells.
            grid_h: Grid height in cells.
            grow: If True, keep tail (snake length +1).

        Returns:
            New head position.
        """
        new_head = self.next_head_position(grid_w, grid_h)

        # Insert new head at the front of the deque.
        self.body.appendleft(new_head)

        # If not growing this tick, remove tail to keep length constant.
        if not grow:
            self.body.pop()

        return new_head

    def step(self, grid_w: int, grid_h: int) -> None:
        """Backward-compatible alias for a normal non-growth movement tick."""
        self.move_snake(grid_w, grid_h, grow=False)

    def check_collision(self, occupied: Iterable[Vec2]) -> bool:
        """Return True if head overlaps any given occupied position."""
        return self.head in set(occupied)

    def check_self_collision(self) -> bool:
        """Return True if head collides with any non-head segment."""
        return self.head in list(self.body)[1:]

    @staticmethod
    def _validate_grid_size(grid_w: int, grid_h: int) -> None:
        """Validate grid dimensions before modulo-wrapping math is used."""
        if grid_w <= 0 or grid_h <= 0:
            raise ValueError("Grid dimensions must be positive")


def make_body(*coords: Vec2) -> Deque[Vec2]:
    """Helper to build a deque body from inline coordinate tuples."""
    return deque(coords)
