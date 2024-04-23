import pygame
import sys
import subprocess

import config

def show_title_screen(screen):
    width, height = config.WIDTH, config.HEIGHT
    pygame.display.set_caption("DungeonQuest Title Screen")

    font = pygame.font.Font("resources/PixelOperator8.ttf", 36)
    start_button_text = "JOIN GAME"
    start_button = font.render(start_button_text, True, (255, 255, 255))
    start_button_rect = start_button.get_rect(center=(width // 2, height // 1.5))

    ascii_logo = pygame.image.load('resources/ascii_logo.png')
    logo_width, logo_height = ascii_logo.get_size()
    ascii_logo = pygame.transform.scale(ascii_logo, (int(logo_width * 0.6), int(logo_height * 0.6)))

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if start_button_rect.collidepoint(event.pos):
                    return config.SCREEN_LOGIN_MENU

        logo_width, logo_height = ascii_logo.get_size()
        position = ((width - logo_width) // 2, (height - logo_height) // 2 - 100)

        screen.blit(ascii_logo, position)
        screen.blit(start_button, start_button_rect)

        pygame.display.flip()

if __name__ == "__main__":
    show_title_screen()
