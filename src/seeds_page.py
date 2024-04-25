import pygame
import player_menu

import config

# Set up the display
WIDTH, HEIGHT = config.WIDTH, config.HEIGHT
pygame.display.set_caption("Set Seed")

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

def submit_button(screen):
    # Center the button horizontally, position it near the bottom of the screen
    button_rect = pygame.Rect((WIDTH - 200) // 2, HEIGHT // 2 + 50, 200, 50)
    pygame.draw.rect(screen, GRAY, button_rect)
    draw_text(screen, "Submit", BLACK, (button_rect.x + 50, button_rect.y + 15))
    return button_rect

def show_seeds_screen(screen):
    # Initialize seed value
    seed = ""

    # Adjust dimensions of the input box
    input_box_width = 200  # Twice as long as before
    input_box_height = 45  # 1.5 times bigger

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if main_menu_rect.collidepoint(event.pos):  # Check if the main menu button is clicked
                    return config.SCREEN_PLAYER_MENU  # Return to the player menu
                elif submit_button_rect.collidepoint(event.pos):  # Check if the submit button is clicked
                    config.seed = int(seed)  # Set the seed value
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:  # Set seed when Enter key is pressed
                    config.seed = int(seed)
                elif event.key == pygame.K_BACKSPACE:  # Remove last character if Backspace is pressed
                    seed = seed[:-1]
                else:
                    seed += event.unicode  # Add pressed key to seed

        # Clear the screen
        screen.fill((0, 0, 0))

        # Display seed input box
        draw_text(screen, "Enter Seed:", WHITE, (WIDTH // 2 - 100, HEIGHT // 2 - 70))
        pygame.draw.rect(screen, WHITE, (WIDTH // 2 - input_box_width // 2, HEIGHT // 2 - 20, input_box_width, input_box_height))
        draw_text(screen, seed, BLACK, (WIDTH // 2 - input_box_width // 2 + 5, HEIGHT // 2))

        # Draw the main menu button
        main_menu_rect = main_menu_button(screen)

        # Draw the submit button
        submit_button_rect = submit_button(screen)

        pygame.display.flip()
