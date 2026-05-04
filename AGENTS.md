# ArcSpace - Agent Instructions

## Running the Game

```bash
pip install -r requirements.txt
python main.py
```

## Project Structure

- `main.py` - Single-file Pygame game (~245 lines)
- `data/` - JSON files for game data (`astros.json`, `scores.json`)
- `assets/` - Graphics and fonts (Silkscreen font, keyboard icons, star sprite)

## Key Details

- **No tests** exist in this repository
- **No build/lint/typecheck** tooling configured
- Game uses Pygame for rendering; keyboard controls: arrow keys or WASD for movement, SPACE to take photos
- Entry point is `main.py`; no additional CLI interface
- Virtual environment is pre-configured in `.venv/`

## Development Notes

- Main game loop uses simple state machine: menu → playing → (back to menu)
- Sprites: `Camara` (player/visor), `Astro` (celestial objects with proximity-based visibility)
- Data files are loaded at runtime; modify `data/astros.json` to change game objects