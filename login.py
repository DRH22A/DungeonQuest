import pygame
import sys
import sqlite3
import mysql.connector
import bcrypt
import os

from colorama import Fore, Back, Style

import config

class InputBox:

    def __init__(self, x, y, w, h, text=''):
        self.rect = pygame.Rect(x, y, w, h)
        self.color = pygame.Color('white')
        self.text = text
        self.font = pygame.font.Font("resources/PixelOperator8.ttf", 16)
        self.txt_surface = self.font.render(text, True, self.color)
        self.active = False
        self.cursor_visible = True 
        self.cursor_counter = 0
        self.color_active = pygame.Color('gray')
        self.color_passive = pygame.Color('white')

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.active = not self.active
            else:
                self.active = False
            self.color = self.color_active if self.active else self.color_passive
        if event.type == pygame.KEYDOWN:
            if self.active:
                if event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                elif len(self.text) < 12:
                    self.text += event.unicode
                self.txt_surface = self.font.render(self.text, True, self.color)

    def update(self):
        self.cursor_counter += 1
        if self.cursor_counter % 500 == 0:   
            self.cursor_visible = not self.cursor_visible 
        if not self.active:
            self.cursor_visible = False 

    def draw(self, screen):
        screen.blit(self.txt_surface, (self.rect.x+5, self.rect.y+5))
        if self.cursor_visible:
            pygame.draw.line(screen, self.color, (self.txt_surface.get_width()+5+self.rect.x, self.rect.y+5), 
                            (self.txt_surface.get_width()+5+self.rect.x, self.rect.y+self.rect.h-5))
        pygame.draw.rect(screen, self.color, self.rect, 2)


def draw_text(screen, text: str, pos: tuple):
    font = pygame.font.Font("resources/PixelOperator8.ttf", 16)
    txt_surface = font.render(text, True, pygame.Color('white'))
    screen.blit(txt_surface, pos)
    

def show_login_screen(screen):
    width, height = config.WIDTH, config.HEIGHT

    pygame.display.set_caption("DungeonQuest Login Screen")

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

                    connection = mysql.connector.connect(
                        host="cop4521-dungeonquest.c3gw2k8i8nc0.us-east-1.rds.amazonaws.com",
                        user="cop4521",
                        password="COP4521!",
                        database="dungeonquest"
                    )
                    cursor = connection.cursor(dictionary=True)

                    # create users table if it doesn't exist
                    cursor.execute("""CREATE TABLE IF NOT EXISTS users(
                                    id INTEGER PRIMARY KEY AUTO_INCREMENT,
                                    username VARCHAR(255) NOT NULL UNIQUE,
                                    password VARCHAR(255) NOT NULL,
                                    role VARCHAR(10) NOT NULL)""")

                    if sign_up_rect.collidepoint(event.pos):
                        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

                        try:
                            cursor.execute("""INSERT INTO users (username, password, role) VALUES (%s, %s, %s)""",
                                      (username, hashed_password, 'Admin' if is_admin else 'Player'))
                            print(Fore.GREEN + "Sign Up Successful")
                            if is_admin:
                                print(Fore.BLUE + "You have been signed up as an admin!")
                            print(Fore.GREEN + "You may now sign in to the game!" + Style.RESET_ALL)
                        except sqlite3.IntegrityError:
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
                            print(Fore.RED + "Invalid username or password" + Style.RESET_ALL)

                    connection.commit()
                    connection.close()

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
        
        screen.blit(sign_up_button, sign_up_rect.topleft)
        screen.blit(sign_in_button, sign_in_rect.topleft)
        
        pygame.display.flip()
