import pygame
import sys
import subprocess

import config

def show_title_screen(screen):
    width, height = config.WIDTH, config.HEIGHT
    pygame.display.set_caption("DungeonQuest Title Screen")

    background_image = pygame.image.load("images/title_background.png").convert_alpha()
    background_image = pygame.transform.scale(background_image, (width, height))

    font = pygame.font.Font(None, 36)
    start_button_text = "Start"
    start_button = font.render(start_button_text, True, (255, 255, 255))
    start_button_rect = start_button.get_rect(center=(width // 2, height - 50))

    square_width = start_button.get_width() + 20
    square_height = start_button.get_height() + 20
    square_x = width // 2 - square_width // 2
    square_y = height - 70 - square_height

    # Game loop
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if start_button_rect.collidepoint(event.pos):
                    # Return login menu enum instead of spawning new pygame window
                    return config.SCREEN_LOGIN_MENU

        screen.blit(background_image, (0, 0))
        pygame.draw.rect(screen, (0, 0, 0), (square_x, square_y, square_width, square_height))
        screen.blit(start_button, start_button_rect.topleft)

        pygame.display.flip()

if __name__ == "__main__":
    show_title_screen()
