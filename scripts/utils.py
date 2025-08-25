import sys
import pygame


def close():
    pygame.quit()
    sys.exit()

class Background:
    def __init__(self):
        self.c1 = (0x59, 0x85, 0x32)
        self.c2 = (0x4f, 0x77, 0x2d)
        self.tile_size = 10

    def render(self, surf):
        surf.fill(self.c1)
        for x in range(320 // self.tile_size + 1):
            for y in range(180 // self.tile_size + 1):
                if (x + y) % 2:
                    rect = (x * self.tile_size, y * self.tile_size,
                            self.tile_size, self.tile_size)
                    pygame.draw.rect(surf, self.c2, rect)

class PauseMenu:
    def __init__(self, font):
        self.font = font
        self.text = self.font.render("Click any key to continue", False, (0, 0, 0))
        self.rect = self.text.get_rect()
        self.rect.left = 160 - self.rect.width // 2
        self.rect.top = 150

    def render(self, surf):
        surf.blit(self.text, self.rect)

def load_image(path, scale=1):
    image = pygame.image.load(path).convert_alpha()
    return pygame.transform.scale(image, (image.get_width() // 5 * scale, image.get_height() // 5 * scale))
