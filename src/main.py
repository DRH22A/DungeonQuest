# DungeonQuest.py
import contextlib
with contextlib.redirect_stdout(None):
    import pygame

import title
import login
import foundation
import player_menu
import config
import seeds_page
import admin_menu

from colorama import Fore, Back, Style

if __name__ == "__main__":
    pygame.init()
    pygame.mixer.init()

    main_menu_music = pygame.mixer.Sound("resources/main_menu_music.wav")
    
    main_menu_music.play()
    
    screen = pygame.display.set_mode((config.WIDTH, config.HEIGHT))

    print(Fore.BLACK + Back.GREEN + "Welcome to DUNGEON QUEST!" + Style.RESET_ALL)

    while True:
        # Loads Main Menu
        if config.current_menu == config.SCREEN_MAIN_MENU:
            config.current_menu = title.show_title_screen(screen)
        # Loads Login Screen
        elif config.current_menu == config.SCREEN_LOGIN_MENU:
            config.current_menu = login.show_login_screen(screen)
        # Loads Player Menu
        elif config.current_menu == config.SCREEN_PLAYER_MENU:
            config.current_menu = player_menu.show_player_menu(screen)
        #Loads Game
        elif config.current_menu == config.SCREEN_GAME:
            main_menu_music.stop()
            foundation.show_game_screen(screen)
        # Loads Stats Page
        elif config.current_menu == config.SEEDS:
            config.current_menu = seeds_page.show_seeds_screen(screen)  
        elif config.current_menu == config.SCREEN_ADMIN_MENU:
            config.current_menu = admin_menu.show_admin_menu(screen)