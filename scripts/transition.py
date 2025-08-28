import pygame


class Transition:
    def __init__(self, surf, screenshot):
        self.sound = pygame.mixer.Sound('sfx/transition.mp3')
        self.sound.set_volume(1)
        self.surf = surf
        self.screenshot = screenshot

    def render(self, timeout):
        if timeout == 60:
            self.sound.play()
        t_surf = pygame.Surface(self.surf.get_size())
        t_surf.fill((0x1e, 0x29, 0x2e))
        pygame.draw.circle(t_surf, (0, 0, 0), (t_surf.get_width() // 2, t_surf.get_height() // 2), (abs(30 - timeout)) * 8)
        t_surf.set_colorkey((0, 0, 0))
        if timeout < 30:
            self.surf.blit(t_surf, (0, 0))
        else:
            self.surf.blit(self.screenshot, (0, 0))
            self.surf.blit(t_surf, (0, 0))