import pygame
import sys
import mysql.connector
import bcrypt
import os

from colorama import Fore, Back, Style

import config
from textbox import InputBox

def draw_text(screen, text: str, pos: tuple):
    font = pygame.font.Font("resources/PixelOperator8.ttf", 16)
    txt_surface = font.render(text, True, pygame.Color('white'))
    screen.blit(txt_surface, pos)


def message_text(screen, text, color, pos):
    text_surface = pygame.font.Font("resources/PixelOperator8.ttf", 16).render(text, True, color)
    text_rect = text_surface.get_rect(center=pos)
    screen.blit(text_surface, text_rect.topleft)

def show_login_screen(screen):
    width, height = config.WIDTH, config.HEIGHT

    pygame.display.set_caption("DungeonQuest Login Screen")

    text = 'Enter your username and password to sign up or sign in'
    color = (255, 255, 255)
    pos = (width // 2, height - 750)

    input_box_username = InputBox(width // 2 - 100, height // 2 - 160, 200, 32)
    input_box_password = InputBox(width // 2 - 100, height // 2 - 100, 200, 32)
    input_boxes = [input_box_username, input_box_password]
    is_admin_rect = pygame.Rect(width // 2 - 100, height // 2 - 40, 20, 20)
    is_admin = False

    sign_up_button = pygame.font.Font("resources/PixelOperator8.ttf", 16).render("Sign Up", True, (255, 255, 255))
    sign_up_rect = sign_up_button.get_rect(center=(width // 2, height // 2 + 30))

    sign_in_button = pygame.font.Font("resources/PixelOperator8.ttf", 16).render("Sign In", True, (255, 255, 255))
    sign_in_rect = sign_in_button.get_rect(center=(width // 2, height // 2 + 80))

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            elif event.type == pygame.MOUSEBUTTONUP:
                if is_admin_rect.collidepoint(event.pos):
                    is_admin = not is_admin

                if sign_up_rect.collidepoint(event.pos) or sign_in_rect.collidepoint(event.pos):
                    username = input_box_username.text
                    password = input_box_password.text

                    if not os.path.exists('instance'):
                        os.makedirs('instance')

                    connection = config.sql_connection = mysql.connector.connect(
                        host="cop4521-dungeonquest.c3gw2k8i8nc0.us-east-1.rds.amazonaws.com",
                        user="cop4521",
                        password="COP4521!",
                        database="dungeonquest"
                    )
                    cursor = connection.cursor(dictionary=True)

                    if sign_up_rect.collidepoint(event.pos):
                        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

                        try:
                            cursor.execute("""INSERT INTO users (username, password, role) VALUES (%s, %s, %s)""",
                                      (username, hashed_password, 'Admin' if is_admin else 'Player'))
                            text = "Sign Up Successful"
                            print(Fore.GREEN + "Sign Up Successful")
                            if is_admin:
                                print(Fore.BLUE + "You have been signed up as an admin!")
                            print(Fore.GREEN + "You may now sign in to the game!" + Style.RESET_ALL)
                        except mysql.connector.errors.IntegrityError as e:
                            print(Fore.RED + "Username already taken!" + Style.RESET_ALL)

                    if sign_in_rect.collidepoint(event.pos):
                        cursor.execute("""SELECT username, password FROM users WHERE username = %s""", (username,))
                        user = cursor.fetchone()

                        if user and bcrypt.checkpw(password.encode('utf-8'), user.get('password').encode('utf-8')):
                            print(Fore.GREEN + "Sign In Successful" + Style.RESET_ALL)
                            config.local_username = username
                            config.local_password = user.get('password')

                            return config.SCREEN_GAME
                        else:
                            text = "Invalid username or password"
                            color = (255, 255, 255)
                            pos = (width // 2, height - 750)

                            print(Fore.RED + "Invalid username or password" + Style.RESET_ALL)

                    connection.commit()

            for box in input_boxes:
                box.handle_event(event)

        screen.fill((0, 0, 0))
        for box in input_boxes:
            box.update()
            box.draw(screen)

        pygame.draw.rect(screen, (255, 255, 255), is_admin_rect, 2)
        if is_admin:
            pygame.draw.rect(screen, (0, 255, 0), is_admin_rect.inflate(-5, -5)) 

        draw_text(screen, "Sign up as admin!", (width // 2 - 70, height // 2 - 38))
        message_text(screen, text, color, pos)

        screen.blit(sign_up_button, sign_up_rect.topleft)
        screen.blit(sign_in_button, sign_in_rect.topleft)
        # screen.blit(message, message_rect.topleft)

        
        pygame.display.flip()
