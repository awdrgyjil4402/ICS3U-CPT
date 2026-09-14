import pygame

import button, enemy, item, level, player_data, player, settings, random

pygame.init()

WIDTH = 1280
HEIGHT = 720
SIZE = (WIDTH, HEIGHT)

screen = pygame.display.set_mode(SIZE)
clock = pygame.time.Clock()

# ---------------------------
# Initialize global variables

game_settings = settings.load_settings()
player_settings = player_data.load_player()
last_click_time = pygame.time.get_ticks()

spawn_ticker = 0

h_up_ticker = 0

difficulty_ticker = 1

player = player.Player(x=608, y=360)
level_rects = level.get_level_rects()
enemies = []
items = []
for item_pos in level.get_items():
    items.append(item.Item(x=(item_pos[0]*64), y=(item_pos[1]*64)+80))

verdana_25 = pygame.font.SysFont('verdana', 25, True)

current_screen = 'menu'

menu_text = button.Text('DUNGEONS AND MORE DUNGEONS', verdana_25, WIDTH // 2, 300)
dead_text = button.Text('YOU DIED', verdana_25, WIDTH // 2, 200)
settings_text = button.Text('SETTINGS', verdana_25, WIDTH // 2, 200)

hp_boost_text = button.Text('MAX HP +1', verdana_25, WIDTH // 2 - 450, 300)
red_skin_text = button.Text('RED ARMOUR', verdana_25, WIDTH // 2 - 150, 300)
blue_skin_text = button.Text('BLUE ARMOUR', verdana_25, WIDTH // 2 + 150, 300)
gold_skin_text = button.Text('GOLD ARMOUR', verdana_25, WIDTH // 2 + 450, 300)
hp_boost_price = button.Text('50 COINS', verdana_25, WIDTH // 2 - 450, 350)
red_price_text = button.Text('20 COINS', verdana_25, WIDTH // 2 - 150, 350)
blue_price_text = button.Text('50 COINS', verdana_25, WIDTH // 2 + 150, 350)
gold_price_text = button.Text('100 COINS', verdana_25, WIDTH // 2 + 450, 350)

start_button = button.Button('START', verdana_25, WIDTH // 2, 450, 200, 100)
shop_button = button.Button('SHOP', verdana_25, WIDTH // 2, 450, 200, 100)
pause_button = button.Button('PAUSE', verdana_25, WIDTH // 2, 300, 200, 100)
settings_button = button.Button('SETTINGS', verdana_25, WIDTH // 2, 600, 200, 100)
hp_purchase_button = button.Button('PURCHASE', verdana_25, WIDTH // 2 - 450, 500, 200, 100)
red_purchase_button = button.Button('PURCHASE', verdana_25, WIDTH // 2 - 150, 500, 200, 100)
blue_purchase_button = button.Button('PURCHASE', verdana_25, WIDTH // 2 + 150, 500, 200, 100)
gold_purchase_button = button.Button('PURCHASE', verdana_25, WIDTH // 2 + 450, 500, 200, 100)
exit_button = button.Button('EXIT', verdana_25, 1200, 640, 80, 80)

try_again_button = button.Button('TRY AGAIN', verdana_25, WIDTH //2, 300, 200, 100)

light_theme_button = button.Button('LIGHT', verdana_25, WIDTH // 2 - 125, 300, 200, 100)
dark_theme_button = button.Button('DARK', verdana_25, WIDTH // 2 + 125, 300, 200, 100)
wasd_keybinds_button = button.Button('WASD', verdana_25, WIDTH // 2 - 125, 450, 200, 100)
arrow_keybinds_button = button.Button('ARROWS', verdana_25, WIDTH // 2 + 125, 450, 200, 100)

wall = pygame.transform.scale_by(pygame.image.load("../assets/wall.png").convert_alpha(), 2)

# ---------------------------

running = True
while running:
    if current_screen == 'menu':
        # EVENT HANDLING
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif start_button.is_clicked():
                current_screen = 'game loop'
            elif settings_button.is_clicked():
                current_screen = 'menu/settings'

        # GAME STATE UPDATES

        # DRAWING
        if game_settings['theme'] == 'light':
            screen.fill((255, 255, 255))
        elif game_settings['theme'] == 'dark':
            screen.fill((0, 0, 0))
        
        menu_text.draw(screen)
        start_button.draw(screen)
        settings_button.draw(screen)

    elif current_screen == 'game loop':
        # EVENT HANDLING
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    current_screen = "pause"
    
        # GAME STATE UPDATES
        if spawn_ticker >= 120/difficulty_ticker:
            enemy_pos = random.choice(level.get_enemies())
            enemies.append(enemy.Enemy(x=(enemy_pos[0]*64), y=(enemy_pos[1]*64)+80))
            spawn_ticker = 0
    
        spawn_ticker += 1

        if h_up_ticker >= 120 and len(items) < 2:
            items.append(item.Item(random.randint(64, 1100), random.randint(144, 600)))
            h_up_ticker = 0

        h_up_ticker += 1
    
        player.update()
        for e in enemies:
            e.update(player)
    
        player.collide_wall(level_rects)
        for e in enemies:
            e.collide_wall(level_rects)
        
        if player.collide_enemy(enemies) and not player.attacking:
            player.hp -= 1
        if not player.collide_enemy(enemies) and player.attacking:
            for e in enemies:
                if player.rect.colliderect(e.rect):
                    enemies.remove(e)
                    player.coins += 5
                    difficulty_ticker += 0.2
        
        player.collide_item(items)

        if player.hp == 0:
            current_screen = 'dead'

    
        # DRAWING
        screen.fill((97, 36, 0))  # always the first drawing command

        pygame.draw.rect(screen, (255, 255, 255), (0, 0, 1280, 100))
    
        player.draw(screen)

        screen.blit(verdana_25.render('COINS: '+str(player.coins), True, (0, 0, 0)), (1000, 20))
        screen.blit(verdana_25.render('HP: '+str(player.hp)+'/'+str(player.max_hp), True, (0, 0, 0)), (20, 20))
    
        for e in enemies:
            e.draw(screen)
    
        for i in items:
            i.draw(screen)
    
        for rect in level_rects:
            screen.blit(wall, rect.topleft)

    elif current_screen == 'pause':
        # EVENT HANDLING
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    current_screen = "game loop"
            elif pause_button.is_clicked():
                current_screen = 'game loop'
            elif shop_button.is_clicked():
                current_screen = 'shop'
            elif settings_button.is_clicked():
                current_screen = 'game/settings'

        # GAME STATE UPDATES

        # DRAWING
        screen.fill((97, 36, 0))  # always the first drawing command

        pygame.draw.rect(screen, (255, 255, 255), (0, 0, 1280, 100))
    
        player.draw(screen)

        screen.blit(verdana_25.render('COINS: '+str(player.coins), True, (0, 0, 0)), (1000, 20))
        screen.blit(verdana_25.render('HP: '+str(player.hp)+'/'+str(player.max_hp), True, (0, 0, 0)), (20, 20))
    
        for e in enemies:
            e.draw(screen)
    
        for i in items:
            i.draw(screen)
    
        for rect in level_rects:
            screen.blit(wall, rect)

        pause_button.draw(screen)
        settings_button.draw(screen)
        exit_button.draw(screen)
        shop_button.draw(screen)

    elif current_screen == 'dead':
        # EVENT HANDLING
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif try_again_button.is_clicked():
                current_screen = 'game loop'
                player.hp = player.max_hp
                enemies.clear()
                items.clear()
                player.coins = 0
                difficulty_ticker = 1
                spawn_ticker = 0
                hp_up_ticker = 0
                player.rect.topleft = (608, 360)
            elif shop_button.is_clicked():
                current_screen = 'shop'
            elif settings_button.is_clicked():
                current_screen = 'game/settings'

        # GAME STATE UPDATES

        # DRAWING
        screen.fill((97, 36, 0))  # always the first drawing command
    
        pygame.draw.rect(screen, (255, 255, 255), (0, 0, 1280, 100))

        player.draw(screen)
    
        for e in enemies:
            e.draw(screen)
    
        for i in items:
            i.draw(screen)
    
        for rect in level_rects:
            screen.blit(wall, rect)

        try_again_button.draw(screen)
        settings_button.draw(screen)
        exit_button.draw(screen)
        shop_button.draw(screen)
    
    elif current_screen == 'menu/settings':
        # EVENT HANDLING
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    current_screen = "menu"
            elif light_theme_button.is_clicked():
                game_settings['theme'] = 'light'
                settings.save_settings(game_settings)
            elif dark_theme_button.is_clicked():
                game_settings['theme'] = 'dark'
                settings.save_settings(game_settings)
            elif wasd_keybinds_button.is_clicked():
                game_settings['keybinds'] = 'wasd'
                settings.save_settings(game_settings)
            elif arrow_keybinds_button.is_clicked():
                game_settings['keybinds'] = 'arrows'
                settings.save_settings(game_settings)
            elif exit_button.is_clicked():
                current_screen = "menu"

        # GAME STATE UPDATES

        # DRAWING
        if game_settings['theme'] == 'light':
            screen.fill((255, 255, 255))
        elif game_settings['theme'] == 'dark':
            screen.fill((0, 0, 0))

        settings_text.draw(screen)
        light_theme_button.draw(screen)
        dark_theme_button.draw(screen)
        wasd_keybinds_button.draw(screen)
        arrow_keybinds_button.draw(screen)
        exit_button.draw(screen)

    elif current_screen == 'game/settings':
        # EVENT HANDLING
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    current_screen = "game loop"
            elif light_theme_button.is_clicked():
                game_settings['theme'] = 'light'
                settings.save_settings(game_settings)
            elif dark_theme_button.is_clicked():
                game_settings['theme'] = 'dark'
                settings.save_settings(game_settings)
            elif wasd_keybinds_button.is_clicked():
                game_settings['keybinds'] = 'wasd'
                settings.save_settings(game_settings)
            elif arrow_keybinds_button.is_clicked():
                game_settings['keybinds'] = 'arrows'
                settings.save_settings(game_settings)
            elif exit_button.is_clicked():
                current_screen = "game loop"

        # GAME STATE UPDATES

        # DRAWING
        if game_settings['theme'] == 'light':
            screen.fill((255, 255, 255))
        elif game_settings['theme'] == 'dark':
            screen.fill((0, 0, 0))

        settings_text.draw(screen)
        light_theme_button.draw(screen)
        dark_theme_button.draw(screen)
        wasd_keybinds_button.draw(screen)
        arrow_keybinds_button.draw(screen)
        exit_button.draw(screen)

    elif current_screen == 'shop':
        # EVENT HANDLING
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    current_screen = "game loop"
            elif hp_purchase_button.is_clicked() and player.coins >= 50:
                player.coins -= 50
                player.max_hp += 1
            elif red_purchase_button.is_clicked() and player.coins >= 20:
                player.coins -= 20
                player.equip_tint((255, 0, 0))
            elif blue_purchase_button.is_clicked() and player.coins >= 50:
                player.coins -= 50
                player.equip_tint((0, 0, 255))
            elif gold_purchase_button.is_clicked() and player.coins >= 100:
                player.coins -= 100
                player.equip_tint((255, 255, 0))
            elif exit_button.is_clicked():
                current_screen = "game loop"

        # GAME STATE UPDATES

        # DRAWING
        if game_settings['theme'] == 'light':
            screen.fill((255, 255, 255))
        elif game_settings['theme'] == 'dark':
            screen.fill((0, 0, 0))

        screen.blit(verdana_25.render('COINS: '+str(player.coins), True, (0, 0, 0)), (1000, 20))
        
        pygame.draw.circle(screen, (255, 192, 203), (WIDTH // 2 - 450, 200), 75)
        pygame.draw.circle(screen, (255, 0, 0), (WIDTH // 2 - 150, 200), 75)
        pygame.draw.circle(screen, (0, 0, 255), (WIDTH // 2 + 150, 200), 75)
        pygame.draw.circle(screen, (255, 255, 0), (WIDTH // 2 + 450, 200), 75)
        hp_boost_text.draw(screen)
        red_skin_text.draw(screen)
        blue_skin_text.draw(screen)
        gold_skin_text.draw(screen)
        hp_boost_price.draw(screen)
        red_price_text.draw(screen)
        blue_price_text.draw(screen)
        gold_price_text.draw(screen)
        hp_purchase_button.draw(screen)
        red_purchase_button.draw(screen)
        blue_purchase_button.draw(screen)
        gold_purchase_button.draw(screen)
        exit_button.draw(screen)

    # Must be the last two lines
    # of the game loop
    pygame.display.flip()
    clock.tick(60)
    #---------------------------


pygame.quit()
