# DungeonQuest
This is a cloud-saving Dungeon Crawler developed with Pygame and designed to allow players to pick up and play their game from anywhere.
Our main goal with this project was to solve the problem of boredom by creating a game for others to play.

We had some of our project done and then after spring break,
decided to take things in a different direction. We plan to use this project as a learning experience in the future.

## Usage
From the repository root directory:
```
pip install -r requirements.txt
python3 ./src/main.py
```
Use arrow keys to move around.

Press ESC from the main game to quit the game.

### Admin-specific Usage
As an admin, you can change you can change your ID to any user that exists within the SQL database. This is done from the game menu before the main game. The users table is dumped to stdout for ease of use.

In the main game, press M to dump the users table into the terminal.

## Features
### Information Management (RBAC)
Role based access control is one feature of the game's database. It allows for a distiction between three types of users: Player, Winner, and Admin. Players are only allowed read and update access to the users tabel. Winners are allowed the same as Players, but also have the ability to read and update the seeds table, allowing other Winners to see the previous seeds. Admins have full CRUD access on all tables in the database.
```python
# Only permitted when logged in as a "Winner" user
cursor = config.sql_connection.cursor(dictionary=False)
cursor.execute('SELECT seed FROM dungeonquest.seeds')
seeds = cursor.fetchone()
```
### Secure Computing
Secure computing is achieved in this application through the user registration and login system. We securely store and compare hashed and salted passwords to prevent the security risk.
```python
hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
```
### Parallel Computing
In this game, parallel computing plays a role in the generation of the mazes. Specifically, a pool of processes is created to generate 5 mazes when a player starts a new game.
```python
 with multiprocessing.Pool() as pool:
        if config.seed == 0:
            config.seed = int(time.time())

        seeds = [(n, config.seed + n) for n in range(1, 6)]
        levels_data = pool.map(generate_dungeon_wrapper, seeds)
        for n, data in enumerate(levels_data, 1):
            config.levels[f'LEVEL_{n}'] = data
```

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
Early development, wrote the reports and distribution plan, server building, player menu

### Nico Milette
Parellel computation, dungeon generation, maze generation

### Evan Rudd
Database setup, role based access, backend networking
