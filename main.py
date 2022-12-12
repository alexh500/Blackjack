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



class Player:
    def __init__(self):


class Dealer:
    pass

class Round:
    def __init__(self, game: Game):
        self.player = Player()
        self.dealer = Dealer()
        self.game = game

    def calculate_move(self):
        while True:
            if

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
            self.shoe = self.shoe.create_shoe()
            while self.rounds_played < self.rounds_to_play and len(self.shoe) > self.num_of_decks * 52 * self.deck_penetration:
                round = Round(self)




