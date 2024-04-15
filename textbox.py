import pygame

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