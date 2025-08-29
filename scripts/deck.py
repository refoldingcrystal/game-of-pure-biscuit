import random
import pygame
from scripts.utils import load_image, spread_pos


class Card:
    def __init__(self, value, pos, gamble=False):
        self.swipe = pygame.mixer.Sound('sfx/swipe.mp3')
        self.value = value
        self.image = load_image(f'cards/{str(value + 1)}-P.png')
        self.back = load_image('cards/BACK.png')
        self.pos = [pos, 120 + self.image.get_height() * (value + 1) // 2]

    def update(self, selected=None, move=False):
        if self.pos[1] > 120:
            if self.pos[1] <= 125:
                self.swipe.play()
            self.pos[1] -= 5
        else:
            if selected:
                if move:
                    self.pos[1] -= 10
                    if self.pos[1] < -70:
                        return True
                else:
                    self.pos[1] = max(self.pos[1] - 3, 110)
            else:
                self.pos[1] = min(self.pos[1] + 3, 120)

    def render(self, surf, hide=False):
        surf.blit(self.back if hide else self.image, self.pos)

class Deck:
    def __init__(self, gamble=False):
        self.gamble = gamble
        self.swipe = pygame.mixer.Sound('sfx/swipe.mp3')
        self.cards = []
        card_count = 13
        self.values = list(range(1, 14))
        random.shuffle(self.values)
        for i in range(card_count):
            self.cards.append(Card(self.values[i] if self.gamble else i + 1, spread_pos(card_count, i), gamble))
        self.hidden = [random.random() < 1 / len(self.cards) * random.randint(1, 3) for _ in self.cards]
        self.selected = 6
        self.select_lock = False

    def change_selected(self, movement):
        if not self.select_lock:
            if len(self.cards) > 1:
                self.swipe.set_volume(0.7 + 0.3 * random.random())
                self.swipe.play()
                self.swipe.set_volume(1.0)
                self.selected = (self.selected + movement) % len(self.cards)

    def select(self):
        self.select_lock = True
        self.swipe.play()

    def render(self, surf):
        choosen_card = None
        for i, card in enumerate(self.cards):
            card.render(surf, self.hidden[i] if self.gamble else False)
        i = 0
        for card in self.cards.copy():
            kill = card.update(self.selected == i, self.select_lock)
            if kill:
                choosen_card = card.value
                self.cards.remove(card)
                if self.gamble:
                    random.shuffle(self.cards)
                for j, c in enumerate(self.cards):
                    c.pos = [spread_pos(len(self.cards), j), c.pos[1]]
                self.hidden = [random.random() < 1 / len(self.cards) * random.randint(1, 3) for _ in self.cards]
                if not len(self.cards):
                    return 60, choosen_card
                if self.selected >= len(self.cards):
                    self.selected -= 1
            else:
                i += 1
        if choosen_card:
            return 60, choosen_card    
        return 0, choosen_card