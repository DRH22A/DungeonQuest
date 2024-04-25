import pygame
import sys
import os

from colorama import Fore, Back, Style

import config
from textbox import InputBox

def draw_text(screen, text: str, color: tuple, pos: tuple):
    font = pygame.font.Font("resources/PixelOperator8.ttf", 16)
    txt_surface = font.render(text, True, color)
    screen.blit(txt_surface, pos)


def show_player_menu(screen):
    width, height = config.WIDTH, config.HEIGHT

    # Define button width and height
    button_width = 200
    button_height = 40

    # Adjust the button positions accordingly
    start_button = pygame.Rect(width // 2 - button_width // 2 + 25, height // 2 - 100, button_width, button_height)
    seeds_button = pygame.Rect(width // 2 - button_width // 2 + 25, height // 2 - 40, button_width, button_height)
    exit_button = pygame.Rect(width // 2 - button_width // 2 + 25, height // 2 + 40, button_width, button_height)

    if config.admin:
        admin_button = pygame.Rect(width // 2 - button_width // 2 + 25, height // 2 - 150, button_width, button_height)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = event.pos
                if start_button.collidepoint(mouse_pos):
                    return config.SCREEN_GAME
                elif seeds_button.collidepoint(mouse_pos):
                    return config.SEEDS
                elif config.admin and admin_button.collidepoint(mouse_pos):
                    return config.SCREEN_ADMIN_MENU
                elif exit_button.collidepoint(mouse_pos):
                    pygame.quit()
                    quit()

        # Draw the menu buttons
        screen.fill((0, 0, 0))
        pygame.draw.rect(screen, (0, 0, 0), start_button)
        pygame.draw.rect(screen, (0, 0, 0), seeds_button)
        pygame.draw.rect(screen, (0, 0, 0), exit_button)

        # Button labels
        draw_text(screen, "Start", (255, 255, 255), (width // 2, height // 2 - 90))
        draw_text(screen, "Seeds", (255, 255, 255), (width // 2, height // 2 - 30))
        draw_text(screen, "Exit", (255, 255, 255), (width // 2 + 10, height // 2 + 50))

        if config.admin:
            pygame.draw.rect(screen, (0, 0, 0), admin_button)
            draw_text(screen, "Admin Menu", (255, 255, 255), (width // 2 - 40, height // 2 - 150))

        pygame.display.flip()
