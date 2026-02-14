"""Two-player Snake scaffold: currently implements Snake A only.

Controls:
- Arrow keys: change Snake A direction
"""

from __future__ import annotations

from dataclasses import dataclass
from collections import deque
from typing import Tuple

import pygame

from snake_core import Direction, Snake


@dataclass(frozen=True)
class GameConfig:
    window_width: int = 960
    window_height: int = 640
    cell_size: int = 32
    logic_hz: int = 10
    background_color: Tuple[int, int, int] = (18, 18, 22)
    snake_a_color: Tuple[int, int, int] = (64, 220, 130)
    grid_line_color: Tuple[int, int, int] = (35, 35, 42)

    @property
    def grid_width(self) -> int:
        return self.window_width // self.cell_size

    @property
    def grid_height(self) -> int:
        return self.window_height // self.cell_size


class SnakeGame:
    def __init__(self, config: GameConfig | None = None) -> None:
        self.cfg = config or GameConfig()
        self.screen: pygame.Surface | None = None
        self.clock: pygame.time.Clock | None = None
        self.running = False

        self.snake_a = self._create_snake_a()

    def _create_snake_a(self) -> Snake:
        cx = self.cfg.grid_width // 2
        cy = self.cfg.grid_height // 2
        body = deque([(cx, cy), (cx - 1, cy), (cx - 2, cy)])
        return Snake(initial_body=body, initial_direction=Direction.RIGHT)

    def initialize(self) -> None:
        pygame.init()
        self.screen = pygame.display.set_mode((self.cfg.window_width, self.cfg.window_height))
        pygame.display.set_caption("Snake (2P scaffold) - Snake A")
        self.clock = pygame.time.Clock()
        self.running = True

    def run(self) -> None:
        self.initialize()

        assert self.clock is not None
        logic_step_ms = 1000.0 / self.cfg.logic_hz
        accumulated_ms = 0.0

        while self.running:
            frame_ms = self.clock.tick(60)
            accumulated_ms += frame_ms

            self._handle_events()

            while accumulated_ms >= logic_step_ms:
                self._update()
                accumulated_ms -= logic_step_ms

            self._render()

        pygame.quit()

    def _handle_events(self) -> None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    self.snake_a.set_direction(Direction.UP)
                elif event.key == pygame.K_DOWN:
                    self.snake_a.set_direction(Direction.DOWN)
                elif event.key == pygame.K_LEFT:
                    self.snake_a.set_direction(Direction.LEFT)
                elif event.key == pygame.K_RIGHT:
                    self.snake_a.set_direction(Direction.RIGHT)

    def _update(self) -> None:
        self.snake_a.step(self.cfg.grid_width, self.cfg.grid_height)

    def _render(self) -> None:
        assert self.screen is not None

        self.screen.fill(self.cfg.background_color)
        self._draw_grid()
        self._draw_snake(self.snake_a, self.cfg.snake_a_color)
        pygame.display.flip()

    def _draw_grid(self) -> None:
        assert self.screen is not None
        c = self.cfg

        for x in range(0, c.window_width, c.cell_size):
            pygame.draw.line(self.screen, c.grid_line_color, (x, 0), (x, c.window_height))
        for y in range(0, c.window_height, c.cell_size):
            pygame.draw.line(self.screen, c.grid_line_color, (0, y), (c.window_width, y))

    def _draw_snake(self, snake: Snake, color: Tuple[int, int, int]) -> None:
        assert self.screen is not None

        for gx, gy in snake.body:
            rect = pygame.Rect(
                gx * self.cfg.cell_size,
                gy * self.cfg.cell_size,
                self.cfg.cell_size,
                self.cfg.cell_size,
            )
            pygame.draw.rect(self.screen, color, rect)


def main() -> None:
    SnakeGame().run()


if __name__ == "__main__":
    main()
