'''
import pygame
import sys
import config

pygame.init()

# Set up the display
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Player Stats")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (128, 128, 128)
GREEN = (0, 255, 0)

# Fonts
font = pygame.font.SysFont(None, 40)
small_font = pygame.font.SysFont(None, 30)

def draw_text(screen, text: str, color: tuple, pos: tuple):
    font = pygame.font.Font("resources/PixelOperator8.ttf", 16)
    txt_surface = font.render(text, True, color)
    screen.blit(txt_surface, pos)

def show_stats_screen(screen):
    width, height = config.WIDTH, config.HEIGHT

    # Dummy data for player stats
    total_score = 1000
    total_deaths = 5
    total_runs = 20

    # Define the main menu button rectangle
    button_width = 200
    button_height = 50
    main_menu_rect = pygame.Rect((width - button_width) // 2, height - 100, button_width, button_height)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if main_menu_rect.collidepoint(event.pos):  # Check if the main menu button is clicked
                    return config.SCREEN_PLAYER_MENU  # Return to the player menu

        # Clear the screen
        screen.fill((0, 0, 0))

        # Display player stats
        draw_text(screen, "Player Stats", (255, 255, 255), (width // 2, height // 2 - 200))
        draw_text(screen, "Total Score: {}".format(total_score), (255, 255, 255), (width // 2, height // 2 - 150))
        draw_text(screen, "Total Deaths: {}".format(total_deaths), (255, 255, 255), (width // 2, height // 2 - 100))
        draw_text(screen, "Total Runs: {}".format(total_runs), (255, 255, 255), (width // 2, height // 2 - 50))

        # Draw the main menu button
        pygame.draw.rect(screen, GRAY, main_menu_rect)
        draw_text(screen, "Main Menu", BLACK, ((width - button_width) // 2 + 50, height - 80))  # Adjust text position

        pygame.display.flip()

if __name__ == "__main__":
    show_stats_screen(screen)
'''