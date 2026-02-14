# Snake (2P scaffold)

This repository now contains a modular starter implementation of a 2-player Snake game using **Pygame**, currently with **Snake A** movement only.

## Implemented

- Window: **960×640**
- Grid: **30×20** cells (32×32 each)
- Fixed logic tick rate: **10 updates/sec**
- Snake A movement with **Arrow keys**
- Screen-edge wrapping

## Run

```bash
python -m pip install pygame
python snake_game.py
```

## Next steps

- Add Snake B (WASD or other controls)
- Food/spawn system
- Growth and collision handling
- Score and game over states
