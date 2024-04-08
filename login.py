import pygame
import sys
import subprocess

import config

def show_login_screen(screen):
    width, height = config.WIDTH, config.HEIGHT
    pygame.display.set_caption("DungeonQuest Login Screen")

    font = pygame.font.Font(None, 36)

    sign_up_button = font.render("Sign Up", True, (255, 255, 255))
    sign_up_rect = sign_up_button.get_rect(center=(width // 2, height // 2 - 50))

    sign_in_button = font.render("Sign In", True, (255, 255, 255))
    sign_in_rect = sign_in_button.get_rect(center=(width // 2, height // 2 + 50))

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONUP:
                if sign_up_rect.collidepoint(event.pos):
                    subprocess.run(["python", "sign_up.py"])
                elif sign_in_rect.collidepoint(event.pos):
                    subprocess.run(["python", "sign_in.py"])

        screen.fill((0, 0, 0))

        screen.blit(sign_up_button, sign_up_rect.topleft)
        screen.blit(sign_in_button, sign_in_rect.topleft)

        pygame.display.flip()

if __name__ == "__main__":
    show_login_screen()
