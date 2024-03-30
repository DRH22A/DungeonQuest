import pygame
import sys
import subprocess

def show_login_screen():
    pygame.init()

    # Set up the game window
    width, height = 1280, 900
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption("DungeonQuest Login Screen")

    # Set up font for buttons
    font = pygame.font.Font(None, 36)

    # Set up buttons
    sign_up_button = font.render("Sign Up", True, (255, 255, 255))
    sign_up_rect = sign_up_button.get_rect(center=(width // 2, height // 2 - 50))

    sign_in_button = font.render("Sign In", True, (255, 255, 255))
    sign_in_rect = sign_in_button.get_rect(center=(width // 2, height // 2 + 50))

    # Game loop
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # Check if the mouse click is within the buttons
                if sign_up_rect.collidepoint(event.pos):
                    # Handle sign-up logic
                    subprocess.run(["python", "sign_up.py"])
                elif sign_in_rect.collidepoint(event.pos):
                    # Handle sign-in logic
                    subprocess.run(["python", "sign_in.py"])

        # Fill the screen with black color
        screen.fill((0, 0, 0))

        # Draw the buttons
        screen.blit(sign_up_button, sign_up_rect.topleft)
        screen.blit(sign_in_button, sign_in_rect.topleft)

        # Refresh the display
        pygame.display.flip()

if __name__ == "__main__":
    show_login_screen()
