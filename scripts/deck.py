from scripts.utils import load_image, spread_pos


class Card:
    def __init__(self, value, pos):
        self.value = value
        self.image = load_image(f'cards/{str(value)}-P.png')
        self.pos = [pos, 120]

    def update(self, selected=None, move=False):
        if selected:
            if move:
                self.pos[1] -= 10
                if self.pos[1] < -60:
                    return True
            else:
                self.pos[1] = max(self.pos[1] - 3, 100)
        else:
            self.pos[1] = min(self.pos[1] + 3, 120)

    def render(self, surf):
        surf.blit(self.image, self.pos)

class Deck:
    def __init__(self):
        self.cards = []
        card_count = 13
        for i in range(card_count):
            self.cards.append(Card(i + 1, spread_pos(card_count, i)))
        self.selected = 0
        self.select_lock = False

    def change_selected(self, movement):
        if not self.select_lock:
            self.selected = (self.selected + movement) % len(self.cards)

    def select(self):
        self.select_lock = True

    def render(self, surf):
        choosen_card = None
        i = 0
        for card in self.cards.copy():
            kill = card.update(self.selected == i, self.select_lock)
            card.render(surf)
            if kill:
                choosen_card = card.value
                self.select_lock = False
                self.cards.remove(card)
                for j, c in enumerate(self.cards):
                    c.pos = [spread_pos(len(self.cards), j), c.pos[1]]
                if not len(self.cards):
                    return 0, choosen_card
                if self.selected >= len(self.cards):
                    self.selected -= 1
            else:
                i += 1
        if choosen_card:
            return 0, choosen_card    
        return 0, choosen_card