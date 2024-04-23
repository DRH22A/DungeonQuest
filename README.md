# DungeonQuest
This is a cloud-saving Dungeon Crawler developed with Pygame and designed to allow players to pick up and play their game from anywhere.

## Usage
```
pip install -r requirements.txt
python3 ./src/main.py
```
Use arrow keys to move around.

## Features
- Parallel dungeon generation
- Cloud-based saves via MySQL and AWS
- Admin-based access and data manipulation

## Libraries
See `requirements.txt`

## Resources
- PixelOperator Font (Public domain)
- Tileset (https://dwarffortresswiki.org/Tileset_repository)

## Separation of work
### Jack Brower
Graphics & UI, dungeon building, game logic, project structure

### Daniel Halterman
Early development, wrote the reports, server building, player menu, account bound resources

### Nico Milette
Parellel computation, dungeon generation, maze generation

### Evan Rudd
Database setup, role based access, backend networking