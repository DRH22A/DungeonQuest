import pygame
import mysql.connector
from colorama import Fore, Style
from prettytable import prettytable

import config
from textbox import InputBox

# Set up the display
WIDTH, HEIGHT = config.WIDTH, config.HEIGHT
pygame.display.set_caption("Admin Menu")

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
    draw_text(screen, "Set User ID", BLACK, (button_rect.x + 50, button_rect.y + 15))
    return button_rect

def show_admin_menu(screen):
    user_id = None

    input_box_user_id = InputBox(WIDTH // 2 - 100, HEIGHT // 2 - 160, 200, 32)

    connection = config.sql_connection
    cursor = connection.cursor(dictionary=False)
    print(Fore.YELLOW + "Dumping SQL users table!" + Style.RESET_ALL)
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

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if main_menu_rect.collidepoint(event.pos):  
                    user_id = input_box_user_id.text
                    print(f"New User ID: {user_id}")
                    input_box_user_id.text = ""

                    try:
                        if user_id != "":
                            cursor = connection.cursor(dictionary=True)
                            cursor.execute("""SELECT username, level, x, y, seed FROM users WHERE id = %s""", (user_id,))
                            user = cursor.fetchone()
                            if user.get('username') and user.get('level') and user.get('x') and user.get('y') and user.get('seed'):
                                config.local_username = user.get('username')
                                config.current_level = int(user.get('level'))
                                config.player_x = int(user.get('x'))
                                config.player_y = int(user.get('y'))
                                config.seed = int(user.get('seed'))

                    except:
                        print("Invalid user ID")

                    return config.SCREEN_PLAYER_MENU
            
            input_box_user_id.handle_event(event)

        screen.fill((0, 0, 0))

        draw_text(screen, "Admin Menu", (255, 255, 255), (WIDTH // 2, HEIGHT // 2 - 200))

        input_box_user_id.update()
        input_box_user_id.draw(screen)

        main_menu_rect = main_menu_button(screen)

        pygame.display.flip()
