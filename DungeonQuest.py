# DungeonQuest.py
import pygame

import title
import login
import foundation
import config

if __name__ == "__main__":
    print("Main Game Started")
    pygame.init()
    
    screen = pygame.display.set_mode((config.WIDTH, config.HEIGHT))
    while True:
        if config.current_menu == config.SCREEN_MAIN_MENU:
            config.current_menu = title.show_title_screen(screen)
        elif config.current_menu == config.SCREEN_LOGIN_MENU:
            config.current_menu = login.show_login_screen(screen)
            print("Login Screen")
        elif config.current_menu == config.SCREEN_GAME:
            foundation.show_game_screen(screen)
            print("Game Screen")

