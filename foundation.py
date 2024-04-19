# main.py
import pygame
from pygame.locals import *
import threading
import multiprocessing
from colorama import Fore, Back, Style

import config
from dungeon_builder import build_dungeon
from dungeon_generator import generate_dungeon
from textbox import InputBox
import time

def generate_dungeon_wrapper(level_seed):
    level, seed = level_seed
    print(f"Process starting for seed: {seed}, level: {level}")
    start_time = time.perf_counter()
    
    # Linear scaling of complexity from 0.5 to 1.0 based on level
    if level <= 10:
        complexity = 0.1 + (0.9 * ((level - 1) / 9) ** 2)  # Exponential growth within first 10 levels
    else:
        complexity = 1.0  # Maximum complexity for levels beyond 10
    result = generate_dungeon(seed=seed, complexity=complexity)
    end_time = time.perf_counter()
    duration = end_time - start_time
    print(f"Process finished for seed: {seed}, Level: {level}, Duration: {duration:.5f} seconds")
    return result


def show_game_screen(screen):
    width, height = config.WIDTH, config.HEIGHT
    pygame.display.set_caption("Dungeon Quest")
    pygame.key.set_repeat(1, 1)

    player_size = config.VISUAL_TILE_SIZE
    collision_size = player_size

    player_x = round((width // 2) / player_size) * player_size
    player_y = round((height // 2) / player_size) * player_size

    player_speed = 0.1 
    player_velocity = pygame.math.Vector2(0, 0)
    player_acceleration = 0.5  # How quickly the player can change speed
    friction = 0.9  # Simulate friction to stop the player smoothly

    player_speed = player_size
    key_pressed = False
    player_rect = pygame.Rect(player_x, player_y, collision_size, collision_size) 

    # Load tileset
    level_font = pygame.font.Font("resources/PixelOperator8.ttf", 24)
    tileset = pygame.image.load("resources/tileset.png")
    tile_size = 16
    tiles = []
    for y in range(0, tileset.get_height(), tile_size):
        for x in range(0, tileset.get_width(), tile_size):
            tile = tileset.subsurface(x, y, tile_size, tile_size)
            tile = pygame.transform.scale(tile, (player_size, player_size))
            tiles.append(tile)

    config.TILE_SET = tiles

    player_name = pygame.font.Font("resources/PixelOperator8.ttf", 16).render(config.local_username, True, (255, 255, 255))

    with multiprocessing.Pool() as pool:
        seeds = [(n, int(time.time()) + n) for n in range(1, 11)]
        levels_data = pool.map(generate_dungeon_wrapper, seeds)
        for n, data in enumerate(levels_data, 1):
            config.levels[f'LEVEL_{n}'] = data


    # Game loop
    colliders, exits = [], []
    
    while config.running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                config.running = False

        keys = pygame.key.get_pressed()

        # Reset velocity each frame
        player_velocity *= friction

        # Update velocity based on key presses
        if keys[pygame.K_LEFT]:
            player_velocity.x -= player_acceleration
        if keys[pygame.K_RIGHT]:
            player_velocity.x += player_acceleration
        if keys[pygame.K_UP]:
            player_velocity.y -= player_acceleration
        if keys[pygame.K_DOWN]:
            player_velocity.y += player_acceleration

        # Update player position based on velocity
        player_rect.x += player_velocity.x
        player_rect.y += player_velocity.y

        # Check for collisions after moving
        if any(player_rect.colliderect(c) for c in colliders):
            player_rect.x -= player_velocity.x  # Move back horizontally
            player_rect.y -= player_velocity.y  # Move back vertically

        player_x, player_y = player_rect.topleft

        screen.fill((0, 0, 0))

        if config.current_level == 0:
            screen, colliders, exits = build_dungeon(screen, config.SPAWN_MAP)
        elif config.current_level > 10:
            screen, colliders, exits = build_dungeon(screen, config.VICTORY_MAP)
        else:
            level_key = f'LEVEL_{config.current_level}'
            if level_key in config.levels:
                screen, colliders, exits = build_dungeon(screen, config.levels[level_key])
            else:
                screen, colliders, exits = build_dungeon(screen, generate_dungeon(config.SPAWN_MAP))


        #
        # MAIN GAME LOGIC START
        #

        for i, _ in enumerate(exits[0]):
            if exits and i < len(exits[0]) and player_rect.colliderect(exits[1][i]):
                if exits[0][i] == 'R':
                    player_x = round((width // 20) / player_size) * player_size
                    player_y = round((height // 20) / player_size) * player_size
                    config.current_level += 1
                elif exits[0][i] == 'L':
                    player_x = round((width - (width // 10)) / player_size) * player_size
                    player_y = round((height - (height // 9)) / player_size) * player_size
                    config.current_level -= 1
                elif exits[0][i] == 'U':
                    player_x = round((width // 2) / player_size) * player_size
                    player_y = round((height - (height // 9)) / player_size) * player_size
                else:
                    player_x = round((width // 2) / player_size) * player_size
                    player_y = round((height // 10) / player_size) * player_size

                player_rect = pygame.Rect(player_x, player_y, collision_size, collision_size)

                

        if config.current_level > 10:
            screen, colliders, exits = build_dungeon(screen, config.VICTORY_MAP)

            winner_text = pygame.font.Font("resources/PixelOperator8.ttf", 16).render("YOU ARE A WINNER!", True, (255, 215, 0))
            delete_text = pygame.font.Font("resources/PixelOperator8.ttf", 11).render("Exit the game to delete your account and play again!", True, (255, 255, 255))
            screen.blit(winner_text, ((width / 2) - (winner_text.get_width() / 2), height / 2 - 50))
            screen.blit(delete_text, ((width / 2) - (delete_text.get_width() / 2), (height / 2) - (delete_text.get_height()) - 10))

            
        #
        # MAIN GAME LOGIC END
        #

        
        screen.blit(tiles[config.CHARACTER_TILE], (player_x, player_y))
        screen.blit(player_name, (player_x, player_y - 15))

        if 1 <= config.current_level <= 10:
            level_text = level_font.render(f"Level: {config.current_level}", True, (0, 0, 0))
            screen.blit(level_text, (10, 10))  # Position at top-left corner


        pygame.display.flip()

    print(Fore.BLUE + "Goodbye!" + Style.RESET_ALL)
    pygame.quit()
