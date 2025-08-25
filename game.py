import math
import sys
import pygame
import random

def close():
    pygame.quit()
    sys.exit()

def draw_background(surf):
    surf.fill((0x59, 0x85, 0x32))
    tile_size = 10
    for x in range(320 // tile_size + 1):
        for y in range(180 // tile_size + 1):
            if (x + y) % 2:
                rect = (x * tile_size, y * tile_size, tile_size, tile_size)
                color = (0x4f, 0x77, 0x2d)
                pygame.draw.rect(surf, color, rect)

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
                self.selected = (self.selected - 1) % len(self.cards)
            else:
                i += 1
        return choosen_card

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
    def __init__(self):
        self.score = 0
        self.opp_score = 0
        self.font = pygame.font.Font("font/jersey.ttf", 40)

    def render(self, surf):
        text = self.font.render(str(self.score), False, (0, 0, 0))
        opp_text = self.font.render(str(self.opp_score), False, (0, 0, 0))
        rect = opp_text.get_rect()
        rect.right = 308
        surf.blit(text, (12, 0))
        surf.blit(opp_text, rect)

class Duel:
    def __init__(self, card, opp_card, biscuits, particles):
        self.particles = particles
        self.c = card
        self.oc = opp_card
        self.card = load_image(f'cards/{str(card)}-P.png', scale=2)
        self.opp_card = load_image(f'cards/{str(opp_card)}-D.png', scale=2)
        self.prize = biscuits
        print(f'biscuits {self.prize}')
        self.frame = 0

        self.pos = 50
        self.opp_pos = 194

        self.y_pos = 36
        self.tie = False
        self.winner = None

    def result(self, scores):
        if self.c != self.oc:
            if self.c > self.oc:
                scores.score += self.prize
                self.winner = True
            else:
                scores.opp_score += self.prize
                self.winner = False
            return True
        self.tie = True
        return False

    def update(self):
        if self.frame < 60:
            pass
        elif self.frame < 78:
            if not self.tie:
                self.pos += 4
                self.opp_pos -= 4
        elif self.frame > 100:
            return True

        # for i in range(5):
        #     self.particles.append(Particle((random.random() * 76 + 194, random.random() * 108 + self.y_pos), animation_speed=random.randint(3, 6), angle=0))
        self.frame += 1
        return False

    def render(self, surf):
        if self.winner:
            surf.blit(self.opp_card, (self.opp_pos, self.y_pos))
            surf.blit(self.card, (self.pos, self.y_pos))
        else:
            surf.blit(self.card, (self.pos, self.y_pos))
            surf.blit(self.opp_card, (self.opp_pos, self.y_pos))
            

class Particle:
    def __init__(self, pos, animation_speed=5, angle=math.pi):
        self.pos = list(pos)
        self.animation_speed = animation_speed
        self.color = (255, 255, 255)
        self.size = 10
        self.speed = 3
        self.frame = 0
        self.angle = angle
        self.velocity = (math.cos(self.angle) * self.speed, math.sin(self.angle) * self.speed)
    
    def update(self):
        self.pos[0] += self.velocity[0]
        self.pos[1] += self.velocity[1]
        if self.frame % self.animation_speed:
            self.size -= 1

        self.frame += 1
        if self.frame > 30:
            return True
        return False

    def render(self, surf):
        rect = (*self.pos, self.size, self.size)
        pygame.draw.rect(surf, self.color, rect)


class Game:
    def __init__(self):
        pygame.init()

        self.screen = pygame.display.set_mode((1280, 720), pygame.FULLSCREEN)
        self.display = pygame.surface.Surface((320, 180))
        pygame.display.set_caption("Game of Pure Biscuit")
        self.clock = pygame.time.Clock()

        self.scores = Scores()
        self.deck = Deck()
        self.opponent = Opponent()
        self.biscuits = Biscuits()
        self.choosen_card = None

        self.duel = None
        self.particles = []

        self.paused = False
        self.next_round_biscuits = 0

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    close()
                if event.type == pygame.KEYDOWN:
                    if not self.paused:
                        if event.key == pygame.K_RIGHT:
                            self.deck.change_selected(1)
                        if event.key == pygame.K_LEFT:
                            self.deck.change_selected(-1)
                        if event.key == pygame.K_RETURN:
                            self.deck.select()
                        if event.key == pygame.K_ESCAPE:
                            self.paused = True
                    else:
                        if event.key == pygame.K_ESCAPE:
                            self.paused = False
        
            draw_background(self.display)

            if not self.paused:
                if self.choosen_card:
                    # Render duel
                    if self.duel.update():
                        self.choosen_card = None
                    self.duel.render(self.display)
                else:
                    # Render deck + UI
                    self.choosen_card = self.deck.render(self.display)
                    if self.choosen_card:
                        print("old biscuits", self.next_round_biscuits)
                        biscuits = self.biscuits.randomize_biscuits() + self.next_round_biscuits
                        self.next_round_biscuits = 0
                        self.duel = Duel(self.choosen_card,
                                         self.opponent.choose_card(self.choosen_card),
                                         biscuits, self.particles)
                        if self.duel.result(self.scores):
                            print(self.scores.score, self.scores.opp_score)
                        else:
                            self.next_round_biscuits = biscuits
                            print("tie!")
                    
                    self.scores.render(self.display)

                for p in self.particles.copy():
                    p.render(self.display)
                    kill = p.update()
                    if kill:
                        self.particles.remove(p)

            self.screen.blit(pygame.transform.scale(self.display, self.screen.get_size()), (0, 0))
            pygame.display.update()
            self.clock.tick(60)

Game().run()

