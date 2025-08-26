import random
import pygame

from scripts.utils import load_image, spread_pos


class Opponent:
    def __init__(self):
        self.deck = range(1, 14)
        self.mode = 'inc'

    def choose_card(self, card):
        if self.mode == 'rand':
            value = random.choice(list(self.deck))
        elif self.mode == 'inc':
            value = self.deck[0]
        self.deck = [c for c in self.deck if c != value]
        return value
    
class Biscuits:
    def __init__(self):
        self.biscuits = list(range(1, 14))
        print(self.biscuits)
        self.image = load_image('biscuit.png', scale=20)
        self.shadow = self.image.copy()
        self.shadow.fill((0, 0, 0, 70), special_flags=pygame.BLEND_RGBA_MULT)
        self.value = 0
        self.pos = []
        self.frame = 0


    def randomize_biscuits(self):
        value = random.choice(self.biscuits)
        self.value = value
        self.pos = [(spread_pos(value, i), random.randint(1, 5) + 50) for i in range(value)]
        self.frame = 0
        self.biscuits = [b for b in self.biscuits if b != value]
        return value
    
    # def update(self):
    #     self.fra
    
    def render(self, surf):
        for pos in self.pos:
            surf.blit(self.shadow, (pos[0] - 3, pos[1] + 3))
            surf.blit(self.image, pos)

class Scores:
    def __init__(self, font):
        self.score = 0
        self.opp_score = 0
        self.font = font

    def render(self, surf):
        text = self.font.render(str(self.score), False, (0, 0, 0))
        opp_text = self.font.render(str(self.opp_score), False, (0, 0, 0))
        rect = opp_text.get_rect()
        rect.right = 308
        surf.blit(text, (12, 0))
        surf.blit(opp_text, rect)