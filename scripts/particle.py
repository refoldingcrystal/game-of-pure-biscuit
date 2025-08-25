import math
import pygame


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
