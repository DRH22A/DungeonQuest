import pygame
import sys
import sqlite3
import bcrypt
import os

import config

class InputBox:

    def __init__(self, x, y, w, h, text=''):
        self.rect = pygame.Rect(x, y, w, h)
        self.color = pygame.Color('dodgerblue2')
        self.text = text
        self.font = pygame.font.Font(None, 32)
        self.txt_surface = self.font.render(text, True, self.color)
        self.active = False
        self.cursor_visible = True 
        self.cursor_counter = 0
        self.color_active = pygame.Color('dodgerblue4')
        self.color_passive = pygame.Color('dodgerblue2')

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
                else:
                    self.text += event.unicode
                # Re-render the text.
                self.txt_surface = self.font.render(self.text, True, self.color)

    def update(self):
        self.cursor_counter += 1
        if self.cursor_counter % 30 == 0:   
            self.cursor_visible = not self.cursor_visible 
        if not self.active:
            self.cursor_visible = False 

    def draw(self, screen):
        # Blit the text.
        screen.blit(self.txt_surface, (self.rect.x+5, self.rect.y+5))
        if self.cursor_visible:
            pygame.draw.line(screen, self.color, (self.txt_surface.get_width()+5+self.rect.x, self.rect.y+5), 
                            (self.txt_surface.get_width()+5+self.rect.x, self.rect.y+self.rect.h-5))
        pygame.draw.rect(screen, self.color, self.rect, 2)


def draw_text(screen, text: str, pos: tuple):
    font = pygame.font.Font(None, 32)
    txt_surface = font.render(text, True, pygame.Color('white'))
    screen.blit(txt_surface, pos)
    

def show_login_screen(screen):
    width, height = config.WIDTH, config.HEIGHT

    pygame.display.set_caption("DungeonQuest Login Screen")

    input_box_username = InputBox(width // 2, height // 2 - 160, 200, 32)
    input_box_password = InputBox(width // 2, height // 2 - 100, 200, 32)
    input_boxes = [input_box_username, input_box_password]
    is_admin_rect = pygame.Rect(width // 2, height // 2 - 40, 20, 20)
    is_admin = False

    sign_up_button = pygame.font.Font(None, 36).render("Sign Up", True, (255, 255, 255))
    sign_up_rect = sign_up_button.get_rect(center=(width // 2, height // 2))

    sign_in_button = pygame.font.Font(None, 36).render("Sign In", True, (255, 255, 255))
    sign_in_rect = sign_in_button.get_rect(center=(width // 2, height // 2 + 50))

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

                    conn = sqlite3.connect(os.path.join('instance', 'site.db'))
                    c = conn.cursor()

                    # create users table if it doesn't exist
                    c.execute("""CREATE TABLE IF NOT EXISTS users(
                                    id INTEGER PRIMARY KEY,
                                    username TEXT NOT NULL UNIQUE,
                                    password TEXT NOT NULL,
                                    role TEXT NOT NULL)""")

                    if sign_up_rect.collidepoint(event.pos):
                        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

                        try:
                            c.execute("""INSERT INTO users (username, password, role) VALUES (?, ?, ?)""",
                                      (username, hashed_password, 'Admin' if is_admin else 'Player'))
                            print("Sign Up Successful")
                        except sqlite3.IntegrityError:
                            print("Username already taken")

                    if sign_in_rect.collidepoint(event.pos):
                        c.execute("""SELECT * FROM users WHERE username = ?""", (username,))
                        user = c.fetchone()

                        if user and bcrypt.checkpw(password.encode('utf-8'), user[2]):
                            print("Sign In Successful")
                            config.local_username = username
                            config.local_password = user[2]

                            return config.SCREEN_GAME
                        else:
                            print("Invalid username or password")

                    conn.commit()
                    conn.close()

            for box in input_boxes:
                box.handle_event(event)

        screen.fill((0, 0, 0))
        for box in input_boxes:
            box.update()
            box.draw(screen)

        pygame.draw.rect(screen, (255, 255, 255), is_admin_rect, 2)
        if is_admin:
            pygame.draw.rect(screen, (0, 255, 0), is_admin_rect.inflate(-5, -5)) 

        draw_text(screen, "Admin", (width // 2 + 40, height // 2 - 50))
        
        screen.blit(sign_up_button, sign_up_rect.topleft)
        screen.blit(sign_in_button, sign_in_rect.topleft)
        
        pygame.display.flip()
