import pygame
import level
import os

class Player(pygame.sprite.Sprite):
    def __init__(self, x=640, y=360, speed=5):
        # frames
        super().__init__()
        base_dir = os.path.dirname(os.path.dirname(__file__))
        assets_dir = os.path.join(base_dir, "assets", "player")
        self.frames = [
            pygame.image.load(os.path.join(assets_dir, "frame1.png")),
            pygame.image.load(os.path.join(assets_dir, "frame2.png")),
        ]
        self.frames_down = [
            pygame.image.load(os.path.join(assets_dir, "frame3.png")),
            pygame.image.load(os.path.join(assets_dir, "frame4.png")),
        ]
        self.frames_right = [
            pygame.image.load(os.path.join(assets_dir, "frame5.png")),
            pygame.image.load(os.path.join(assets_dir, "frame6.png")),
        ]

        self.frames_left = [
            pygame.image.load(os.path.join(assets_dir, "frame8.png")),
            pygame.image.load(os.path.join(assets_dir, "frame7.png")),
        ]
        self.idle_image = pygame.image.load(os.path.join(assets_dir, "idle.png"))
        self.scale = 1
        self.frames = [self._scale_frame(frame) for frame in self.frames]
        self.frames_down = [self._scale_frame(frame) for frame in self.frames_down]
        self.frames_right = [self._scale_frame(frame) for frame in self.frames_right]
        self.frames_default = self.frames
        self.idle_image = self._scale_frame(self.idle_image)
        self.index = 0
        self.image = self.frames[self.index]
        self.orientation = 'down'
        self.attacking = False
        self.attack_ticker = 0

        # rect
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

        self.level_rects = level.get_level_rects()

        # time / delay
        self.last_frame_time = 0
        self.frame_delay_ms = 150
        self.image = self.frames[self.index]

        # velocity
        self.direction = pygame.Vector2(0, 0)
        self.speed = speed
        self.vel = pygame.Vector2(0, 0)

        # invulnerability
        self.invulnerability_time = 2000
        self.last_hit_time = -self.invulnerability_time

        # game
        self.max_hp = 5
        self.hp = 5
        self.coins = 0
        self.inventory = []

        # cosmetics
        self.tint = (255, 255, 255)

    def _scale_frame(self, frame):
        width = max(1, int(frame.get_width() * self.scale))
        height = max(1, int(frame.get_height() * self.scale))
        return pygame.transform.smoothscale(frame, (width, height))

    def collision_direction(self, target: pygame.Rect):
        '''
        uses min overlap method
        doesnt work for extreme speeds or extremely small hitboxes
        should work for game
        simplest implementation; i couldnt figure out swept AABB
        '''

        if not self.rect.colliderect(target):
            return None

        overlap_left   = self.rect.right - target.left
        overlap_right  = target.right - self.rect.left
        overlap_top    = self.rect.bottom - target.top
        overlap_bottom = target.bottom - self.rect.top

        overlaps = {
        "left": overlap_left,
        "right": overlap_right,
        "top": overlap_top,
        "bottom": overlap_bottom,
        }

        return min(overlaps, key=overlaps.get)

    def collide_wall(self, targets: list[pygame.Rect]):
        '''
        uses axis-separated collision
        not perfect but works and simple
        '''

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

    def collide_enemy(self, targets):
        now = pygame.time.get_ticks()

        for enemy in targets:
            enemy_rect = enemy.rect
            if not self.rect.colliderect(enemy_rect):
                continue

            if now - self.last_hit_time >= self.invulnerability_time and not self.attacking:
                self.last_hit_time = now

                knockback_direction = pygame.Vector2(self.rect.center) - pygame.Vector2(enemy_rect.center)
                if knockback_direction.length_squared() == 0:
                    knockback_direction = pygame.Vector2(1, 0)
                else:
                    knockback_direction = knockback_direction.normalize()

                knockback = knockback_direction * 25

                old_vel = self.vel.copy()

                '''
                axis-separated collisions
                '''
                self.vel = pygame.Vector2(knockback.x, 0)
                self.collide_wall(self.level_rects)
                self.vel = pygame.Vector2(0, knockback.y)
                self.collide_wall(self.level_rects)
                self.vel = old_vel

                return True


    def collide_item(self, items: list[pygame.Rect]):
        for item in items[:]:
            if self.rect.colliderect(item.rect):
                self.inventory.append(item.name)
                items.remove(item)
                if self.hp < self.max_hp:
                    self.hp += 1

    def equip_tint(self, color: tuple[int, int, int]):
        self.tint = color  
    
    def unequip_tint(self):
        self.tint = (255, 255, 255)

    def update(self):
        keys = pygame.key.get_pressed()
        self.direction = pygame.Vector2(keys[pygame.K_d] - keys[pygame.K_a],
                                        keys[pygame.K_s] - keys[pygame.K_w])
        moving = False
        if self.direction.length_squared() > 0:
            self.direction = self.direction.normalize()
            moving = True

        self.vel = self.direction * self.speed

        desired_frames = self.frames_default
        if keys[pygame.K_w]:
            self.orientation = 'up'
        if keys[pygame.K_s]:
            desired_frames = self.frames_down
            self.orientation = 'down'
        if keys[pygame.K_a]:
            desired_frames = self.frames_left
            self.orientation = 'left'
        if keys[pygame.K_d]:
            desired_frames = self.frames_right
            self.orientation = 'right'
        if keys[pygame.K_k]:
            self.attack_ticker += 1
            if self.attack_ticker < 10:
                self.attacking = True
            else:
                self.attacking = False
        else:
            self.attack_ticker = 0
            self.attacking = False
        print(self.hp, self.attacking)
        if self.frames is not desired_frames:
            self.frames = desired_frames
            self.index = 0

        if moving:
            now = pygame.time.get_ticks()
            if now - self.last_frame_time >= self.frame_delay_ms:
                self.index = (self.index + 1) % len(self.frames)
                self.image = self.frames[self.index]
                self.last_frame_time = now
        else:
            self.index = 0
            self.image = self.frames[self.index]
        if not moving:
            self.image = self.idle_image

    def draw(self, screen):
        tinted_image = self._apply_tint(self.image, self.tint)
        screen.blit(tinted_image, self.rect)

    def _apply_tint(self, image, tint):
        tinted_image = image.copy()
        tint_surface = pygame.Surface(tinted_image.get_size())
        tint_surface.fill(tint)
        tinted_image.blit(tint_surface, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)
        return tinted_image
