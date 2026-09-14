import pygame
import math, random, os

class Enemy:
    def __init__(self, x=0, y=0, speed=3):
        # frames
        base_dir = os.path.dirname(os.path.dirname(__file__))
        assets_dir = os.path.join(base_dir, "assets")
        self.image = pygame.transform.scale_by((pygame.image.load(os.path.join(assets_dir, "enemy.png")).convert_alpha()), 2)

        # rect
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

        # time
        self.last_move_time = pygame.time.get_ticks()

        # movement
        self.direction = pygame.Vector2(0, 0)
        self.speed = speed
        self.vel = pygame.Vector2(0, 0)


    def collide_wall(self, targets: list[pygame.Rect]):

        self.rect.x += int(self.vel.x)
        for target in targets:
            if self.rect.colliderect(target):
                if self.vel.x > 0:      # moving right
                    self.rect.right = target.left
                elif self.vel.x < 0:    # moving left
                    self.rect.left = target.right
                self.vel.x = 0

        self.rect.y += int(self.vel.y)
        for target in targets:
            if self.rect.colliderect(target):
                if self.vel.y > 0:      # moving down
                    self.rect.bottom = target.top
                elif self.vel.y < 0:    # moving up
                    self.rect.top = target.bottom
                self.vel.y = 0

    def update(self, player_obj):
        current_time = pygame.time.get_ticks()

        # Only update target direction every 2s
        if current_time - self.last_move_time > 2000:
            player_pos = pygame.Vector2(player_obj.rect.center)
            enemy_pos  = pygame.Vector2(self.rect.center)

            self.direction = player_pos - enemy_pos

            if self.direction.length_squared() > 0:
                self.direction = self.direction.normalize()

            self.last_move_time = current_time

        # velocity always based on normalized direction
        self.vel = self.direction * self.speed

    def draw(self, screen):
        screen.blit(self.image, self.rect)

class RandEnemy:
    def __init__(self, x=400, y=400, speed=5):
        # frames
        base_dir = os.path.dirname(os.path.dirname(__file__))
        assets_dir = os.path.join(base_dir, "assets")
        self.image = pygame.image.load(os.path.join(assets_dir, "enemy_temp.png")).convert_alpha()

        # rect
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

        # time
        self.last_move_time = pygame.time.get_ticks()

        # movement
        self.rand_direction = pygame.Vector2(0, 0)
        self.speed = speed
        self.vel = pygame.Vector2(0, 0)


    def collide_wall(self, targets: list[pygame.Rect]):

        self.rect.x += int(self.vel.x)
        for target in targets:
            if self.rect.colliderect(target):
                if self.vel.x > 0:      # moving right
                    self.rect.right = target.left
                elif self.vel.x < 0:    # moving left
                    self.rect.left = target.right
                self.vel.x = 0

        self.rect.y += int(self.vel.y)
        for target in targets:
            if self.rect.colliderect(target):
                if self.vel.y > 0:      # moving down
                    self.rect.bottom = target.top
                elif self.vel.y < 0:    # moving up
                    self.rect.top = target.bottom
                self.vel.y = 0

    def update(self):
        current_time = pygame.time.get_ticks()

        if current_time - self.last_move_time > 2000:
            rand_angle = random.random() * 2 * math.pi
            self.rand_direction = pygame.Vector2(math.cos(rand_angle), math.sin(rand_angle))

            if self.rand_direction.length_squared() > 0:
                self.rand_direction = self.rand_direction.normalize()
            
            self.last_move_time = current_time

        self.vel = self.rand_direction * self.speed

    def draw(self, screen):
        screen.blit(self.image, self.rect)
