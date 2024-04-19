import random

def generate_dungeon(seed, width=21, height=15, complexity=0.75):
    random.seed(seed)
    # Initialize the dungeon with walls
    dungeon = [['W' for _ in range(width)] for _ in range(height)]
    
    # Ensure walls on all sides
    for x in range(width):
        dungeon[0][x] = 'W'  # Top wall
        dungeon[height - 1][x] = 'W'  # Bottom wall
    for y in range(height):
        dungeon[y][0] = 'W'  # Left wall
        dungeon[y][width - 1] = 'W'  # Right wall

    # Start randomly inside the grid but not on the edge
    start_x, start_y = random.randint(3, width - 4), random.randint(3, height - 4)
    stack = [(start_x, start_y)]
    
    # Set the starting point as a path
    dungeon[start_y][start_x] = '.'

    # Directions: up, down, left, right
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]

    while stack:
        x, y = stack[-1]
        # Randomize directions to ensure randomness in path creation
        random.shuffle(directions)

        neighbors = []
        for dx, dy in directions:
            nx, ny = x + dx * 2, y + dy * 2
            if 1 <= nx < width - 1 and 1 <= ny < height - 1 and dungeon[ny][nx] == 'W':
                # Check only along the direction of dx, dy to avoid isolating any cell
                canCarve = True
                if dx != 0:  # Horizontal movement
                    if (1 <= ny - 1 and dungeon[ny - 1][nx] == '.') or (ny + 1 < height - 1 and dungeon[ny + 1][nx] == '.'):
                        canCarve = False
                elif dy != 0:  # Vertical movement
                    if (1 <= nx - 1 and dungeon[ny][nx - 1] == '.') or (nx + 1 < width - 1 and dungeon[ny][nx + 1] == '.'):
                        canCarve = False
                if canCarve:
                    neighbors.append((nx, ny, x + dx, y + dy))



        if neighbors:
            nx, ny, px, py = random.choice(neighbors)
            dungeon[ny][nx] = '.'
            dungeon[py][px] = '.'  # Open the path between the current cell and the chosen neighbor
            stack.append((nx, ny))  # Add new position to stack
        else:
            stack.pop()  # Backtrack if no unvisited neighbors


    # Set entrance and exit
    dungeon[1][0] = 'L'  # Entrance on the left side
    dungeon[height - 2][width - 1] = 'R'  # Exit on the right side

    dungeon[1][1] = '.'  # Entrance on the left side
    dungeon[height - 2][width - 2] = '.'  # Exit on the right side

    dungeon[2][1] = '.'  # Entrance on the left side
    dungeon[height - 2][width - 3] = '.'  # Exit on the right side
    
    dungeon[1][2] = '.'  # Entrance on the left side
    dungeon[height - 3][width - 2] = '.'  # Exit on the right side


    return dungeon
