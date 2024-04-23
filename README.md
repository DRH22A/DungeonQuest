# DungeonQuest
This is a cloud-saving Dungeon Crawler developed with Pygame and designed to allow players to pick up and play their game from anywhere.
Our main goal with this project was to solve the problem of boredom by creating a game for others to play.
We did not achieve everything we set out for when it comes to game mechanics, but we feel that we displayed the elements of parallelization, 
distributed computing, secure computing, and information management well. We had some of our project done and then after spring break,
decided to take things in a different direction. We plan to use this project as a learning experience in the future.

## Usage
```
pip install -r requirements.txt
python3 ./src/main.py
```
Use arrow keys to move around.
Press ESC from the main game to quit the game.
### Admin-specific Usage
Press M to dump the users table into the terminal.

## Features
- Parallel dungeon generation
- Cloud-based saves via MySQL and AWS
- Admin-based access and data manipulation

## Libraries
See `requirements.txt`

## Resources
- PixelOperator Font (Public domain)
- Tileset (https://dwarffortresswiki.org/Tileset_repository)
- Main menu music (https://www.youtube.com/watch?v=CukIc8pfmXI)
- Other sound effects (https://df.zweistein.cz/soundsense/)

## Separation of work
### Jack Brower
Graphics & UI, dungeon building, game logic, project structure

### Daniel Halterman
Early development, wrote the reports, server building, player menu, comments

### Nico Milette
Parellel computation, dungeon generation, maze generation

### Evan Rudd
Database setup, role based access, backend networking