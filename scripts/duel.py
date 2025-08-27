from scripts.utils import load_image


class Duel:
    def __init__(self, card, opp_card, biscuits, particles):
        self.particles = particles
        self.c = card
        self.oc = opp_card
        self.card = load_image(f'cards/{str(card + 1)}-P.png', scale=2)
        self.opp_card = load_image(f'cards/{str(opp_card + 1)}-D.png', scale=2)
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