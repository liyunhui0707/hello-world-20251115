# Snake (2-player scaffold)

This repository contains a modular Snake starter using **Pygame**.

## Implemented

- Window: **960×640**
- Grid: **30×20** cells (32×32 each)
- Fixed logic tick rate: **10 updates/sec**
- Wrapping movement across screen edges
- **Snake A controls:** Arrow keys
- **Snake B controls:** WASD
- Both snakes update every logic tick
- Reversal is blocked (no instant 180° turn)
- Overlap prevention (head-on, body overlap, head swap)

## Multiplayer-ready architecture

- `snake_core.py` keeps movement rules independent from rendering
- `snake_game.py` uses per-player profiles (controls, color, spawn, direction)
- Input mapping is centralized and conflict-checked

## Run

```bash
python -m pip install pygame
python snake_game.py
```

## Tests

```bash
pytest -q
```

Covers wrapping, movement update, and defensive movement constraints.
