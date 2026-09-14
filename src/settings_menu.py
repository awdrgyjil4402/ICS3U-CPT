# pygame template

import pygame
import settings
import player_data


pygame.init()

pygame.mixer.init()

WIDTH = 640
HEIGHT = 480
SIZE = (WIDTH, HEIGHT)

screen = pygame.display.set_mode(SIZE)
clock = pygame.time.Clock()

# ---------------------------
# Initialize global variables

font_arial_25 = pygame.font.SysFont('Arial', 25)

game_settings = settings.load_settings()

player_settings = player_data.load_player()

last_click_time = pygame.time.get_ticks()

pygame.mixer.music.load('assets_bgm.ogg')

pygame.mixer.music.play(-1)

pygame.mixer.music.set_volume(game_settings['volume'])

# ---------------------------

running = True

while running:
    # EVENT HANDLING
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    mouse_pos = pygame.mouse.get_pos()

    current_time = pygame.time.get_ticks()
    
    if game_settings['theme'] == 'dark': 
        screen.fill((0, 0, 0))  # always the first drawing command
    elif game_settings['theme'] == 'light':
        screen.fill((255, 255, 255))
    

    settings_1 = font_arial_25.render('SETTINGS', True, (0, 0, 255))
    settings_2 = font_arial_25.render(f"Theme: {game_settings['theme']}", True, (0, 0, 255))
    settings_3 = font_arial_25.render(f"Volume: {game_settings['volume']}", True, (0, 0, 255))
    settings_4 = font_arial_25.render(f"Keybinds: {game_settings['keybinds']}", True, (0, 0, 255))
    settings_5 = font_arial_25.render('Exit', True, (0, 0, 255))
    
    vol_up = font_arial_25.render('+', True, (0, 0, 255))
    vol_down = font_arial_25.render('-', True, (0, 0, 255))

    set_1_width = settings_1.get_width()
    set_2_width = settings_2.get_width()
    set_3_width = settings_3.get_width()
    set_4_width = settings_4.get_width()
    set_5_width = settings_5.get_width()

    vol_up_width = vol_up.get_width()
    vol_down_width = vol_down.get_width()

    set_rect_1 = settings_1.get_rect(center=(WIDTH//2, HEIGHT//2 - 160))
    set_rect_2 = settings_2.get_rect(center=(WIDTH//2, HEIGHT//2 - 120))
    set_rect_3 = settings_3.get_rect(center=(WIDTH//2, HEIGHT//2 - 80))
    set_rect_4 = settings_4.get_rect(center=(WIDTH//2, HEIGHT//2 - 40))
    set_rect_5 = settings_5.get_rect(center=(WIDTH//2, HEIGHT//2))

    vol_up_rect = vol_up.get_rect(center=(450, HEIGHT//2 - 80))
    vol_down_rect = vol_down.get_rect(center=(425, HEIGHT//2 - 80))

    if set_rect_2.collidepoint(mouse_pos) and event.type == pygame.MOUSEBUTTONDOWN:
        if game_settings['theme'] == 'dark':
            game_settings['theme'] = 'light'
            settings.save_settings(game_settings)
            pygame.time.wait(15)
        elif game_settings['theme'] == 'light':
            game_settings['theme'] = 'dark'
            settings.save_settings(game_settings)
            pygame.time.wait(15)

    if vol_up_rect.collidepoint(mouse_pos) and event.type == pygame.MOUSEBUTTONDOWN:
        if game_settings['volume'] <= 99: 
            game_settings['volume'] += 1
            pygame.mixer.music.set_volume(game_settings['volume'])
            settings.save_settings(game_settings)
        else: 
            game_settings['volume'] += 0

    if vol_down_rect.collidepoint(mouse_pos) and event.type == pygame.MOUSEBUTTONDOWN:
        if game_settings['volume'] >= 1:
            game_settings['volume'] -= 1
            pygame.mixer.music.set_volume(game_settings['volume'])
            settings.save_settings(game_settings)
        else: 
            game_settings['volume'] += 0

    if set_rect_4.collidepoint(mouse_pos) and event.type == pygame.MOUSEBUTTONDOWN:
        if game_settings['keybinds'] == 'wasd':
            game_settings['keybinds'] = 'arrows'
            settings.save_settings(game_settings)
            pygame.time.wait(15)
        elif game_settings['keybinds'] == 'arrows':
            game_settings['keybinds'] = 'wasd'
            settings.save_settings(game_settings)
            pygame.time.wait(15)

    if set_rect_5.collidepoint(mouse_pos) and event.type == pygame.MOUSEBUTTONDOWN:
        settings.save_settings(game_settings)
        running = False 


    screen.blit(settings_1, set_rect_1)
    screen.blit(settings_2, set_rect_2)
    screen.blit(settings_3, set_rect_3)
    screen.blit(settings_4, set_rect_4)
    screen.blit(settings_5, set_rect_5)
    
    screen.blit(vol_up, vol_up_rect)
    screen.blit(vol_down, vol_down_rect)

    # Must be the last two lines
    # of the game loop
    pygame.display.flip()
    clock.tick(30)
    #---------------------------

