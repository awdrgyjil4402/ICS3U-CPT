import pygame

import os

# Level legend
# 1 = wall
# 2 = level transition
# 7 = item
# 9 = homing enemy


level_base = [[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
              [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
              [1, 0, 9, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 9, 0, 1],
              [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
              [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
              [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
              [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
              [1, 0, 9, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 9, 0, 1],
              [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
              [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]]

def get_level_rects():
    level_rects = []
    for y in range(len(level_base)):
        for x in range(len(level_base[1])):
            if level_base[y][x] == 1:
                level_rects.append(pygame.Rect(x*64, y*64 + 80, 64, 64))
    return level_rects

def get_enemies():
    enemy_pos = []
    for y in range(len(level_base)):
        for x in range(len(level_base[1])):
            if level_base[y][x] == 9:
                enemy_pos.append([x, y])
    return enemy_pos

def get_items():
    item_pos = []
    for y in range(len(level_base)):
        for x in range(len(level_base[1])):
            if level_base[y][x] == 7:
                item_pos.append([x, y])
    return item_pos