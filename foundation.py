# main.py
import pygame
import os
import random
from pygame.locals import *

class MainGame:
    def __init__(self, logindata) -> None:
        # Initialize Pygame
        pygame.init()

        # Set up the game window
        width, height = 1280, 900
        screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption("Dungeon Quest")

        # Define player properties
        player_size = 50
        player_x, player_y = 0, height - player_size 
        player_speed = 2.5 * player_size  # Set speed to three times the size of one square
        key_pressed = False  # Flag to track whether a movement key is pressed


        # Get a list of image files in the "images" directory
        image_directory = "images"
        image_files = [f for f in os.listdir(image_directory) if f.endswith((".png", ".jpg", ".jpeg"))]

        # Randomly select an image for the player from the list
        player_image = pygame.image.load(os.path.join(image_directory, "player_image.png"))
        player_image = pygame.transform.scale(player_image, (player_size, player_size))

        # Game loop
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == QUIT:
                    running = False

                # Check for key press events
                if event.type == KEYDOWN:
                    key_pressed = True

                # Check for key release events
                if event.type == KEYUP:
                    key_pressed = False

                # Handle player movement
                keys = pygame.key.get_pressed()
                if keys[K_LEFT] and player_x > 0 and key_pressed:
                    player_x = max(0, player_x - player_speed)  # Ensure player stays within the left boundary
                    key_pressed = False  # Reset the flag after moving
                if keys[K_RIGHT] and player_x < width - player_size and key_pressed:
                    player_x = min(width - player_size, player_x + player_speed)  # Ensure player stays within the right boundary
                    key_pressed = False
                if keys[K_UP] and player_y > 0 and key_pressed:
                    player_y = max(0, player_y - player_speed)  # Ensure player stays within the top boundary
                    key_pressed = False
                if keys[K_DOWN] and player_y < height - player_size and key_pressed:
                    player_y = min(height - player_size, player_y + player_speed)  # Ensure player stays within the bottom boundary
                    key_pressed = False


            # Update game logic here

            # Draw the game elements here
            screen.fill((255, 255, 255))  # Fill the screen with a white background

            # Draw the background image
            background_image = pygame.image.load(os.path.join(image_directory, "background_image.png"))  # Replace with your background image file
            background_image = pygame.transform.scale(background_image, (width, height))
            screen.blit(background_image, (0, 0))

            # Draw the player image at the player's position
            screen.blit(player_image, (player_x, player_y))

            # Refresh the display
            pygame.display.flip()

        # Clean up
        pygame.quit()
