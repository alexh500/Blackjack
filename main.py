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
    def __init__(self):
        self.hand = random.choices(deck, k=1)


class Player:
    def __init__(self):
        self.hand = random.choices(deck, k=2)
        self.card1, self.card2 = self.hand
        self.total = self.card1.get_value() + self.card2.get_value()

        # self.bet = bet

    def return_name(self):
        return self.card1.get_name(), self.card2.get_name()

    def same_card(self):
        #return self.card1.same_value(self.card2)
        return self.return_name()[0] == self.return_name()[1]

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
a = Player()
print(a.total, a.return_name(), a.same_card())
