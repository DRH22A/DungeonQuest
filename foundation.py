# main.py
import pygame
from pygame.locals import *
import threading

from colorama import Fore, Back, Style

import config
from dungeon_builder import build_dungeon
from dungeon_generator import generate_dungeon
from textbox import InputBox

def show_game_screen(screen):
    width, height = config.WIDTH, config.HEIGHT
    pygame.display.set_caption("Dungeon Quest")
    pygame.key.set_repeat(1, 1)

    player_size = config.VISUAL_TILE_SIZE
    collision_size = player_size

    player_x = round((width // 2) / player_size) * player_size
    player_y = round((height // 2) / player_size) * player_size

    player_speed = player_size
    key_pressed = False
    player_rect = pygame.Rect(player_x, player_y, collision_size, collision_size) 

    # Load tileset
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

    # Game loop
    colliders, exits = [], []
    
    while config.running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                config.running = False

            if event.type == pygame.KEYUP:
                key_pressed = False

            keys = pygame.key.get_pressed()
            old_position = player_rect.topleft

            if event.type == pygame.KEYDOWN and not key_pressed:
                if keys[pygame.K_LEFT] and player_rect.x > 0:
                    player_rect.move_ip(-player_speed, 0)
                if keys[pygame.K_RIGHT] and player_rect.x < width - player_size:
                    player_rect.move_ip(player_speed, 0)
                if keys[pygame.K_UP] and player_rect.y > 0:
                    player_rect.move_ip(0, -player_speed)
                if keys[pygame.K_DOWN] and player_rect.y < height - player_size:
                    player_rect.move_ip(0, player_speed)
 
                if any(player_rect.colliderect(c) for c in colliders):
                    player_rect.topleft = old_position

                key_pressed = True

        player_x, player_y = player_rect.topleft

        screen.fill((0, 0, 0))

        if config.current_level == 0:
            screen, colliders, exits = build_dungeon(screen, config.SPAWN_MAP)
        else:
            screen, colliders, exits = build_dungeon(screen, generate_dungeon('N'))

        #
        # MAIN GAME LOGIC START
        #

        for i, _ in enumerate(exits[0]):
            if player_rect.colliderect(exits[1][i]):
                screen, colliders, exits = build_dungeon(screen, generate_dungeon(exits[0][i]))
                if exits[0][i] == 'R':
                    player_x = round((width // 10) / player_size) * player_size
                    player_y = round((height // 2) / player_size) * player_size
                elif exits[0][i] == 'L':
                    player_x = round((width - (width // 10)) / player_size) * player_size
                    player_y = round((height // 2) / player_size) * player_size
                elif exits[0][i] == 'U':
                    player_x = round((width // 2) / player_size) * player_size
                    player_y = round((height - (height // 9)) / player_size) * player_size
                else:
                    player_x = round((width // 2) / player_size) * player_size
                    player_y = round((height // 10) / player_size) * player_size

                player_rect = pygame.Rect(player_x, player_y, collision_size, collision_size) 
                config.current_level += 1

        if config.current_level >= 10:
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

        pygame.display.flip()

    print(Fore.BLUE + "Goodbye!" + Style.RESET_ALL)
    pygame.quit()
