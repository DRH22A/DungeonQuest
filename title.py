import pygame
import sys
import subprocess

def show_title_screen():
    pygame.init()

    # Set up the game window
    width, height = 1280, 900
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption("DungeonQuest Title Screen")

    # Load background image
    background_image = pygame.image.load("images/title_background.png").convert_alpha()
    background_image = pygame.transform.scale(background_image, (width, height))

    # Set up font for the "Start" button
    font = pygame.font.Font(None, 36)
    start_button_text = "Start"
    start_button = font.render(start_button_text, True, (255, 255, 255))
    start_button_rect = start_button.get_rect(center=(width // 2, height - 50))

    # Calculate the position and size of the black background square
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
                # Check if the mouse click is within the "Start" button area
                if start_button_rect.collidepoint(event.pos):
                    # Use subprocess to open login.py
                    subprocess.Popen(["python", "login.py"])
                    # Close title.py
                    pygame.quit()
                    sys.exit()

        # Draw the game elements
        screen.blit(background_image, (0, 0))
        pygame.draw.rect(screen, (0, 0, 0), (square_x, square_y, square_width, square_height))
        screen.blit(start_button, start_button_rect.topleft)

        # Refresh the display
        pygame.display.flip()

if __name__ == "__main__":
    show_title_screen()
