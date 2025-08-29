import random
import pygame

from scripts.gameplay import Gameplay
from scripts.menu import Menu
from scripts.pause import Pause
from scripts.utils import Background, Title, close

class Game:
    def __init__(self):
        pygame.init()

        self.screen = pygame.display.set_mode((1280, 720), pygame.FULLSCREEN)
        pygame.display.set_caption("Game of Pure Biscuit")
        self.clock = pygame.time.Clock()
        self.display = pygame.surface.Surface((320, 180))
        self.font = pygame.font.Font("font/jersey.ttf", 40)
        self.sound = pygame.mixer.Sound('sfx/button-mature.mp3')

        self.title = Title()
        self.background = Background()
        self.gameplay = Gameplay(self.display, self.font)
        self.menu = Menu()
        self.pause = Pause()

        self.state = 'paused'
        self.verdict = 'title'
        self.first_time = True

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    close()
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
                            self.sound.play()
                            self.state = 'quit'
                    elif self.state == 'paused':
                        # Endgame & launch
                        self.sound.play()
                        if self.verdict != 'title' or self.first_time:
                            self.first_time = False
                            self.state = 'menu'
                        else:
                            self.state = 'game'
                    elif self.state == 'quit':
                        # Quit menu
                        if event.key == pygame.K_ESCAPE:
                            self.state = 'game'
                            if random.random() < 0.02:
                                pygame.mixer.Sound('sfx/meow.mp3').play()
                        if event.key == pygame.K_UP:
                            self.pause.change_selected(-1)
                        if event.key == pygame.K_DOWN:
                            self.pause.change_selected(1)
                        if event.key == pygame.K_RETURN:
                            decision = self.pause.select()
                            if decision == 'quit':
                                close()
                            elif decision == 'resume':
                                self.state = 'game'
                            else:
                                self.state = 'menu'
                            self.pause.selected = 0
                    else:
                        # Menu
                        if event.key == pygame.K_UP:
                            self.menu.change_selected(-1)
                        if event.key == pygame.K_DOWN:
                            self.menu.change_selected(1)
                        if event.key == pygame.K_RETURN:
                            self.gameplay.new_game(difficulty=self.menu.select())                        
                            self.state = 'game'
        
            self.screen.fill((0x1e, 0x29, 0x2e))
            self.background.render(self.display)

            if self.state == 'game':
                finish = self.gameplay.next()
                if finish:
                    result = self.gameplay.result()
                    self.state = 'paused'
                    self.verdict = 'win' if result else 'lose'
            elif self.state == 'paused':
                self.title.render(self.display, name=self.verdict)
            elif self.state == 'quit':
                self.pause.render(self.display)
            else:
                # Menu
                self.menu.render(self.display)
            
            ratio = self.display.get_width() / self.display.get_height()
            if ratio > self.screen.get_width() / self.screen.get_height():
                width = self.screen.get_width()
                height = int(width / ratio)
            else:
                height = self.screen.get_height()
                width = int(height * ratio)
            self.screen.blit(pygame.transform.scale(self.display, (width, height)),
                             ((self.screen.get_width() - width) // 2, (self.screen.get_height() - height) // 2))
            pygame.display.update()
            self.clock.tick(60)

Game().run()

