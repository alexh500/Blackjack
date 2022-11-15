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
        self.low_total = 0
        for i in self.hand:
            self.total += i.get_value()
        if self.hand[0].get_name() == "ace" or self.hand[1].get_name() == "ace":
            self.low_total = self.total - 10
        self.bet = 1

    def same_name(self):
        return self.hand[0].get_name() == self.hand[1].get_name()


class Game:
    def __init__(self, deck, totals):
        self.player = Player(deck)
        self.dealer = Dealer(deck)
        self.deck = deck
        self.chart = totals

    def determine_move(self):
        finish_move = False
        first_move = True
        while not finish_move:
            print(self.player.hand[0].get_name(), self.player.hand[1].get_name(), self.player.total,
                  self.dealer.up_card.get_name())
            if self.player.total == 16 and 8 < self.dealer.total or self.player.total == 15 and self.dealer.total == 10 \
                    and first_move:
                """move = self.surrender()"""
                print("surrender")

            elif self.player.same_name() and self.chart[self.player.hand[0].get_value() +
                                                        16][self.dealer.up_card.get_value() - 1] == "y" and first_move:
                """move=self.split()"""
                print("split")

            elif self.player.total < 9 or (self.chart[self.player.total - 7][self.dealer.total - 1] == "h" and
                                           self.chart[self.player.total - 7][0] == str(self.player.total)):
                move = self.hit()
                print(move)

            elif self.player.total > 16 or (self.chart[self.player.total - 7][self.dealer.total - 1] == "s" and
                                            self.chart[self.player.total - 7][0] == str(self.player.total)):
                """move = self.stand()"""
                print("stand")
            else:
                move = self.double()
                print(move)
            first_move = False

    def hit(self):
        self.player.hand.append(self.deck[random.randint(0, len(self.deck) - 1)])
        return self.player.hand

    def stand(self):
        pass

    def double(self):
        self.player.bet *= 2
        return self.hit(), self.player.bet

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
main.determine_move()
