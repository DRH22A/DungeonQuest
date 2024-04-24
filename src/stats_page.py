import pygame
import player_menu

import config

# Set up the display
WIDTH, HEIGHT = config.WIDTH, config.HEIGHT
pygame.display.set_caption("Player Stats")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (128, 128, 128)

def draw_text(screen, text: str, color: tuple, pos: tuple):
    font = pygame.font.Font("resources/PixelOperator8.ttf", 16)
    txt_surface = font.render(text, True, color)
    screen.blit(txt_surface, pos)


def main_menu_button(screen):
    # Center the button horizontally, position it near the bottom of the screen
    button_rect = pygame.Rect((WIDTH - 200) // 2, HEIGHT - 100, 200, 50)
    pygame.draw.rect(screen, GRAY, button_rect)
    draw_text(screen, "Main Menu", BLACK, (button_rect.x + 50, button_rect.y + 15))
    return button_rect

def show_stats_screen(screen):
    # Dummy data for player stats
    total_runs_started = 0
    total_runs_completed = 0
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
        draw_text(screen, "Player Stats", (255, 255, 255), (WIDTH // 2, HEIGHT // 2 - 200))
        draw_text(screen, "Total Runs Started: {}".format(total_runs_started), (255, 255, 255), (WIDTH // 2, HEIGHT // 2 - 150))
        draw_text(screen, "Total Runs Completed: {}".format(total_runs_completed), (255, 255, 255), (WIDTH // 2, HEIGHT // 2 - 50))

        # Draw the main menu button
        main_menu_rect = main_menu_button(screen)

        pygame.display.flip()
