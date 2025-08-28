import pygame

from scripts.gameplay import Gameplay
from scripts.menu import Menu
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
        self.menu = Menu()

        self.slow = True
        # TEMPORARY
        self.gameplay.new_game(self.slow)
        self.states = ['paused', 'menu', 'game']
        self.state = self.states[0]
        self.verdict = 'title'
        self.first_time = True

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    close()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    # ONLY DEBUG
                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    display_width, display_height = self.display.get_size()
                    screen_width, screen_height = self.screen.get_size()
                    rel_x = int(mouse_x * display_width / screen_width)
                    rel_y = int(mouse_y * display_height / screen_height)
                    print(rel_x, rel_y)
                if event.type == pygame.KEYDOWN:
                    if self.state == 'game':
                        # Game
                        if event.key == pygame.K_RIGHT:
                            self.gameplay.change_selected(1)
                        if event.key == pygame.K_LEFT:
                            self.gameplay.change_selected(-1)
                        if event.key == pygame.K_RETURN:
                            self.gameplay.select()
                        if event.key == pygame.K_ESCAPE:
                            self.state = 'paused'
                            self.verdict = 'title'
                    elif self.state == 'paused':
                        # Pause
                        if self.verdict != 'title' or self.first_time:
                            self.first_time = False
                            self.state = 'menu'
                        else:
                            self.state = 'game'
                    else:
                        # Menu
                        if event.key == pygame.K_UP:
                            self.menu.change_selected(-1)
                        if event.key == pygame.K_DOWN:
                            self.menu.change_selected(1)
                        if event.key == pygame.K_RETURN:
                            self.gameplay.new_game(difficulty=self.menu.select())                        
                            self.state = 'game'
        
            self.background.render(self.display)

            if self.state == 'game':
                finish = self.gameplay.next()
                if finish:
                    result = self.gameplay.result()
                    self.state = 'paused'
                    self.verdict = 'win' if result else 'lose'
            elif self.state == 'paused':
                self.title.render(self.display, name=self.verdict)
            else:
                # Menu
                self.menu.render(self.display)

            self.screen.blit(pygame.transform.scale(self.display, self.screen.get_size()), (0, 0))
            pygame.display.update()
            self.clock.tick(60)

Game().run()

