# Jump Ball

A simple Pygame platform-jumping game where you control a ball and try to climb as high as possible.

## How to Play

- Use `A` or `←` to move left
- Use `D` or `→` to move right
- Jumping is automatic when the ball lands on a platform
- Avoid falling off the bottom of the screen
- Collect items and progress through menus as shown in the game UI

## Build / Run

1. Install Python 3.8+ if you do not already have it.
2. Run the game from the project folder:

```bash
python main.py
```
or
```bash
py main.py
```

## Project Structure

- `main.py` - game entrypoint
- `settings.py` - game settings and constants
- `assets/` - images, audio, and game resources
- `entities/` - player, enemies, platforms, and collectibles
- `screens/` - game screens and menu flow
- `managers/` - asset, audio, and data managers
- `utils/` - helper utilities

Enjoy the game!