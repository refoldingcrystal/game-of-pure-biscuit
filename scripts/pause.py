import math
import pygame
from scripts.utils import load_image


class Pause:
    def __init__(self):
        self.sound = pygame.mixer.Sound('sfx/button.mp3')
        self.sound_mature = pygame.mixer.Sound('sfx/button-mature.mp3')
        self.selected = 0
        self.modes = ['resume', 'menu', 'quit']
        self.images = {}
        self.shadows = {}
        for name in self.modes:
            self.images[name] = load_image(f'paused-{name}.png', scale=5)
            self.shadows[name] = self.images[name].copy()
            self.shadows[name].fill((0, 0, 0, 50), special_flags=pygame.BLEND_RGBA_MULT)

        self.height = 17
        self.frame = 0

    def change_selected(self, movement):
        self.sound.play()
        self.selected = (self.selected + movement) % len(self.modes)

    def select(self):
        self.sound_mature.play()
        return self.modes[self.selected]

    def render(self, surf):
        surf.blit(self.shadows[self.modes[self.selected]], (60 + math.sin(self.frame/60) * 5, self.height + 5))
        surf.blit(self.images[self.modes[self.selected]], (60, self.height))
        self.frame += 1