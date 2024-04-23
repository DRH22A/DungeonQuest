# main.py
import mysql.connector
import pygame
from pygame.locals import *
import multiprocessing
from colorama import Fore, Back, Style
import prettytable

import config
from dungeon_builder import build_dungeon
from dungeon_generator import generate_dungeon
import time

def generate_dungeon_wrapper(level_seed):
    level, seed = level_seed
    print(f"Process starting for seed: {seed}, level: {level}")
    start_time = time.perf_counter()
    
    if level <= 10:
        complexity = 0.1 + (0.9 * ((level - 1) / 9) ** 2)  
    else:
        complexity = 1.0  
    result = generate_dungeon(seed=seed, complexity=complexity)
    end_time = time.perf_counter()
    duration = end_time - start_time
    print(f"Process finished for seed: {seed}, Level: {level}, Duration: {duration:.5f} seconds")
    return result


def show_game_screen(screen):
    width, height = config.WIDTH, config.HEIGHT
    pygame.display.set_caption("Dungeon Quest")
    pygame.key.set_repeat(1, 1)

    win_music = pygame.mixer.Sound("resources/win_music.wav")
    win_music_played = False

    transition_sound = pygame.mixer.Sound("resources/transition_sound.wav")

    player_size = config.VISUAL_TILE_SIZE
    collision_size = player_size

    player_x = round((width // 2) / player_size) * player_size
    player_y = round((height // 2) / player_size) * player_size

    if config.player_x and config.player_y:
        player_x = config.player_x
        player_y = config.player_y

    player_speed = player_size
    key_pressed = False
    player_rect = pygame.Rect(player_x, player_y, collision_size, collision_size) 

    # Load tileset
    level_font = pygame.font.Font("resources/PixelOperator8.ttf", 24)
    tileset = pygame.image.load("resources/tileset.png")
    tile_size = 16
    tiles = []
    for y in range(0, tileset.get_height(), tile_size):
        for x in range(0, tileset.get_width(), tile_size):
            tile = tileset.subsurface(x, y, tile_size, tile_size)
            tile = pygame.transform.scale(tile, (player_size, player_size))
            tiles.append(tile)

    config.TILE_SET = tiles

    player_name = pygame.font.Font("resources/PixelOperator8.ttf", 16).render(config.local_username, True, (255, 255, 255))

    with multiprocessing.Pool() as pool:
        if config.seed == 0:
            config.seed = int(time.time())

        seeds = [(n, config.seed + n) for n in range(1, 6)]
        levels_data = pool.map(generate_dungeon_wrapper, seeds)
        for n, data in enumerate(levels_data, 1):
            config.levels[f'LEVEL_{n}'] = data


    # Game loop
    colliders, exits = [], []
    
    while config.running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                config.running = False

            if event.type == pygame.KEYUP:
                key_pressed = False

            keys = pygame.key.get_pressed()
            old_position = player_rect.topleft

            if event.type == pygame.KEYDOWN and not key_pressed:
                if keys[pygame.K_LEFT] and player_rect.x > 0:
                    player_rect.move_ip(-player_speed, 0)
                if keys[pygame.K_RIGHT] and player_rect.x < width - player_size:
                    player_rect.move_ip(player_speed, 0)
                if keys[pygame.K_UP] and player_rect.y > 0:
                    player_rect.move_ip(0, -player_speed)
                if keys[pygame.K_DOWN] and player_rect.y < height - player_size:
                    player_rect.move_ip(0, player_speed)

                if keys[pygame.K_ESCAPE]:
                    config.running = False
                if keys[pygame.K_m] and config.admin:
                    print(Fore.YELLOW + "Dumping SQL users table!" + Style.RESET_ALL)

                    cursor = config.sql_connection.cursor()
                    try:
                        cursor.execute("SELECT * FROM users")
                        columns = [i[0] for i in cursor.description]

                        x = prettytable.PrettyTable(columns)
                        rows = cursor.fetchall()

                        for row in rows:
                            x.add_row(row)
                        
                        print(x)

                    except mysql.connector.Error as error:
                        print(Fore.RED + f"Error: {error}" + Style.RESET_ALL)
 
                if any(player_rect.colliderect(c) for c in colliders):
                    player_rect.topleft = old_position

                key_pressed = True

        player_x, player_y = player_rect.topleft

        screen.fill((0, 0, 0))

        if config.current_level == 0:
            screen, colliders, exits = build_dungeon(screen, config.SPAWN_MAP)
        elif config.current_level > 5:
            screen, colliders, exits = build_dungeon(screen, config.VICTORY_MAP)
        else:
            level_key = f'LEVEL_{config.current_level}'
            if level_key in config.levels:
                screen, colliders, exits = build_dungeon(screen, config.levels[level_key])
            else:
                screen, colliders, exits = build_dungeon(screen, generate_dungeon(config.SPAWN_MAP))


        #
        # MAIN GAME LOGIC START
        #

        for i, _ in enumerate(exits[0]):
            if exits and i < len(exits[0]) and player_rect.colliderect(exits[1][i]):
                if exits[0][i] == 'R':
                    player_x = round((width // 20) / player_size) * player_size
                    player_y = round((height // 20) / player_size) * player_size
                    config.current_level += 1
                    transition_sound.play()
                elif exits[0][i] == 'L':
                    player_x = round((width - (width // 10)) / player_size) * player_size
                    player_y = round((height - (height // 9)) / player_size) * player_size
                    config.current_level -= 1
                    transition_sound.play()
                elif exits[0][i] == 'U':
                    player_x = round((width // 2) / player_size) * player_size
                    player_y = round((height - (height // 9)) / player_size) * player_size
                else:
                    player_x = round((width // 2) / player_size) * player_size
                    player_y = round((height // 10) / player_size) * player_size

                player_rect = pygame.Rect(player_x, player_y, collision_size, collision_size)

                
        if config.current_level == 0:
            winner_text = pygame.font.Font("resources/PixelOperator8.ttf", 16).render("Embark on a dangerous joruney...", True, (255, 15, 15))
            delete_text = pygame.font.Font("resources/PixelOperator8.ttf", 11).render("Proceed through five dungeons to win the game!", True, (255, 255, 255))
            screen.blit(winner_text, ((width / 2) - (winner_text.get_width() / 2), height / 2 - 50))
            screen.blit(delete_text, ((width / 2) - (delete_text.get_width() / 2), (height / 2) - (delete_text.get_height()) - 10))

        if config.current_level > 5:
            screen, colliders, exits = build_dungeon(screen, config.VICTORY_MAP)

            winner_text = pygame.font.Font("resources/PixelOperator8.ttf", 16).render("YOU ARE A WINNER!", True, (255, 215, 0))
            delete_text = pygame.font.Font("resources/PixelOperator8.ttf", 11).render("Exit the game to play again!", True, (255, 255, 255))
            screen.blit(winner_text, ((width / 2) - (winner_text.get_width() / 2), height / 2 - 50))
            screen.blit(delete_text, ((width / 2) - (delete_text.get_width() / 2), (height / 2) - (delete_text.get_height()) - 10))

            if not win_music_played:
                win_music.play()
                win_music_played = True

            
        #
        # MAIN GAME LOGIC END
        #

        
        screen.blit(tiles[config.CHARACTER_TILE], (player_x, player_y))
        screen.blit(player_name, (player_x, player_y - 15))

        if 1 <= config.current_level <= 5:
            level_text = level_font.render(f"Level: {config.current_level}", True, (0, 0, 0))
            screen.blit(level_text, (10, 10))  

        pygame.display.flip()

    #
    # SAVE GAME
    #

    print(Fore.WHITE + "Saving game..." + Style.RESET_ALL)
    connection = config.sql_connection

    if connection is None:
        print(Fore.RED + "Error: Failed to establish connection to database" + Style.RESET_ALL)
    else:
        try:
            cursor = connection.cursor(dictionary=True)

            if config.current_level > 5 or config.current_level == 0:
                cursor.execute("""UPDATE users SET level = %s, x = %s, y = %s, seed = %s WHERE username = %s""",
                               (None, None, None, None, config.local_username))
            else:
                cursor.execute("""UPDATE users SET level = %s, x = %s, y = %s, seed = %s WHERE username = %s""",
                               (config.current_level, player_x, player_y, config.seed, config.local_username))

            connection.commit()
            print(Fore.GREEN + "Game Saved!" + Style.RESET_ALL)

        except mysql.connector.Error as error:
            print(Fore.RED + f"Error: {error}" + Style.RESET_ALL)

        finally:
            if connection.is_connected():
                connection.commit()
                config.sql_connection.close()

    print(Fore.BLUE + "Goodbye!" + Style.RESET_ALL)
    pygame.quit()
