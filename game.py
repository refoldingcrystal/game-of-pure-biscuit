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

class Game:
    def __init__(self):
        pygame.init()

        self.screen = pygame.display.set_mode((1280, 720))
        self.display = pygame.surface.Surface((320, 180))
        self.clock = pygame.time.Clock()

        self.cards = []
        for i in range(1, 14):
            self.cards.append(load_image(f'cards/{str(i)}-P.png'))
        

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    close()
        
            draw_background(self.display)

            self.display.blit(self.cards[5], (50, 50))

            self.screen.blit(pygame.transform.scale(self.display, self.screen.get_size()), (0, 0))
            pygame.display.update()
            self.clock.tick(60)

Game().run()

