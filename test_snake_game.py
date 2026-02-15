import pytest

pygame = pytest.importorskip("pygame")

from snake_game import GameConfig, SnakeGame


def test_snake_a_can_eat_egg_and_grow():
    game = SnakeGame(GameConfig())
    game.egg_position = (3, 2)  # Next cell for Snake A from default spawn.

    len_a_before = len(game.snakes["snake_a"].body)
    len_b_before = len(game.snakes["snake_b"].body)

    game._update_simulation()

    assert len(game.snakes["snake_a"].body) == len_a_before + 1
    assert len(game.snakes["snake_b"].body) == len_b_before


def test_snake_b_can_eat_egg_and_grow():
    game = SnakeGame(GameConfig())
    game.egg_position = (26, 17)  # Next cell for Snake B from default spawn.

    len_a_before = len(game.snakes["snake_a"].body)
    len_b_before = len(game.snakes["snake_b"].body)

    game._update_simulation()

    assert len(game.snakes["snake_a"].body) == len_a_before
    assert len(game.snakes["snake_b"].body) == len_b_before + 1
