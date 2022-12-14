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
    def __init__(self, rounds_to_play, num_of_decks, deck_penetration, five_card_win):
        self.profit = 0
        self.profit_list = []
        self.rounds_to_play = rounds_to_play
        self.rounds_played = 0
        self.rounds_played_list = []
        self.shoe = Shoe(num_of_decks)
        self.num_of_decks = num_of_decks
        self.deck_penetration = deck_penetration
        self.five_card_win = five_card_win

    def simulate(self):
        while self.rounds_played < self.rounds_to_play:
            self.shoe = Shoe(self.num_of_decks)
            while self.rounds_played < self.rounds_to_play and self.shoe.get_length_of_shoe() > self.num_of_decks * 52 \
                    * self.deck_penetration:
                one_round = Round(self)
                print(one_round.player.get_hand_names())
                print(self.shoe.get_length_of_shoe())
                # self.profit += one_round.determine_profit()
                # self.profit_list.append(self.profit)
                self.rounds_played += 1
                self.rounds_played_list.append(self.rounds_played)


class Round:
    def __init__(self, game: Game):
        self.game = game
        self.bet = self.calculate_bet()
        self.player = Player(self, self.bet)
        self.dealer = Dealer(self)
        self.first_move = True



    def calculate_bet(self):
        return 1

    def win(self):
        pass

    def lose(self):
        pass

    def draw(self):
        pass

    def blackjack_win(self):
        pass

    def surrender(self):
        pass

    def split(self):
        pass

    def double(self):
        pass

    def hit(self):
        pass

    def stand(self):
        pass

    def calculate_move(self):
        while True:
            if self.player.get_hand_value() == 21 and self.first_move:
                self.blackjack_win()
                print("blackjack")

            elif self.player.get_hand_value() > 21:
                self.lose()
                print("lose")

            elif (self.player.get_hand_value() == 21) or (self.player.get_hand_length() > 4 and self.game.five_card_win):
                self.win()
                print("win")

            elif ((self.player.get_hand_value() == 16 and self.dealer.get_hand_value() > 8) or
                  (self.player.get_hand_value() == 15 and self.dealer.get_hand_value() == 10)) and self.first_move:
                self.surrender()
                print("surrender")

            elif self.player.splittable() and totals[self.player.hand[0].get_value() + 16]\
                [self.dealer.get_hand_value() -1] == "y" and self.first_move:
                self.first_move = False
                self.split()




    def determine_profit(self):
        pass


class Player:
    def __init__(self, round: Round, bet):
        self.round = round
        self.hand = [self.round.game.shoe.remove_card(), self.round.game.shoe.remove_card()]
        self.bet = bet

    def get_hand_names(self):
        return [i.get_name() for i in self.hand]

    def get_hand_value(self):
        return sum([i.get_value() for i in self.hand])

    def get_hand_length(self):
        return len(self.hand)

    def splittable(self):
        return self.hand[0].same_value(self.hand[1])

class Dealer:
    def __init__(self, round: Round):
        self.round = round
        self.hand = [self.round.game.shoe.remove_card()]

    def get_hand_value(self):
        return sum([i.get_value() for i in self.hand])


blackjack = Game(5, 1, 0.5, True)
blackjack.simulate()
