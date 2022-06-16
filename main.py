import random
import csv

totals_csv = open('Hard totals.csv', 'r')
reader = csv.reader(totals_csv)
totals = []
for row in reader:
    totals.append(row)
totals_csv.close()


class Card:
    values = {"2": 2, "3": 3, "4": 4, "5": 5, "6": 6, "7": 7, "8": 8, "9": 9,
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


class Dealer:
    def __init__(self, deck):
        self.hand = random.choices(deck, k=1)
        self.up_card = self.hand[0]
        self.total = self.up_card.get_value()


class Player:
    def __init__(self, deck):
        self.hand = random.choices(deck, k=2)
        self.total = 0
        for i in self.hand:
            self.total += i.get_value()
        # self.bet = bet

    def same_name(self):
        return self.hand[0].get_name() == self.hand[1].get_name()


class Game:
    def __init__(self, deck, totals):
        self.player = Player(deck)
        self.dealer = Dealer(deck)
        self.deck = deck
        self.chart = totals

    def determine_move(self):
        if self.player.total == 16 and 8 < self.dealer.total or self.player.total == 15 and self.dealer.total == 10:
            move = self.surrender()
            print("hello")
        elif self.player.same_name() and ()

    def hit(self):
        pass

    def stand(self):
        pass

    def double(self):
        pass

    def surrender(self):
        pass

    def split(self):
        pass


names = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "jack", "queen", "king", "ace"]
deck = []
for i in range(1, 5):
    for j in names:
        deck.append(Card(j))

main = Game(deck, totals)
