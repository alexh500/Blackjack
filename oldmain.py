import random
import csv

totals_csv = open('Hard totals.csv', 'r')
reader = csv.reader(totals_csv)
totals = []
for row in reader:
    totals.append(row)
totals_csv.close()


class Card:
    values = {"1": 1, "2": 2, "3": 3, "4": 4, "5": 5, "6": 6, "7": 7, "8": 8, "9": 9,
              "10": 10, "jack": 10, "queen": 10, "king": 10, "ace": 11}

    def __init__(self, name):
        self.name = name
        self.value = self.values[name]

    def get_value(self):
        return self.value

    def same_value(self, other):
        return self.value == other.value

    def get_name(self):
        return self.name


class Shoe:
    def __init__(self, num_of_decks):
        self.num_of_decks = num_of_decks
        names = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "jack", "queen", "king", "ace"]
        self.deck = []
        for k in range(0, self.num_of_decks):
            for i in range(0, 4):
                for j in names:
                    self.deck.append(Card(j))
        random.shuffle(self.deck)

    def remove_card(self):
        card = self.deck.pop()
        return card

    def get_length_of_shoe(self):
        return len(self.deck)


class Game:
    def __init__(self, rounds_to_play, num_of_decks, deck_penetration):
        self.profit = 0
        self.profit_list = []
        self.rounds_to_play = rounds_to_play
        self.rounds_played = 0
        self.rounds_played_list = []
        self.shoe = Shoe(num_of_decks)
        self.num_of_decks = num_of_decks
        self.deck_penetration = deck_penetration

    def simulate(self):
        while self.rounds_played < self.rounds_to_play:
            self.shoe = Shoe(self.num_of_decks)
            while self.rounds_played < self.rounds_to_play and self.shoe.get_length_of_shoe() > self.num_of_decks * 52 \
                    * self.deck_penetration:
                one_round = Round(self)
                print(one_round.hand_cards())
                #self.profit += one_round.determine_profit()
                #self.profit_list.append(self.profit)
                self.rounds_played += 1
                self.rounds_played_list.append(self.rounds_played)


class Round:
    def __init__(self, game: Game):
        self.game = game
        self.player_hand = [self.game.shoe.remove_card(), self.game.shoe.remove_card()]

    def calculate_move(self):
        pass

    def determine_profit(self):
        pass

    def hand_cards(self):
        return [i.get_name() for i in self.player_hand]


class Player:
    pass


class Dealer:
    pass


blackjack = Game(1, 1, 0)
blackjack.simulate()
