import pygame
import random

import config

def build_dungeon(screen: pygame.display, dungeon_grid: list[list[chr]]) -> list:
    """
    Build the dungeon on the screen
    :param screen: Current pygame display object
    :param dungeon_grid: 2D list of characters representing the dungeon
    :return: Updated pygame display object[0], collision data[1], entity data[2]

    dungeon_grid takes in a 2D list of characters representing the dungeon. The dungeon is built by iterating through the list.
    . -> Empty space
    W -> Wall
    X -> Enemy
    O -> Exit
    G -> Decorative grass
    The dungeon_grid should be the size of the screen grid.
    """
    TILE_SIZE = 60

    tile_wall = config.TILE_SET[config.WALL_TILE]
    tile_enemy = config.TILE_SET[config.DRAGON_TILE]
    tile_grass = config.TILE_SET[config.GRASS_TILE]
    tile_exit = config.TILE_SET[config.EXIT_TILE]

    colliders = []
    entities = []
    ent_colliders = []
    for row in range(len(dungeon_grid)):
        for col in range(len(dungeon_grid[row])):
            x, y = col * TILE_SIZE, row * TILE_SIZE

            if dungeon_grid[row][col] == 'W':
                screen.blit(tile_wall, (col * TILE_SIZE, row * TILE_SIZE))
                colliders.append(pygame.Rect(x, y, TILE_SIZE, TILE_SIZE))
            elif dungeon_grid[row][col] == 'X':
                screen.blit(tile_enemy, (col * TILE_SIZE, row * TILE_SIZE))
                # TODO: Create enemy and collidebox
                # Remember, this should be networked separate from the dungeon map!
                # Should probably even move this to a separate function
            elif dungeon_grid[row][col] == 'O':
                # TODO: Allow N, W, S, E exits
                screen.blit(tile_exit, (col * TILE_SIZE, row * TILE_SIZE))
                entities.append('O')
                ent_colliders.append(pygame.Rect(x, y, TILE_SIZE, TILE_SIZE))
            elif dungeon_grid[row][col] == 'G':
                screen.blit(tile_grass, (col * TILE_SIZE, row * TILE_SIZE))

    
    return [screen, colliders, [entities, ent_colliders]]