# 🐍 Local 2-Player Snake (Python + Pygame)

A beginner-friendly **local multiplayer Snake mini-game** built with **Python 3** and **Pygame**.

This project is designed for two players on one keyboard:
- **Player A** controls one snake with **Arrow keys**
- **Player B** controls the other snake with **W / A / S / D**

Everything runs **fully offline** on your computer (no server, no online account, no internet gameplay).

---

## 🎮 Project Description

This is a classic Snake-style game with a local 2-player twist. Both snakes move on the same board, wrap around screen edges, and compete for points while avoiding collisions.

The game includes common arcade mechanics such as:
- collecting eggs/food,
- avoiding obstacles,
- handling snake-to-wall/body/snake collisions,
- and saving a high score locally.

---

## ✨ Features

- 2-player local gameplay on one keyboard
- Smooth grid-based snake movement
- **Wrap-around movement** at screen edges
- **Egg eating / food collection** gameplay
- **Obstacle** elements on the map
- Collision rules (self, opponent, and environment)
- Persistent **high score** saved in a local JSON file
- Offline-only play (no network features)

---

## ⌨️ Controls

### Player A
- **Move Up:** `↑`
- **Move Down:** `↓`
- **Move Left:** `←`
- **Move Right:** `→`

### Player B
- **Move Up:** `W`
- **Move Down:** `S`
- **Move Left:** `A`
- **Move Right:** `D`

---

## 🛠 Requirements

- Python **3.10+** (Python 3 recommended)
- `pygame`

---

## ▶️ How to Run

### 1) Clone or download this project

```bash
git clone <your-repo-url>
cd hello-world-20251115
```

### 2) (Recommended) Create and activate a virtual environment

#### macOS / Linux
```bash
python3 -m venv .venv
source .venv/bin/activate
```

#### Windows (PowerShell)
```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

### 3) Install dependencies

```bash
pip install pygame
```

### 4) Start the game

```bash
python snake_game.py
```

---

## 💾 Save File Behavior (High Score)

- The game stores high-score data in a local **JSON** file.
- The save file is created automatically when needed.
- If the save file is missing, the game starts with a default score and recreates it.
- If the save file is invalid/corrupted JSON, you can delete it and run the game again to regenerate it.
- Save data is local to your machine and is **not synced online**.

> Tip: Keep the JSON file if you want to preserve your best score between sessions.

---

## 📌 Notes

- This project is meant to be easy to read and extend.
- Good next steps: pause menu, sound effects, difficulty levels, and better sprites.
