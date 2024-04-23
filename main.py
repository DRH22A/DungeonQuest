# DungeonQuest.py
import contextlib
with contextlib.redirect_stdout(None):
    import pygame

import title
import login
import foundation
import player_menu
import config
import stats_page

from colorama import Fore, Back, Style

if __name__ == "__main__":
    pygame.init()
    
    screen = pygame.display.set_mode((config.WIDTH, config.HEIGHT))

    print(Fore.BLACK + Back.GREEN + "Welcome to DUNGEON QUEST!" + Style.RESET_ALL)

    while True:
        if config.current_menu == config.SCREEN_MAIN_MENU:
            config.current_menu = title.show_title_screen(screen)
        elif config.current_menu == config.SCREEN_LOGIN_MENU:
            config.current_menu = login.show_login_screen(screen)
        elif config.current_menu == config.SCREEN_PLAYER_MENU:
            config.current_menu = player_menu.show_player_menu(screen)
        elif config.current_menu == config.SCREEN_GAME:
            foundation.show_game_screen(screen)
        elif config.current_menu == config.STATS:
            config.current_menu = stats_page.show_stats_screen(screen)  

