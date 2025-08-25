import sys
import pygame
import random

def close():
    pygame.quit()
    sys.exit()

def draw_background(surf):
    surf.fill((0x49, 0x5e, 0x29))

def load_image(path, scale=1):
    image = pygame.image.load(path).convert_alpha()
    return pygame.transform.scale(image, (image.get_width() // 5 * scale, image.get_height() // 5 * scale))

def card_pos(total, i):
    card_width = 38
    width = 320
    total_width = (total + 1) * card_width / 2
    start = (width - total_width) / 2
    return start + (card_width / 2) * i

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
            self.cards.append(Card(i + 1, card_pos(card_count, i)))
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
                    c.pos = [card_pos(len(self.cards), j), c.pos[1]]
                if not len(self.cards):
                    return choosen_card
                self.selected = self.selected % len(self.cards)
            else:
                i += 1
        return choosen_card

class Opponent:
    def __init__(self):
        self.deck = range(1, 14)

    def choose_card(self, card):
        value = random.choice(list(self.deck))
        self.deck = [c for c in self.deck if c != value]
        return value

class Scores:
    def __init__(self):
        self.score = 0
        self.opp_score = 0

class Duel:
    def __init__(self, card, opp_card):
        self.c = card
        self.oc = opp_card
        self.card = load_image(f'cards/{str(card)}-P.png', scale=2)
        self.opp_card = load_image(f'cards/{str(opp_card)}-D.png', scale=2)
        self.prize = 69
        self.frame = 0

        self.y_pos = 36

    def result(self, scores):
        if self.c != self.oc:
            if self.c > self.oc:
                scores.score += self.prize
            else:
                scores.opp_score += self.prize
            return True
        return False

    def update(self):
        if self.frame > 60:
            return True

        self.frame += 1
        return False

    def render(self, surf):
        surf.blit(self.card, (50, self.y_pos))
        surf.blit(self.opp_card, (194, self.y_pos))

class Game:
    def __init__(self):
        pygame.init()

        self.screen = pygame.display.set_mode((1280, 720))
        self.display = pygame.surface.Surface((320, 180))
        self.clock = pygame.time.Clock()

        self.scores = Scores()
        self.deck = Deck()
        self.opponent = Opponent()
        self.choosen_card = None

        self.duel = None

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    close()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RIGHT:
                        self.deck.change_selected(1)
                    if event.key == pygame.K_LEFT:
                        self.deck.change_selected(-1)
                    if event.key == pygame.K_RETURN:
                        self.deck.select()
        
            draw_background(self.display)

            if self.choosen_card:
                # Render duel
                if self.duel.update():
                    self.choosen_card = None
                self.duel.render(self.display)
            else:
                # Render deck + UI
                self.choosen_card = self.deck.render(self.display)
                if self.choosen_card:
                    self.duel = Duel(self.choosen_card, self.opponent.choose_card(self.choosen_card))
                    if self.duel.result(self.scores):
                        print(self.scores.score, self.scores.opp_score)
                    else:
                        print("tie!")

            self.screen.blit(pygame.transform.scale(self.display, self.screen.get_size()), (0, 0))
            pygame.display.update()
            self.clock.tick(60)

Game().run()

