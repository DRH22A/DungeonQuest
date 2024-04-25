import pygame
from textbox import InputBox
import player_menu

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
    draw_text(screen, "Main Menu", BLACK, (button_rect.x + 50, button_rect.y + 15))
    return button_rect


def show_seeds_screen(screen):
    seed = ""
    main_menu_rect = main_menu_button(screen)

    if config.admin:
        input_box_seed = InputBox(WIDTH // 2 - 100, HEIGHT // 4, 200, 32)

    cursor = config.sql_connection.cursor(dictionary=False)
    cursor.execute('SELECT seed FROM dungeonquest.seeds')
    seeds = cursor.fetchone()

    seed_rects = []
    for seed in seeds:
        seed_rect = pygame.Rect(WIDTH // 2 - 50, HEIGHT // 3 + (10 * seeds.index(seed)), 200, 50)
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
                            cursor.execute("INSERT INTO seeds (seed) VALUES (%s)", (seed,))
                            config.sql_connection.commit()
                            print('test')

                    except Exception as e:
                        print(e)
                        print("Invalid seed!")

                    return config.SCREEN_PLAYER_MENU

                if [seed_rect for _ in seed_rects if seed_rect.collidepoint(event.pos)]:
                    config.seed = int(seeds[seed_rects.index(seed_rect)])
                    print("Set seed to", config.seed)
                    return config.SCREEN_PLAYER_MENU

            if config.admin:
                input_box_seed.handle_event(event)

        screen.fill((0, 0, 0))

        if config.admin:
            input_box_seed.update()
            input_box_seed.draw(screen)

        main_menu_rect = main_menu_button(screen)

        for seed_rect in seed_rects:
            pygame.draw.rect(screen, BLACK, seed_rect)
            draw_text(screen, seeds[seed_rects.index(seed_rect)], WHITE,
                      (WIDTH // 2 - 50, HEIGHT // 3 + (10 * seed_rects.index(seed_rect))))

        pygame.display.flip()
