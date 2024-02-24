# title.py
import pygame
import sys
import subprocess

def show_title_screen():
    pygame.init()

    # Set up the game window
    width, height = 800, 600
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption("DungeonQuest Title Screen")

    # Load background image
    background_image = pygame.image.load("images/title_background.png")
    background_image = pygame.transform.scale(background_image, (width, height))

    # Set up font for the "Start" button
    font = pygame.font.Font(None, 36)
    start_button = font.render("Start", True, (255, 255, 255))
    start_button_rect = start_button.get_rect(center=(width // 2, height // 2))

    # Game loop
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                # Start the main game when a key is pressed
                return
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # Check if the mouse click is within the "Start" button area
                if start_button_rect.collidepoint(event.pos):

        # Draw the game elements
        screen.blit(background_image, (0, 0))
        screen.blit(start_button, start_button_rect.topleft)

        # Refresh the display
        pygame.display.flip()

if __name__ == "__main__":
    show_title_screen()
