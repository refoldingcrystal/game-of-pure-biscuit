import math
import sys
import pygame

def spread_pos(total, i, type='card'):
    width = 320
    if type == 'card':
        obj_width = 38
    elif type == 'biscuit':
        obj_width = 64
    total_width = (total + 1) * obj_width / 2
    start = (width - total_width) / 2
    return start + (obj_width / 2) * i

def close():
    pygame.quit()
    sys.exit()

def load_image(path, scale=1):
    image = pygame.image.load(path).convert_alpha()
    return pygame.transform.scale(image, (image.get_width() // 5 * scale, image.get_height() // 5 * scale))

class Title:
    def __init__(self, height=17):
        self.image = load_image('title.png', scale=5)
        self.images = {}
        self.shadows = {}
        for name in ['title', 'win', 'lose']:
            self.images[name] = load_image(f'{name}.png', scale=5)
            self.shadows[name] = self.images[name].copy()
            self.shadows[name].fill((0, 0, 0, 70), special_flags=pygame.BLEND_RGBA_MULT)

        self.shadow = self.image.copy()
        self.shadow.fill((0, 0, 0, 70), special_flags=pygame.BLEND_RGBA_MULT)

        self.biscuit = load_image('biscuit.png', scale=20)
        self.biscuit_shadow = self.biscuit.copy()
        self.biscuit_shadow.fill((0, 0, 0, 70), special_flags=pygame.BLEND_RGBA_MULT)

        self.height = height
        self.frame = 0
    
    def render(self, surf, name='title'):
        surf.blit(self.shadows[name], (60 + math.sin(self.frame/60) * 5, self.height + 5))
        surf.blit(self.images[name], (60, self.height))
        # surf.blit(self.shadow, (60 + math.sin(self.frame/60) * 5, self.height + 5))
        # surf.blit(self.image, (60, self.height))

        surf.blit(self.biscuit_shadow, (20 + math.sin(self.frame/60) * 5, self.height + 50))
        surf.blit(self.biscuit, (20, self.height + 45))
        surf.blit(self.biscuit_shadow, (300 - self.biscuit_shadow.get_width() + math.sin(self.frame/60) * 5, self.height + 50))
        surf.blit(self.biscuit, (300 - self.biscuit.get_width(), self.height + 45))


        self.frame += 1

class Background:
    def __init__(self):
        self.c1 = (0x59, 0x85, 0x32)
        self.c2 = (0x4f, 0x77, 0x2d)
        self.tile_size = 10

    def render(self, surf):
        surf.fill(self.c1)
        for x in range(320 // self.tile_size + 1):
            for y in range(180 // self.tile_size + 1):
                if (x + y) % 2:
                    rect = (x * self.tile_size, y * self.tile_size,
                            self.tile_size, self.tile_size)
                    pygame.draw.rect(surf, self.c2, rect)