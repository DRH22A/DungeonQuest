import config

# TODO: Return dungeon grid instead of default spawn map
def generate_dungeon(seed, width=21, height=15, complexity=0.75):
    """
    Generates a dungeon map based on a given seed.
    :param seed: The seed for random number generator to ensure reproducibility.
    :param width: The width of the dungeon map.
    :param height: The height of the dungeon map.
    :param complexity: A factor influencing the number of features (rooms, corridors).
    :return: A grid representing the dungeon map.
    """
    # Set the random seed
    random.seed(seed)
    
    # Create an empty dungeon filled with walls (represented by 'W')
    dungeon = [['W' for _ in range(width)] for _ in range(height)]
    
    # Starting point (roughly in the middle)
    start_x, start_y = width // 2, height // 2
    dungeon[start_y][start_x] = '.'  # Open floor
    
    # Number of features to add (rooms, corridors)
    num_features = int(complexity * (width * height // 50))
    
    for _ in range(num_features):
        # Random direction (up, down, left, right)
        direction = random.choice(['up', 'down', 'left', 'right'])
        length = random.randint(2, 5)  # Random length of the corridor or room size
        
        new_x, new_y = start_x, start_y
        
        if direction == 'up':
            new_y = max(1, start_y - length)
        elif direction == 'down':
            new_y = min(height - 2, start_y + length)
        elif direction == 'left':
            new_x = max(1, start_x - length)
        elif direction == 'right':
            new_x = min(width - 2, start_x + length)
        
        # Carve a path in the selected direction
        while new_x != start_x or new_y != start_y:
            dungeon[new_y][new_x] = '.'
            if new_x > start_x:
                new_x -= 1
            elif new_x < start_x:
                new_x += 1
            if new_y > start_y:
                new_y -= 1
            elif new_y < start_y:
                new_y += 1
    
    return dungeon