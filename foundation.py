# main.py
import pygame
from pygame.locals import *

from colorama import Fore, Back, Style

import config

def show_game_screen(screen):
    width, height = config.WIDTH, config.HEIGHT
    pygame.display.set_caption("Dungeon Quest")

    player_size = 50
    player_x, player_y = 0, height - player_size 
    player_speed = 2.5 * player_size/2
    key_pressed = False

    # Load tileset
    tileset = pygame.image.load("resources/tileset.png")
    tile_size = 16
    tiles = []
    for y in range(0, tileset.get_height(), tile_size):
        for x in range(0, tileset.get_width(), tile_size):
            tile = tileset.subsurface(x, y, tile_size, tile_size)
            tile = pygame.transform.scale(tile, (player_size * 1.1, player_size * 1.1))
            tiles.append(tile)
 
    player_name = pygame.font.Font("resources/PixelOperator8.ttf", 16).render(config.local_username, True, (255, 255, 255))

    print(Fore.BLUE + "Welcome to the gamebox!\n\t" +
          Fore.YELLOW + "Move using the screen, and act in the terminal.\n\t" +
          "Type 'exit' to leave the game.\n" + Style.RESET_ALL)
    print("> ", end="")

    # Game loop
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False

            if event.type == KEYDOWN:
                key_pressed = True

            if event.type == KEYUP:
                key_pressed = False

            keys = pygame.key.get_pressed()
            if keys[K_LEFT] and player_x > 0 and key_pressed:
                player_x = max(0, player_x - player_speed) 
                key_pressed = False
            if keys[K_RIGHT] and player_x < width - player_size and key_pressed:
                player_x = min(width - player_size, player_x + player_speed)
                key_pressed = False
            if keys[K_UP] and player_y > 0 and key_pressed:
                player_y = max(0, player_y - player_speed)
                key_pressed = False
            if keys[K_DOWN] and player_y < height - player_size and key_pressed:
                player_y = min(height - player_size, player_y + player_speed)
                key_pressed = False

        # Update game logic here

        screen.fill((0, 0, 0))
        screen.blit(tiles[config.CHARACTER_TILE], (player_x, player_y))
        screen.blit(player_name, (player_x, player_y - 15))

        pygame.display.flip()

    pygame.quit()
