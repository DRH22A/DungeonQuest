import random

import config


def generate_dungeon(seed, width=21, height=15, complexity=0.75):

    # Setup
    random.seed(seed)
    config.seed = seed
    dungeon = [['W' for _ in range(width)] for _ in range(height)]
    
    for x in range(width):
        dungeon[0][x] = 'W' 
        dungeon[height - 1][x] = 'W'  
    for y in range(height):
        dungeon[y][0] = 'W'  
        dungeon[y][width - 1] = 'W'  

    start_x, start_y = random.randint(3, width - 4), random.randint(3, height - 4)
    stack = [(start_x, start_y)]
    
    dungeon[start_y][start_x] = '.'

    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]

    # Create maze

    while stack:
        x, y = stack[-1]
        random.shuffle(directions)

        neighbors = []
        for dx, dy in directions:
            nx, ny = x + dx * 2, y + dy * 2
            if 1 <= nx < width - 1 and 1 <= ny < height - 1 and dungeon[ny][nx] == 'W':
                canCarve = True
                if dx != 0:  
                    if (1 <= ny - 1 and dungeon[ny - 1][nx] == '.') or (ny + 1 < height - 1 and dungeon[ny + 1][nx] == '.'):
                        canCarve = False
                elif dy != 0:  
                    if (1 <= nx - 1 and dungeon[ny][nx - 1] == '.') or (nx + 1 < width - 1 and dungeon[ny][nx + 1] == '.'):
                        canCarve = False
                if canCarve:
                    neighbors.append((nx, ny, x + dx, y + dy))



        if neighbors:
            nx, ny, px, py = random.choice(neighbors)
            dungeon[ny][nx] = '.'
            dungeon[py][px] = '.'  
            stack.append((nx, ny)) 
        else:
            stack.pop() 

    # Setup exits
  
    dungeon[1][0] = 'L'  
    dungeon[height - 2][width - 1] = 'R'  

    dungeon[1][1] = '.' 
    dungeon[height - 2][width - 2] = '.'

    dungeon[2][1] = '.'  
    dungeon[height - 2][width - 3] = '.' 
    
    dungeon[1][2] = '.'  
    dungeon[height - 3][width - 2] = '.' 


    return dungeon
