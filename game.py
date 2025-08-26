import pygame

from scripts.duel import Duel
from scripts.deck import Deck
from scripts.logic import Biscuits, Opponent, Scores
from scripts.utils import Background, Title, close

class Game:
    def __init__(self):
        pygame.init()

        # self.screen = pygame.display.set_mode((1280, 720), pygame.FULLSCREEN)
        self.screen = pygame.display.set_mode((1280, 720))
        self.display = pygame.surface.Surface((320, 180))
        pygame.display.set_caption("Game of Pure Biscuit")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font("font/jersey.ttf", 40)
        self.font_small = pygame.font.Font("font/jersey.ttf", 20)

        self.title = Title()
        self.background = Background()
        self.scores = Scores(self.font)
        self.deck = Deck()
        self.opponent = Opponent()
        self.biscuits = Biscuits()
        self.choosen_card = None

        self.duel = None
        self.particles = []

        self.paused = False
        self.next_round_biscuits = 0
        self.prize = 0
        self.timeout = 0

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    close()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    # Only DEBUG !!
                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    display_width, display_height = self.display.get_size()
                    screen_width, screen_height = self.screen.get_size()
                    rel_x = int(mouse_x * display_width / screen_width)
                    rel_y = int(mouse_y * display_height / screen_height)
                    print(rel_x, rel_y)
                if event.type == pygame.KEYDOWN:
                    if not self.paused:
                        if event.key == pygame.K_RIGHT:
                            self.deck.change_selected(1)
                        if event.key == pygame.K_LEFT:
                            self.deck.change_selected(-1)
                        if event.key == pygame.K_RETURN:
                            if not self.choosen_card:
                                self.deck.select()
                        if event.key == pygame.K_ESCAPE:
                            self.paused = True
                    else:
                        self.paused = False
        
            self.background.render(self.display)

            if not self.paused:
                if self.choosen_card:
                    if self.timeout:
                        # Render transition
                        self.timeout -= 1
                    else:
                        # Render duel
                        if self.duel.update():
                            self.choosen_card = None
                        self.duel.render(self.display)
                else:
                    # Render deck + UI
                    self.timeout, self.choosen_card = self.deck.render(self.display)
                    if self.prize == 0:
                        self.prize = self.biscuits.randomize_biscuits(self.next_round_biscuits) + self.next_round_biscuits
                    self.biscuits.render(self.display)
                    if self.choosen_card:
                        self.next_round_biscuits = 0
                        self.duel = Duel(self.choosen_card,
                                        self.opponent.choose_card(self.choosen_card),
                                        self.prize, self.particles)
                        if self.duel.result(self.scores):
                            print(self.scores.score, self.scores.opp_score)
                        else:
                            self.next_round_biscuits = self.prize
                            print("tie!")
                        self.prize = 0
                    
                    self.scores.render(self.display)

                for p in self.particles.copy():
                    p.render(self.display)
                    kill = p.update()
                    if kill:
                        self.particles.remove(p)
            else:
                # Paused menu
                self.title.render(self.display)

            self.screen.blit(pygame.transform.scale(self.display, self.screen.get_size()), (0, 0))
            pygame.display.update()
            self.clock.tick(60)

Game().run()

