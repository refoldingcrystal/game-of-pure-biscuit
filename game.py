import pygame

from scripts.duel import Duel
from scripts.deck import Deck
from scripts.gameplay import Gameplay
from scripts.logic import Biscuits, Opponent, Scores
from scripts.utils import Background, Title, close

class Game:
    def __init__(self):
        pygame.init()

        # self.screen = pygame.display.set_mode((1280, 720), pygame.FULLSCREEN)
        self.screen = pygame.display.set_mode((1280, 720))
        pygame.display.set_caption("Game of Pure Biscuit")
        self.clock = pygame.time.Clock()
        self.display = pygame.surface.Surface((320, 180))
        self.font = pygame.font.Font("font/jersey.ttf", 40)

        self.title = Title()
        self.background = Background()
        self.gameplay = Gameplay(self.display, self.font)

        self.paused = True
        self.verdict = 'title'

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
                            self.gameplay.change_selected(1)
                        if event.key == pygame.K_LEFT:
                            self.gameplay.change_selected(-1)
                        if event.key == pygame.K_RETURN:
                            self.gameplay.select()
                        if event.key == pygame.K_ESCAPE:
                            self.paused = True
                    else:
                        self.paused = False
        
            self.background.render(self.display)

            if not self.paused:
                finish = self.gameplay.next()
                if finish:
                    result = self.gameplay
                    self.paused = True
                    self.verdict = 'win' if result else 'lose'
            else:
                self.title.render(self.display, name=self.verdict)

            self.screen.blit(pygame.transform.scale(self.display, self.screen.get_size()), (0, 0))
            pygame.display.update()
            self.clock.tick(60)

Game().run()

