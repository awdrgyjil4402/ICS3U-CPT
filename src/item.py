import pygame, os

class Item():
    def __init__(self, x=0, y=0, name=''):
        base_dir = os.path.dirname(os.path.dirname(__file__))
        assets_dir = os.path.join(base_dir, "assets")
        self.image = pygame.image.load(os.path.join(assets_dir, "item.png")).convert_alpha()
        # rect
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        
        # name
        self.name = name
    
    def draw(self, screen):
        screen.blit(self.image, self.rect)
