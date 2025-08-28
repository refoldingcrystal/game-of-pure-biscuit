from scripts.deck import Deck
from scripts.duel import Duel
from scripts.logic import Biscuits, Opponent, Scores
from scripts.transition import Transition

class Gameplay:
    def __init__(self, display, font):
        self.display = display
        self.font = font

    def new_game(self, difficulty='normal', slow=True):
        self.scores = Scores(self.font)
        self.deck = Deck(slow)
        self.opponent = Opponent(difficulty)
        self.biscuits = Biscuits()

        self.choosen_card = None
        self.duel = None
        self.transition = None
        self.particles = []

        self.next_round_biscuits = 0
        self.prize = 0
        self.timeout = 0

        self.round = 0

    def result(self):
        return self.scores.result()

    def select(self):
        if not self.choosen_card:
            self.deck.select()
    
    def change_selected(self, movement):
        self.deck.change_selected(movement)

    def next(self):
        if self.choosen_card:
            # Render duel
            if self.duel.update():
                self.choosen_card = None
            self.duel.render(self.display)
        else:
            # Render deck + UI
            self.biscuits.render(self.display)
            self.timeout, self.choosen_card = self.deck.render(self.display)
            if self.prize == 0:
                self.round += 1
                if self.round <= 13:
                    self.prize = self.biscuits.randomize_biscuits(self.next_round_biscuits) + self.next_round_biscuits
            self.scores.render(self.display)
            if self.round > 13:
                return self.scores.ready()
            if self.timeout:
                screenshot = self.display.copy()
                self.transition = Transition(self.display, screenshot)
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
            

        for p in self.particles.copy():
            p.render(self.display)
            kill = p.update()
            if kill:
                self.particles.remove(p)

        if self.timeout:
            # Render transition
            self.transition.render(self.timeout)
            self.timeout -= 1
            if not self.timeout:
                self.deck.select_lock = False
            
        
        return False
