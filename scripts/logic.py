import random


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
        self.biscuits = range(1, 14)

    def randomize_biscuits(self):
        value = random.choice(list(self.biscuits))
        self.biscuits = [b for b in self.biscuits if b != value]
        return value

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