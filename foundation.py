# main.py
import pygame
from pygame.locals import *

from colorama import Fore, Back, Style

import config
from dungeon_builder_helper import build_dungeon

def show_game_screen(screen):
    width, height = config.WIDTH, config.HEIGHT
    pygame.display.set_caption("Dungeon Quest")
    pygame.key.set_repeat(1, 1)

    player_size = 50
    collision_size = 32

    player_x = round((width // 2) / 60) * 60
    player_y = round((height // 2) / 60) * 60

    player_speed = 2.5 * player_size/2
    key_pressed = False
    player_rect = pygame.Rect(player_x - 15, player_y - 20, collision_size, collision_size) 

    # Load tileset
    tileset = pygame.image.load("resources/tileset.png")
    tile_size = 16
    tiles = []
    for y in range(0, tileset.get_height(), tile_size):
        for x in range(0, tileset.get_width(), tile_size):
            tile = tileset.subsurface(x, y, tile_size, tile_size)
            tile = pygame.transform.scale(tile, (player_size * 1.1, player_size * 1.1))
            tiles.append(tile)

    config.TILE_SET = tiles

    dungeon_grid = config.SPAWN_MAP
 
    player_name = pygame.font.Font("resources/PixelOperator8.ttf", 16).render(config.local_username, True, (255, 255, 255))

    print(Fore.BLUE + "Welcome to the gamebox!\n" +
          Fore.YELLOW + "Move using the screen, and act in the terminal.\n" +
          "Type 'exit' to leave the game.\n" + Style.RESET_ALL)
    print("> ", end="")
    # TODO: Chatbox

    # Game loop
    colliders, exits, entities = [], [], []

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYUP:
                key_pressed = False

            keys = pygame.key.get_pressed()
            old_position = player_rect.topleft

            if event.type == pygame.KEYDOWN and not key_pressed:
                if keys[pygame.K_LEFT] and player_rect.x > 0:
                    player_rect.move_ip(-player_speed, 0)
                    if any(player_rect.colliderect(c) for c in colliders):
                        player_rect.topleft = old_position
                if keys[pygame.K_RIGHT] and player_rect.x < width - player_size:
                    player_rect.move_ip(player_speed, 0)
                    if any(player_rect.colliderect(c) for c in colliders):
                        player_rect.topleft = old_position
                if keys[pygame.K_UP] and player_rect.y > 0:
                    player_rect.move_ip(0, -player_speed)
                    if any(player_rect.colliderect(c) for c in colliders):
                        player_rect.topleft = old_position
                if keys[pygame.K_DOWN] and player_rect.y < height - player_size:
                    player_rect.move_ip(0, player_speed)
                    if any(player_rect.colliderect(c) for c in colliders):
                        player_rect.topleft = old_position

                key_pressed = True

        player_x, player_y = player_rect.topleft

        screen.fill((0, 0, 0))

        screen, colliders, entities, exits = build_dungeon(screen, dungeon_grid)

        #
        # MAIN GAME LOGIC START
        #

        for i, _ in enumerate(exits[0]):
            # TODO: Handle exit logic
            if player_rect.colliderect(exits[1][i]):
                print(Fore.GREEN + "You found an exit: " + exits[0][i] + Style.RESET_ALL)
            
        #
        # MAIN GAME LOGIC END
        #

    
        screen.blit(tiles[config.CHARACTER_TILE], (player_x, player_y))
        screen.blit(player_name, (player_x, player_y - 15))

        pygame.display.flip()

    pygame.quit()
