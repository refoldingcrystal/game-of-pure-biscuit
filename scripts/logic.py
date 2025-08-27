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
        self.image = load_image('biscuit.png', scale=20)
        self.shadow = self.image.copy()
        self.shadow.fill((0, 0, 0, 70), special_flags=pygame.BLEND_RGBA_MULT)
        self.value = 0
        self.pos = []
        self.frame = 0


    def randomize_biscuits(self, old_biscuits):
        new_value = random.choice(self.biscuits)
        self.value = new_value + old_biscuits
        self.pos = []
        if self.value <= 13:
            for i in range(self.value):
                self.pos.append((spread_pos(self.value, i), random.randint(1, 5) + 55 - self.image.get_height() * 0.5))
        elif self.value <= 26:
            for r, spread in enumerate([self.value - self.value // 2, self.value // 2]):
                for i in range(spread):
                    self.pos.append((spread_pos(spread, i), random.randint(1, 5) + 55 - self.image.get_height() * 0.75 + r * 26))
        else:
            rows = (self.value - 1) // 13 + 1
            tmp = self.value
            for r in range(rows):
                if tmp > 13:
                    spread = 13
                    tmp -= 13
                else:
                    spread = tmp
                for i in range(spread):
                    self.pos.append((spread_pos(spread, i), random.randint(1, 5) + 10 + r * 26))
        self.frame = 0
        self.biscuits = [b for b in self.biscuits if b != new_value]
        return new_value
    
    def render(self, surf):
        for pos in self.pos:
            surf.blit(self.shadow, (pos[0] - 3, pos[1] + 3))
            surf.blit(self.image, pos)

class Scores:
    def __init__(self, font):
        self.score = 0
        self.r_score = 0
        self.opp_score = 0
        self.r_opp_score = 0
        self.font = font
        self.frame = 0

    def result(self):
        return self.score >= self.opp_score

    def update(self):
        if self.score != self.r_score:
            if self.frame % 10:
                self.r_score += 1
            self.frame += 1
        elif self.opp_score != self.r_opp_score:
            if self.frame % 10:
                self.r_opp_score += 1
            self.frame += 1

    def render(self, surf):
        self.update()
        text = self.font.render(str(self.r_score), False, (255, 255, 255))
        rect = text.get_rect()
        rect.left = 12
        opp_text = self.font.render(str(self.r_opp_score), False, (255, 255, 255))
        opp_rect = opp_text.get_rect()
        opp_rect.right = 308
        pygame.draw.rect(surf, (0x2d, 0x3b, 0x77), (rect.left - 6, rect.top + 7, rect.width + 10, rect.height - 12), border_radius=5)
        surf.blit(text, rect)
        pygame.draw.rect(surf, (0x77, 0x2d, 0x40), (opp_rect.left - 6, opp_rect.top + 7, opp_rect.width + 10, opp_rect.height - 12), border_radius=5)
        surf.blit(opp_text, opp_rect)