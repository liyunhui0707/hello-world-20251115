"""Two-player Snake scaffold with multiplayer-ready structure.

Current controls:
- Snake A: Arrow keys

Notes:
- Architecture supports multiple snakes with independent controls/colors/spawn.
- Only Snake A is enabled by default.
"""

from __future__ import annotations

from collections import deque
from dataclasses import dataclass
from typing import Dict, Mapping, Tuple

import pygame

from snake_core import Direction, Snake


@dataclass(frozen=True)
class PlayerConfig:
    """Per-player controls, visuals, and spawn metadata."""

    name: str
    color: Tuple[int, int, int]
    controls: Mapping[int, Direction]
    spawn_head: Tuple[int, int]
    initial_direction: Direction


@dataclass(frozen=True)
class GameConfig:
    """Global game options and player profile factory."""

    window_width: int = 960
    window_height: int = 640
    cell_size: int = 32
    logic_hz: int = 10
    background_color: Tuple[int, int, int] = (18, 18, 22)
    grid_line_color: Tuple[int, int, int] = (35, 35, 42)
    snake_a_color: Tuple[int, int, int] = (64, 220, 130)
    snake_b_color: Tuple[int, int, int] = (255, 165, 64)
    enable_snake_b: bool = False

    @property
    def grid_width(self) -> int:
        return self.window_width // self.cell_size

    @property
    def grid_height(self) -> int:
        return self.window_height // self.cell_size

    def validate(self) -> None:
        """Fail fast for invalid dimensions or tick-rate settings."""
        if self.window_width % self.cell_size != 0 or self.window_height % self.cell_size != 0:
            raise ValueError("Window size must be divisible by cell_size")
        if self.logic_hz <= 0:
            raise ValueError("logic_hz must be positive")

    def build_player_profiles(self) -> Dict[str, PlayerConfig]:
        """Create default player profiles for the current config."""
        mid_y = self.grid_height // 2
        profiles: Dict[str, PlayerConfig] = {
            "snake_a": PlayerConfig(
                name="Snake A",
                color=self.snake_a_color,
                controls={
                    pygame.K_UP: Direction.UP,
                    pygame.K_DOWN: Direction.DOWN,
                    pygame.K_LEFT: Direction.LEFT,
                    pygame.K_RIGHT: Direction.RIGHT,
                },
                spawn_head=(self.grid_width // 3, mid_y),
                initial_direction=Direction.RIGHT,
            )
        }

        if self.enable_snake_b:
            profiles["snake_b"] = PlayerConfig(
                name="Snake B",
                color=self.snake_b_color,
                controls={
                    pygame.K_w: Direction.UP,
                    pygame.K_s: Direction.DOWN,
                    pygame.K_a: Direction.LEFT,
                    pygame.K_d: Direction.RIGHT,
                },
                spawn_head=((self.grid_width * 2) // 3, mid_y),
                initial_direction=Direction.LEFT,
            )

        return profiles


class SnakeGame:
    """Pygame orchestration layer for input, ticks, and rendering."""

    def __init__(self, config: GameConfig | None = None) -> None:
        self.cfg = config or GameConfig()
        self.cfg.validate()

        self.screen: pygame.Surface | None = None
        self.clock: pygame.time.Clock | None = None
        self.running = False

        self.player_profiles = self.cfg.build_player_profiles()
        self.control_to_player = self._build_control_to_player_index(self.player_profiles)
        self.snakes: Dict[str, Snake] = self._create_snakes(self.player_profiles)

    def _build_control_to_player_index(self, players: Mapping[str, PlayerConfig]) -> Dict[int, str]:
        """Map key codes to player IDs and reject control collisions."""
        control_index: Dict[int, str] = {}
        for player_id, profile in players.items():
            for key in profile.controls:
                if key in control_index:
                    raise ValueError(f"Key {key} is assigned to multiple players")
                control_index[key] = player_id
        return control_index

    def _create_snakes(self, profiles: Mapping[str, PlayerConfig]) -> Dict[str, Snake]:
        """Instantiate all snakes from configured player profiles."""
        snakes: Dict[str, Snake] = {}
        for player_id, profile in profiles.items():
            snakes[player_id] = self._create_snake_from_profile(profile)
        return snakes

    @staticmethod
    def _create_snake_from_profile(profile: PlayerConfig) -> Snake:
        """Create a 3-segment snake aligned opposite to initial direction."""
        head_x, head_y = profile.spawn_head
        dir_x, dir_y = profile.initial_direction.vec
        body = deque(
            [
                (head_x, head_y),
                (head_x - dir_x, head_y - dir_y),
                (head_x - 2 * dir_x, head_y - 2 * dir_y),
            ]
        )
        return Snake(initial_body=body, initial_direction=profile.initial_direction)

    def initialize(self) -> None:
        pygame.init()
        self.screen = pygame.display.set_mode((self.cfg.window_width, self.cfg.window_height))
        pygame.display.set_caption("Snake (multiplayer-ready scaffold)")
        self.clock = pygame.time.Clock()
        self.running = True

    def run(self) -> None:
        """Run render loop and fixed-timestep movement updates."""
        self.initialize()

        assert self.clock is not None
        logic_step_ms = 1000.0 / self.cfg.logic_hz
        accumulated_ms = 0.0

        while self.running:
            frame_ms = self.clock.tick(60)
            accumulated_ms += frame_ms

            self._process_events()
            accumulated_ms = self._run_pending_logic_updates(accumulated_ms, logic_step_ms)
            self._render_frame()

        pygame.quit()

    def _run_pending_logic_updates(self, accumulated_ms: float, logic_step_ms: float) -> float:
        """Consume elapsed frame time in fixed-size logic ticks."""
        while accumulated_ms >= logic_step_ms:
            self._update_simulation()
            accumulated_ms -= logic_step_ms
        return accumulated_ms

    def _process_events(self) -> None:
        """Handle quit and player direction input events."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                self._handle_keydown(event.key)

    def _handle_keydown(self, key: int) -> None:
        """Route key press to the matching player's direction input."""
        player_id = self.control_to_player.get(key)
        if player_id is None:
            return

        profile = self.player_profiles[player_id]
        direction = profile.controls[key]
        self.snakes[player_id].set_direction(direction)

    def _update_simulation(self) -> None:
        """Move all snakes once per logic tick."""
        for snake in self.snakes.values():
            snake.move_snake(self.cfg.grid_width, self.cfg.grid_height)

    def _render_frame(self) -> None:
        """Draw grid + all snakes to the current frame."""
        assert self.screen is not None
        self.screen.fill(self.cfg.background_color)
        self._draw_grid()

        for player_id, snake in self.snakes.items():
            color = self.player_profiles[player_id].color
            self._draw_snake(snake, color)

        pygame.display.flip()

    def _draw_grid(self) -> None:
        """Draw 32px grid lines across the game area."""
        assert self.screen is not None
        c = self.cfg

        for x in range(0, c.window_width, c.cell_size):
            pygame.draw.line(self.screen, c.grid_line_color, (x, 0), (x, c.window_height))
        for y in range(0, c.window_height, c.cell_size):
            pygame.draw.line(self.screen, c.grid_line_color, (0, y), (c.window_width, y))

    def _draw_snake(self, snake: Snake, color: Tuple[int, int, int]) -> None:
        """Render a snake body as filled rectangles on the grid."""
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
