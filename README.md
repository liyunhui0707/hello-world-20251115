# Snake (multiplayer-ready scaffold)

This repository contains a modular Snake starter using **Pygame**.

## Implemented

- Window: **960×640**
- Grid: **30×20** cells (32×32 each)
- Fixed logic tick rate: **10 updates/sec**
- Wrapping movement across screen edges
- Snake A controls: **Arrow keys**

## Multiplayer-ready architecture

- `snake_core.py` keeps movement rules independent from rendering
- `snake_game.py` supports **player profiles** (controls, color, spawn, direction)
- Input mapping is centralized and conflict-checked
- Game update/render loops already iterate over all snakes
- Snake B profile (WASD + different color) can be enabled with:

```python
SnakeGame(GameConfig(enable_snake_b=True)).run()
```

## Tests

```bash
pytest -q
```

Covers wrapping, movement update, and defensive direction constraints.
