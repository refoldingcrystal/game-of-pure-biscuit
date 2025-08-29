import pygame
from scripts.utils import load_image


class Duel:
    def __init__(self, card, opp_card, biscuits, particles):
        self.sounds = {
            'cricket': pygame.mixer.Sound('sfx/cricket.mp3')
        }
        self.sounds['cricket'].set_volume(0.6)
        self.particles = particles
        self.c = card
        self.oc = opp_card
        self.card = load_image(f'cards/{str(card + 1)}-P.png', scale=2)
        self.opp_card = load_image(f'cards/{str(opp_card + 1)}-D.png', scale=2)
        self.result_images = {}
        for name in ['winner', 'loser', 'tie']:
            self.result_images[name] = load_image(f'{name}.png', scale=5)
        self.prize = biscuits
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
        if not self.tie:
            if self.frame < 60:
                pass
            elif self.frame < 78:
                    self.pos += 4
                    self.opp_pos -= 4
            elif self.frame > 100:
                return True
        else:
            if self.frame == 30:
                self.sounds['cricket'].play()
            elif self.frame == 150:
                self.sounds['cricket'].fadeout(1000)
            elif self.frame > 210:
                self.sounds['cricket'].stop()
                return True
            
        # for i in range(5):
        #     self.particles.append(Particle((random.random() * 76 + 194, random.random() * 108 + self.y_pos), animation_speed=random.randint(3, 6), angle=0))
        self.frame += 1
        return False

    def render(self, surf):
        if self.tie:
                surf.blit(self.result_images['tie'], (surf.get_width() // 2 - 60, 10))
        else:
            if self.winner:
                surf.blit(self.result_images['winner'], (surf.get_width() // 2 - 60, 10))
            else:
                surf.blit(self.result_images['loser'], (surf.get_width() // 2 - 60, 10))

        if self.winner:
            surf.blit(self.opp_card, (self.opp_pos, self.y_pos))
            surf.blit(self.card, (self.pos, self.y_pos))
        else:
            surf.blit(self.card, (self.pos, self.y_pos))
            surf.blit(self.opp_card, (self.opp_pos, self.y_pos))