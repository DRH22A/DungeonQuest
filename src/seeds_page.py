import pygame
from textbox import InputBox

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
    button_rect = pygame.Rect((WIDTH - 200) // 2, HEIGHT - 100, 200, 50)
    pygame.draw.rect(screen, GRAY, button_rect)
    draw_text(screen, "Enter", BLACK, (button_rect.x + 50, button_rect.y + 15))
    return button_rect

def show_seeds_screen(screen):
    seed = ""
    main_menu_rect = main_menu_button(screen)

    if config.admin:
        input_box_seed = InputBox(WIDTH // 2 - 100, HEIGHT // 4, 200, 32)

    seeds = [] # todo: set me to seeds from db

    seed_rects = []
    for seed in seeds:
        seed_rect = pygame.Rect(WIDTH // 2, HEIGHT // 3 + (10 * seeds.index(seed)), 200, 50)
        pygame.draw.rect(screen, BLACK, seed_rect)
        draw_text(screen, seed, WHITE, (WIDTH // 2, HEIGHT // 2))
        seed_rects.append(seed_rect)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                if main_menu_rect.collidepoint(event.pos):  
                    seed = input_box_seed.text
                    print(f"Set new seed: {seed}")
                    input_box_seed.text = ""

                    try:
                        if seed != "":
                            cursor = config.sql_connection.cursor(dictionary=True)
                            #cursor.execute("""SELECT username, level, x, y, seed FROM users WHERE id = %s""", (user_id,))
                            #user = cursor.fetchone()
                            #if user.get('username') and user.get('level') and user.get('x') and user.get('y') and user.get('seed'):
                            #    config.local_username = user.get('username')
                            #    config.current_level = int(user.get('level'))
                            #    config.player_x = int(user.get('x'))
                            #    config.player_y = int(user.get('y'))
                            #    config.seed = int(user.get('seed'))
                        
                    except:
                        print("Invalid seed!")

                if [seed_rect for seed_rect in seed_rects if seed_rect.collidepoint(event.pos)]:
                    config.seed = seeds[seed_rects.index(seed_rect)]
                    return config.SCREEN_PLAYER_MENU  
 
            input_box_seed.handle_event(event)

        screen.fill((0, 0, 0))

        if config.admin:
            input_box_seed.update()
            input_box_seed.draw(screen)


        main_menu_rect = main_menu_button(screen)

        pygame.display.flip()
