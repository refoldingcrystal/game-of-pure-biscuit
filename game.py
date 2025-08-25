import sys
import pygame

def close():
    pygame.quit()
    sys.exit()

def draw_background(surf):
    surf.fill((0x49, 0x5e, 0x29))

def load_image(path):
    image = pygame.image.load(path).convert_alpha()
    return pygame.transform.scale(image, (image.get_width() // 5, image.get_height() // 5))

def card_pos(total, i):
    card_width = 38
    width = 320
    total_width = (total + 1) * card_width / 2
    start = (width - total_width) / 2
    return start + (card_width / 2) * i

class Card:
    def __init__(self, value, pos):
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
        i = 0
        for card in self.cards.copy():
            kill = card.update(self.selected == i, self.select_lock)
            card.render(surf)
            if kill:
                self.select_lock = False
                self.cards.remove(card)
                for j, c in enumerate(self.cards):
                    c.pos = [card_pos(len(self.cards), j), c.pos[1]]
                self.selected = self.selected % len(self.cards)
            else:
                i += 1

class Game:
    def __init__(self):
        pygame.init()

        self.screen = pygame.display.set_mode((1280, 720))
        self.display = pygame.surface.Surface((320, 180))
        self.clock = pygame.time.Clock()

        self.deck = Deck()

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

            self.deck.render(self.display)

            self.screen.blit(pygame.transform.scale(self.display, self.screen.get_size()), (0, 0))
            pygame.display.update()
            self.clock.tick(60)

Game().run()

