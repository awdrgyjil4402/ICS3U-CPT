import pygame

class Text:
    def __init__(self, text, font, x, y):
        self.text = text
        self.x = x
        self.y = y
        self.font = font
        self.text_color = (0, 0, 0)

        self.text_surface = self.font.render(self.text, True, self.text_color)

        self.text_rect = self.text_surface.get_rect()
        self.text_rect.center = (self.x, self.y)

    def draw(self, screen):
        screen.blit(self.text_surface, self.text_rect)

class Button:
    def __init__(self, text, font, x, y, width, height):
        self.rect = pygame.Rect(0, 0, width, height)
        self.rect.center = (x, y)
        self.text = text
        self.font = font

        self.color = (200, 200, 200)
        self.hover_color = (170, 170, 170)
        self.text_color = (0, 0, 0)

        self.text_surface = self.font.render(self.text, True, self.text_color)
        self.text_rect = self.text_surface.get_rect(center=self.rect.center)

    def draw(self, screen):
        mouse_pos = pygame.mouse.get_pos()

        # hover effect
        color = self.hover_color if self.rect.collidepoint(mouse_pos) else self.color
        pygame.draw.rect(screen, color, self.rect)

        screen.blit(self.text_surface, self.text_rect)

    def is_clicked(self):
        mouse_pos = pygame.mouse.get_pos()
        mouse_pressed = pygame.mouse.get_pressed()[0]

        clicked = (
            self.rect.collidepoint(mouse_pos)
            and mouse_pressed
        )

        return clicked
