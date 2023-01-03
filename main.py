import random
import csv
import matplotlib.pyplot as plt

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

    def same_name(self, other):
        return self.name == other.name

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
    def __init__(self, rounds_to_play, num_of_decks, deck_penetration, five_card_win, blackjack_payout):
        self.profit = 0
        self.profit_list = []
        self.rounds_to_play = rounds_to_play
        self.rounds_played = 0
        self.rounds_played_list = []
        self.shoe = Shoe(num_of_decks)
        self.num_of_decks = num_of_decks
        self.deck_penetration = deck_penetration
        self.five_card_win = five_card_win
        self.blackjack_payout = blackjack_payout

    def simulate(self):
        while self.rounds_played < self.rounds_to_play:
            self.shoe = Shoe(self.num_of_decks)
            while self.rounds_played < self.rounds_to_play and self.shoe.get_length_of_shoe() > self.num_of_decks * 52 \
                    * self.deck_penetration:
                one_round = Round(self)
                self.profit += one_round.determine_profit()
                print(one_round.determine_profit())
                self.profit_list.append(self.profit)
                self.rounds_played += 1
                self.rounds_played_list.append(self.rounds_played)


class Round:
    def __init__(self, game: Game):
        self.game = game
        self.finished = False
        self.hands_played = 0
        self.bet = 1
        self.player = Player(self, self.bet)
        self.dealer = Dealer(self)
        self.player.deal_hand()

        while not self.finished:
            self.player.calculate_move(self.hands_played)
            self.hands_played += 1
            if self.hands_played == len(self.player.hand_list):
                self.finished = True

        if "stand" in self.player.last_move_list:
            self.deal_dealer_cards()
            self.determine_winner()

        self.determine_profit()

        for i in range(0, len(self.player.hand_list)):
            print(f"Player hand: {self.player.get_hand_names(i)}")
        print(f"Dealer hand:{self.dealer.get_hand_names()}\n")
        print(f"Profit list: {self.player.profit_list_of_hands}")


    """def calculate_bet(self):
        return 1"""

    def determine_profit(self):
        return sum(self.player.profit_list_of_hands)

    def deal_dealer_cards(self):
        while self.dealer.get_hand_value() < 17:
            self.dealer.hand.append(self.game.shoe.remove_card())

    def determine_winner(self):
        for hand_num in range(0,len(self.player.hand_list)):
            if self.player.last_move_list[hand_num] != "stand":
                continue

            elif self.dealer.get_hand_value() == 21:
                self.player.lose()

            elif self.dealer.get_hand_value() > 21:
                self.player.win()

            elif self.dealer.get_hand_value() > self.player.get_hand_value(hand_num):
                self.player.lose()

            elif self.dealer.get_hand_value() < self.player.get_hand_value(hand_num):
                self.player.win()

            else:
                self.player.draw()



class Player:
    def __init__(self, round: Round, bet):
        self.round = round
        self.hand_list = []
        self.bet = bet
        self.first_move = True
        self.profit_list_of_hands = []
        self.last_move_list = []

    def deal_hand(self):
        self.hand_list.append([self.round.game.shoe.remove_card(), self.round.game.shoe.remove_card()])

    def deal_hand_split(self, hand):
        self.hand_list.append([self.hand_list[hand][0], self.round.game.shoe.remove_card()])
        self.hand_list[hand] = [self.hand_list[hand][0], self.round.game.shoe.remove_card()]

    def win(self):
        self.profit_list_of_hands.append(self.bet)


    def lose(self):
        self.profit_list_of_hands.append(-self.bet)


    def draw(self):
        self.profit_list_of_hands.append(0)

    def blackjack_win(self):
        self.profit_list_of_hands.append(self.bet * self.round.game.blackjack_payout)

    def surrender(self):
        self.profit_list_of_hands.append(-self.bet * 0.5)

    def split(self, hand):
        self.deal_hand_split(hand)

    def double(self, hand):
        self.bet *= 2
        self.hand_list[hand].append(self.round.game.shoe.remove_card())

    def hit(self, hand):
        self.hand_list[hand].append(self.round.game.shoe.remove_card())


    def calculate_move(self, hand):
        self.first_move = True
        while True:
            if self.get_hand_value(hand) == 21 and self.first_move:
                self.blackjack_win()
                print("blackjack", self.get_hand_names(hand), self.round.dealer.get_hand_names())
                self.last_move_list.append("blackjack")
                return

            elif self.get_hand_value(hand) > 21:
                self.lose()
                print("lose", self.get_hand_names(hand), self.round.dealer.get_hand_names())
                self.last_move_list.append("blackjack")
                return

            elif (self.get_hand_value(hand) == 21) or \
                    (self.get_hand_length(hand) > 4 and self.round.game.five_card_win):
                self.win()
                print("win", self.get_hand_names(hand), self.round.dealer.get_hand_names())
                self.last_move_list.append("blackjack")
                return

            elif ((self.get_hand_value(hand) == 16 and self.round.dealer.get_hand_value() > 8) or
                  (self.get_hand_value(hand) == 15 and self.round.dealer.get_hand_value() == 10)) and self.first_move:
                print("surrender", self.get_hand_names(hand), self.round.dealer.get_hand_names())
                self.surrender()
                self.last_move_list.append("blackjack")
                return

            elif self.splittable(hand) and totals[self.hand_list[hand][0].get_value() + 16]\
                [self.round.dealer.get_hand_value() -1] == "y":
                print("split", self.get_hand_names(hand), self.round.dealer.get_hand_names())
                self.split(hand)


            elif totals[self.get_hand_value(hand) - 7][self.round.dealer.get_hand_value() - 1] == "d" and self.first_move:
                print("double", self.get_hand_names(hand), self.round.dealer.get_hand_names())
                self.double(hand)
                self.last_move_list.append("stand")
                return

            elif self.get_hand_value(hand) > 16 or \
                    totals[self.get_hand_value(hand) - 7][self.round.dealer.get_hand_value() - 1] == "s":
                print("stand", self.get_hand_names(hand), self.round.dealer.get_hand_names())
                self.last_move_list.append("stand")
                return

            else:
                self.first_move = False
                print("hit", self.get_hand_names(hand), self.round.dealer.get_hand_names())
                self.hit(hand)


    def get_hand_names(self, hand):
        return [i.get_name() for i in self.hand_list[hand]]

    def get_hand_value(self, hand):
        return sum([i.get_value() for i in self.hand_list[hand]])

    def get_hand_length(self, hand):
        return len(self.hand_list[hand])

    def splittable(self, hand):
        return self.hand_list[hand][0].same_name(self.hand_list[hand][1])


class Dealer:
    def __init__(self, round: Round):
        self.round = round
        self.hand = [self.round.game.shoe.remove_card()]

    def get_hand_value(self):
        return sum([i.get_value() for i in self.hand])
    def get_card_value(self, index):
        return self.hand[index].get_value()

    def get_hand_names(self):
        return [i.get_name() for i in self.hand]



blackjack = Game(100000, 8, 0.5, False, 1.5)
blackjack.simulate()
print(blackjack.profit_list)
plt.plot(blackjack.rounds_played_list, blackjack.profit_list)
plt.show()
