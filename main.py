import csv
import math
import random
from tkinter import font, Tk, Button, Label, OptionMenu, Entry, StringVar, Toplevel, Message

import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# importing all the libraries that I will use


totals_csv = open('Hard totals.csv', 'r')
# opens the csv for basic strategy
reader = csv.reader(totals_csv)
# creates a reader variable
totals = []
# creates a variable that will be used as the contents of the csv in the code
for row in reader:
    # creates a for loop to go through the rows of the csv
    totals.append(row)
    # adding the contents of each row to the totals variable
totals_csv.close()
# closing the csv

illustrous_18_csv = open('illustrous_18.csv', 'r')
# opens the csv for the illustrous 18 card counting deviations
reader = csv.reader(illustrous_18_csv)
# creates a reader variable
illustrous_18 = []
# creates a variable that will be used as the contents of the csv in the code
for row in reader:
    # creates a for loop to go through the rows of the csv
    illustrous_18.append(row)
    # adding the contents of each row to the illustrous 18 variable
illustrous_18_csv.close()


# closing the csv

class Card:
    # creates a class called Card

    values = {"1": 1, "2": 2, "3": 3, "4": 4, "5": 5, "6": 6, "7": 7, "8": 8, "9": 9,
              "10": 10, "jack": 10, "queen": 10, "king": 10, "ace": 11}

    # creates a dictionary with each card name and their respective values

    def __init__(self, name):
        # define the init method which initialises the attributes of the class
        self.name = name
        # creates a name attribute
        self.value = self.values[name]
        # creates a value attribute which is found by searching through the values dictionary using the name

    def get_value(self):
        # defines the get value method
        return self.value
        # returns the value of the card

    def same_value(self, other):
        # defines the same value method, which takes in an argument of other which is another instance of the class Card
        return self.value == other.value
        # returns True if the value of the two instances of the card class are the same, False if not

    def get_name(self):
        # defines the get name method
        return self.name
        # returns the name of the card

    def same_name(self, other):
        # defines the same name method, which takes in an argument of other which is another instance of the class Card
        return self.name == other.name
        # returns True if the name of the two instances of the card class are the same, False if not


class Shoe:
    # creates a class called Shoe

    def __init__(self, num_of_decks, game):
        # define the init method which initialises the attributes of the class
        self.num_of_decks = num_of_decks
        # creates a number of decks attribute
        self.game = game
        # creates a game attribute, which is the game that is being played which is passed as a parameter when
        # instantiating an instance of the class
        names = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "jack", "queen", "king", "ace"]
        # creates a list called names with all the names of the different cards
        self.count_value = {"2": 1, "3": 1, "4": 1, "5": 1, "6": 1, "7": 0, "8": 0, "9": 0,
                            "10": -1, "jack": -1, "queen": -1, "king": -1, "ace": -1}
        # creates a dictionary with the card names as keys and their value in the high low card counting system
        self.deck = []
        # creates a deck attribute which is an empty list
        for k in range(0, self.num_of_decks):
            # creates a for loop that goes from 0 to the number of decks - 1
            for i in range(0, 4):
                # creates a for loop from 0 to 3, for each suit in the deck
                for j in names:
                    # creates a for loop cycling through the values in the names list
                    self.deck.append(Card(j))
                    # instantiates an instance of the Card class for each name, with the name being the name used in
                    # the object. This object is then appended to the deck variable
        random.shuffle(self.deck)
        # shuffles the deck
        self.game.running_count = 0
        # sets the running count to be 0, so whenever the shoe is shuffled the count goes back to 0
        self.game.true_count = 0
        # sets the true count to be 0, so whenever the shoe is shuffled the count goes back to 0

    def remove_card(self):
        # defines the remove card method, one of the most important methods in the entire program
        card = self.deck.pop()
        # removes a card from the deck and assigns it the name card
        self.game.running_count += self.count_value[card.get_name()]
        # adds to the running count the count value of the removed card by finding the value of the key being the
        # cards name in the dictionary count value
        self.game.true_count = self.game.running_count / (math.ceil(self.get_length_of_shoe() / 52))
        # adjusts the true count be defining it again - the running count divided by the number of decks left in the shoe
        return card
        # returns the removed card

    def get_length_of_shoe(self):
        # defines a method get length of shoe
        return len(self.deck)
        # returns the length of the shoe


class Game:
    # creates a class called Game
    def __init__(self, rounds_to_play, num_of_decks, deck_penetration, five_card_win, blackjack_payout, card_counting):
        # defines the init method where all the attributes of the class are defined
        self.profit = 0
        # creates a profit attribute with value 0
        self.profit_list = []
        # creates a list of profit values to be used in the graph later. Initially it is an empty list
        self.count_list = []
        # creates a list of count values to be used in the graph later. Initially it is an empty list
        self.rounds_to_play = rounds_to_play
        # creates a rounds to play attribute which is the value set by the player
        self.rounds_played = 0
        # creates a round played attribute which is initially 0
        self.rounds_played_list = []
        # creates a list of the round numbers to be used in the graphs later. Initially it is an empty list
        self.shoe = Shoe(num_of_decks, self)
        # creates the shoe by instantiating an instance of the class, passing in parameters of number of decks
        # and the game itself
        self.num_of_decks = num_of_decks
        # creates a number of decks attribute which is the value set by the player
        self.deck_penetration = deck_penetration
        # creates a deck penetration attribute which is the value set by the player
        self.five_card_win = five_card_win
        # creates a five card win attribute that has value True or False, which is set by the player
        self.blackjack_payout = blackjack_payout
        # creates a blackjack payout attribute that is the value set by the player
        self.card_counting = card_counting
        # creates a boolean card counting attribute that is set by the player
        self.running_count = 0
        # creates a running count attribute that is initialling 0
        self.true_count = self.running_count // (math.ceil(self.shoe.get_length_of_shoe() / 52))
        # creates a true count attribute that is initially the running count divided by the number of decks remaining
        # in the shoe
        self.hands_won = 0
        # creates a hands won attribute that is initially 0
        self.hands_drew = 0
        # creates a hands drew attribute that is initially 0
        self.hands_lost = 0
        # creates a hands lost attribute that is initially 0
        self.hands_surrendered = 0
        # creates a hands surrendered attribute that is initially 0
        self.hands_blackjack = 0
        # creates a number of blackjacks attribute that is initially 0
        self.hands_21 = 0
        # creates a hands reached 21 attribute that is initially 0
        self.hands_bust = 0
        # creates a hands that went bust attribute that is initially 0
        self.hands_player_beat_dealer = 0
        # creates an attribute that is the number of times the player was closer to 21 than the dealer
        # that is initially 0
        self.hands_dealer_beat_player = 0
        # creates an attribute that is the number of times the dealer was closer to 21 than the player
        # that is initially 0
        self.hands_dealer_bust = 0
        # creates a hands the dealer went bust attribute that is initially 0

    def simulate(self):
        # defines the simulate method, where each round is called from
        while self.rounds_played < self.rounds_to_play:
            # creates a while that halts once the number of rounds played is equal to the number of rounds to be played
            self.shoe = Shoe(self.num_of_decks, self)
            # remakes the shoe when the deck penetration is reached
            while self.rounds_played < self.rounds_to_play and self.shoe.get_length_of_shoe() > self.num_of_decks * 52 \
                    * (1 - self.deck_penetration):
                # checks to see if the deck penetration has been and if the number of rounds played is of
                # an acceptable number
                if self.shoe.get_length_of_shoe() < 15:
                    # checks to see if the number of card in the deck is too small, even if the deck penetration
                    # has not been reached yet
                    self.shoe = Shoe(self.num_of_decks, self)
                    # remakes the shoe
                one_round = Round(self)
                # instantiates an instance of the Round class called one round. This automatically plays out the round
                self.profit += one_round.determine_profit()
                # adjusts the profit variable according to the outcome of the determine profit method of the Round class
                self.profit_list.append(self.profit)
                # adds the new profit value to the profit list
                self.count_list.append(self.true_count)
                # adds the new count value to the count list
                self.rounds_played += 1
                # increments the round counter by 1
                self.rounds_played_list.append(self.rounds_played)
                # adds the new rounds played number to the rounds played list
                self.hands_won += one_round.player.hand_status.count("w") + one_round.player.hand_status.count("b")
                # adds the number of w's or b's in the hand status attribute of player to the hands won attribute, each
                # of these representing a won hand
                self.hands_lost += one_round.player.hand_status.count("l") + one_round.player.hand_status.count("s")
                # adds the number of l's or s's in the hand status attribute of player to the hands lost attribute, each
                # of these representing a lost hand
                self.hands_drew += one_round.player.hand_status.count("d")
                # adds the number of d's in the hand status attribute of player to the hands drew attribute, each of
                # these representing a drew hand
                self.hands_surrendered += one_round.player.hand_status.count("s")
                # adds the number of s's in the hand status attribute of player to the hands surrendered attribute, each
                # of these representing a surrendered hand
                self.hands_blackjack += one_round.player.hand_status.count("b")
                # adds the number of b's in the hand status attribute of player to the hands blackjack attribute, each
                # of these representing a hand that was a blackjack
                self.hands_21 += one_round.player.hand_status.count("21")
                # adds the number of 21's in the hand status attribute of player to the hands 21 attribute, each
                # of these representing a hand that reached 21
                self.hands_bust += one_round.player.hand_status.count("bust")
                # adds the number of bust's in the hand status attribute of player to the hands bust attribute, each
                # of these representing a bust hand
                self.hands_player_beat_dealer += one_round.player.hand_status.count("player>dealer")
                # adds the number of player>dealer's in the hand status attribute of player to the hands player beat
                # dealer attribute, each of these representing a hand in which the player was closer to 21 than
                # the dealer
                self.hands_dealer_beat_player += one_round.player.hand_status.count("dealer>player")
                # adds the number of dealer>player's in the hand status attribute of player to the hands dealer beat
                # player attribute, each of these representing a hand in which the dealer was closer to 21 than
                # the player
                self.hands_dealer_bust += one_round.player.hand_status.count("dealer_bust")
                # adds the number of dealer_bust's in the hand status attribute of player to the hands dealer bust
                # attribute, each of these representing a hand in which the dealer was bust


class Round:
    # defines the class Round
    def __init__(self, game: Game):
        # defines the init method which instantiates all the attributes when an instance of the class is created
        self.game = game
        # creates a game attribute which is the instance of the game class that is passed to the class as a parameter
        self.finished = False
        # creates an attribute called finished which is False
        self.hands_played = 0
        # creates a hands played attribute that is set to be 0
        self.bet_calc = self.calculate_bet()
        # creates a bet calc attribute which is the output of the calculate bet method
        self.player = Player(self, self.bet_calc)
        # creates a player attribute which is an instance of the Player class
        self.dealer = Dealer(self)
        # creates a dealer attribute which is an instance of the Dealer class
        self.dealer_hand_value = self.dealer.get_hand_value()
        # creates a dealer hand value attribute with the output of the get hand value method in the Dealer class
        # as the value
        self.player.deal_hand()
        # calls the deal hand method from the Player class

        while not self.finished:
            # checks to make sure that the finished attribute is still False
            self.player.bet = self.bet_calc
            # sets the attribute bet from the Player class to be the bet calc attribute
            self.player.calculate_move(self.hands_played)
            # runs the method calculate move from the Player class which plays one of the players hands fully
            self.hands_played += 1
            # increments the number of hands that have been played by 1
            if self.hands_played == len(self.player.hand_list):
                # checks to see if the number of hands that have been played is the total number of hands that the
                # player has
                self.finished = True
                # if they are equal, the finished attribute is set to True which would terminate the loop the next time
                # it checks

        if "stand" in self.player.last_move_list or "double" in self.player.last_move_list:
            # checks if any of the hands' final move was stand or double, to determine if the dealer needs to deal
            # their cards out
            self.deal_dealer_cards()
            # if true, the deal dealer cards method is called

        self.determine_winner()
        # the determine winner method is called which compares the dealers hand and each of the players hands in turn
        # and determines the winner

    def calculate_bet(self):
        # defines the method calculate bet
        if not self.game.card_counting or self.game.true_count <= 0:
            # check to see if card counting is being played or if the count is less than 0
            return 1
            # if so, return 1
        return int(self.game.true_count)
        # if card counting is being played and the count is larger than 0, return the count rounded down to the
        # nearest integer

    def determine_profit(self):
        # defines the determine profit method
        return sum(self.player.profit_list_of_hands)
        # returns the sum of the profit list of hands attribute in the Player class, a list of all the profits of the
        # player's hands

    def deal_dealer_cards(self):
        # defines the deal dealer cards method
        if self.dealer.get_card_value(-1) == 11:
            # checks to see if the initial dealer card is an ace
            aces = 1
            # if so, aces = 1
        else:
            aces = 0
            # if not, aces = 0
        while self.dealer_hand_value < 17:
            # checks to see what the value is of the dealer hand
            self.dealer.hand.append(self.game.shoe.remove_card())
            # append the output of the remove card method from the Shoe class
            if self.dealer.get_card_value(-1) == 11:
                # checks if the card just drew is an ace
                aces += 1
                # if so, aces += 1
            if aces > 1:
                # checks if the dealer has multiple aces in their hand
                self.dealer_hand_value = self.dealer.get_hand_value() - 10 * (aces - 1)
                # if they do, the excess aces are converted to 1's, altering the value of the hand
            else:
                self.dealer_hand_value = self.dealer.get_hand_value()
                # if there is not multiple aces, the dealer hand value is the output of the get hand value method
                # from the Dealer class
            if self.dealer.get_hand_value() > 21 and aces > 0:
                # check to see if the dealer is bust, and they have any aces to convert into 1's
                self.dealer_hand_value = self.dealer.get_hand_value() - 10 * aces
                # changes the dealer hand value attribute to make all the aces into 1's

    def determine_winner(self):
        # defines the method determine winner
        for hand_num in range(0, len(self.player.hand_list)):
            # creates a for loop that goes from 0 to the number of hands of the player - 1. This is so each hand is
            # checked
            if self.player.last_move_list[hand_num] == "blackjack":
                # checks if the last move of the hand is blackjack
                self.player.blackjack_win()
                # runs the blackjack win method from the Player class
            elif self.player.last_move_list[hand_num] == "bust":
                # checks if the last move the of hand is bust
                self.player.lose(False)
                # runs the lose method from the Player class with the double parameter being False
                self.player.hand_status.append("bust")
                # adds bust to the hand status list attribute of the Player class
            elif self.player.last_move_list[hand_num] == "21":
                # checks if the last move of the hand is 21
                self.player.win(False)
                # runs the win method from the Player class with double parameter False
                self.player.hand_status.append("21")
                # adds 21 to the hand status list attribute of the Player class
            elif self.player.last_move_list[hand_num] == "surrender":
                # checks if the last move of the hand is surrender
                self.player.surrender()
                # runs the surrender method from the Player class
            elif self.player.last_move_list[hand_num] == "double":
                # checks if the last move of the hand is double
                self.compare_to_dealer(hand_num, True)
                # runs the compare to dealer method, passing in the hand number and making the double parameter True
            else:
                self.compare_to_dealer(hand_num, False)
                # runs the compare to dealer method, passing in the hand number and making the double parameter False

    def compare_to_dealer(self, hand_num, double):
        # defines the compare to dealer method
        if self.player.get_hand_value(hand_num) == 21:
            # checks if the value of the hand is equal to 21
            self.player.win(double)
            # runs the win method from the Player class
            self.player.hand_status.append("21")
            # adds 21 to the hand status list attribute from the Player class
        elif self.dealer.get_hand_value() > 21:
            # checks if the value of the dealer's hands is over 21
            self.player.win(double)
            # runs the win method from the Player class
            self.player.hand_status.append("dealer_bust")
            # adds dealer bust to the hand status list attribute from the Player class
        elif self.dealer.get_hand_value() < self.player.get_hand_value(hand_num):
            # checks if the value of the dealer's hand is less than the value of the player's hand
            self.player.win(double)
            # runs the win method from the Player class
            self.player.hand_status.append("player>dealer")
            # adds player>dealer to the hand status list attribute from the Player class
        elif self.dealer.get_hand_value() > self.player.get_hand_value(hand_num):
            # checks if the value of the dealer's hand is more than the value of the player's hand
            self.player.lose(double)
            # runs the lose method from the Player class
            self.player.hand_status.append("dealer>player")
            # adds dealer>player to the hand status list attribute from the Player class
        else:
            self.player.draw()
            # runs the draw method from the player Class


class Player:
    # creates the Player class
    def __init__(self, round: Round, bet):
        # defines the init method which instantiates all the attributes of the class
        self.round = round
        # creates a round attribute
        self.hand_list = []
        # creates a hand list attribute which is initially an empty list
        self.bet = bet
        # creates a bet attribute
        self.first_move = True
        # creates a boolean attribute called first move which is initially True
        self.profit_list_of_hands = []
        # creates an attribute called profit list of hands which is initially an empty list
        self.last_move_list = []
        # creates an attribute called last move list which is initially an empty list
        self.hand_status = []
        # creates an attribute called hand status which is initially an empty list

    def deal_hand(self):
        # defines the deal hand method
        self.hand_list.append([self.round.game.shoe.remove_card(), self.round.game.shoe.remove_card()])
        # the method remove card from the Shoe class is called twice. Both of the removed cards are added to the hand
        # list as their own list

    def deal_hand_split(self, hand):
        # defines the deal hand split method, which is another way of dealing cards when the player split their hand
        self.hand_list.append([self.hand_list[hand][0], self.round.game.shoe.remove_card()])
        # a list is created with one of the cards in the original hand and another card that was removed from the shoe.
        # This list is then appended to the hand list attribute
        self.hand_list[hand] = [self.hand_list[hand][0], self.round.game.shoe.remove_card()]
        # the list in index hand in the hand list is altered where the first game remains the same,
        # but the second come is now a new card that has been removed

    def win(self, double):
        # defines the win method
        if double:
            # checking if the double parameter is true
            self.profit_list_of_hands.append(self.bet * 2)
            # if it is true, the bet is multiplied by 2 and this number is appended to the profit list of hands attribute
        else:
            self.profit_list_of_hands.append(self.bet)
            # the bet attribute is appended to the profit list of hands attribute
        self.hand_status.append("w")
        # w is added to the hand status attribute

    def lose(self, double):
        # defines the lose method
        if double:
            # checking if the double parameter is true
            self.profit_list_of_hands.append(-self.bet * 2)
            # if it is true, the bet is multiplied by 2 and the negative of this number is appended to the
            # profit list of hands attribute
        else:
            self.profit_list_of_hands.append(-self.bet)
            # the negative of the bet attribute is appended to the profit list of hands attribute
        self.hand_status.append("l")
        # l is added to the hand status attribute

    def draw(self):
        # defines the draw method
        self.profit_list_of_hands.append(0)
        # appends 0 to the profit list of hands attribute
        self.hand_status.append("d")
        # d is added to the hand status attribute

    def blackjack_win(self):
        # defines the blackjack win method
        self.profit_list_of_hands.append(self.bet * self.round.game.blackjack_payout)
        # the bet attribute is multiplied by the blackjack payout attribute of the Game class. This value is then added
        # to the profit list of hands attribute
        self.hand_status.append("b")
        # b is added to the hand status attribute

    def surrender(self):
        # defines the surrender method
        self.profit_list_of_hands.append(-self.bet * 0.5)
        # multiplies the attribute the bet by -0.5, then appends that value to the profit list of hands attribute
        self.hand_status.append("s")
        # s is added to the hand status attribute

    def split(self, hand):
        # defines the split method
        self.deal_hand_split(hand)
        # runs the deal hand split method

    def hit(self, hand):
        # defines the hit method
        self.hand_list[hand].append(self.round.game.shoe.remove_card())
        # a card is removed from the shoe via the remove card method, then that card is appended to the hand list
        # attribute at the index of the current hand being played

    def calculate_move(self, hand):
        # defines the calculate move method
        self.first_move = True
        # sets the first move attribute to True
        while True:
            # initialises the while loop, so moves are being made until the loop is broken via a different method
            if self.check_card_counting_moves(hand):
                # runs the check card counting moves method
                return
                # if true, the method is exited from immediately

            elif self.get_hand_value(hand) == 21 and self.first_move:
                # checks to see if the hand value is 21 and it is the first move, in which case the player has a
                # blackjack
                self.last_move_list.append("blackjack")
                # adds blackjack to the last move list attribute
                return
                # exits the method

            elif self.get_hand_value(hand) > 21:
                # checks to see if the player's hand value is over 21
                self.last_move_list.append("bust")
                # if it is, bust is appended to the last move list attribute
                return
                # exits the method

            elif (self.get_hand_value(hand) == 21) or \
                    (self.get_hand_length(hand) > 4 and self.round.game.five_card_win):
                # checks if either the player's hand adds up to 21 or if the player's hand is 5 cards and they are
                # playing the 5 card win rule
                self.last_move_list.append("21")
                # adds 21 to the last move list attribute
                return
                # exits the method

            elif self.get_hand_value(hand) > 16:
                # checks to see if the hand value is over 16
                self.last_move_list.append("stand")
                # adds stand to the last move list attribute
                return
                # exits the method

            elif ((self.get_hand_value(hand) == 16 and self.round.dealer.get_hand_value() > 8) or
                  (self.get_hand_value(hand) == 15 and self.round.dealer.get_hand_value() == 10)) and self.first_move:
                # checks to see if according to basic strategy, the player should surrender and that the first move
                # attribute is True so they are allowed to surrender
                self.last_move_list.append("surrender")
                # adds surrender to the last move list attribute
                return
                # exits the method

            elif self.splittable(hand) and totals[self.hand_list[hand][0].get_value() + 16] \
                    [self.round.dealer.get_hand_value() - 1] == "y":
                # checks to see if according to basic strategy the player should split, and also runs the splittable
                # method to see if they are allowed to split
                self.split(hand)
                # runs the split method


            elif totals[self.get_hand_value(hand) - 7][self.round.dealer.get_hand_value() - 1] == "d" \
                    and self.first_move:
                # checks to see if the player should double according to basic strategy, and also if it is their first
                # move
                self.hand_list[hand].append(self.round.game.shoe.remove_card())
                # a card is removed from the shoe via the remove card method, this card is then appended to the hand
                # list attribute and the index of the hand being played
                self.last_move_list.append("double")
                # adds double to the last move list attribute
                return
                # exits the method

            elif self.get_hand_value(hand) > 16 or \
                    totals[self.get_hand_value(hand) - 7][self.round.dealer.get_hand_value() - 1] == "s":
                # checks to see if the player's hand value is over 16 or if basic strategy says they should stand
                self.last_move_list.append("stand")
                # adds stand to the last move list attribute
                return
                # exits the method

            else:
                self.first_move = False
                # makes first move False
                self.hit(hand)
                # runs the hit method

    def get_hand_names(self, hand):
        # defines the method get hand names
        return [i.get_name() for i in self.hand_list[hand]]
        # creates a for loop through the hand list at index hand, then for each element runs the get name method
        # from the Card class and adds them all to a list. This list is then returned

    def get_hand_value(self, hand):
        # defines a get hand value method
        return sum([i.get_value() for i in self.hand_list[hand]])
        # creates a for loop through the hand list at index hand, then for each element runs the get value method
        # from the Card class and add them all to a list. The sum of all the elements in this list is returned

    def get_hand_length(self, hand):
        # defines the get hand length method
        return len(self.hand_list[hand])
        # returns the length of the hand list attribute at index hand

    def splittable(self, hand):
        # defines the splittable method
        return self.hand_list[hand][0].same_name(self.hand_list[hand][1])
        # runs the same name method from the Card class with the card at index 0 and 1 of the
        # player's hand as parameters

    def check_card_counting_moves(self, hand):
        # defines the check card counting moves method
        for i in range(0, 15):
            # creates a for loop from 0 to 14, checking for each of the 15 deviations
            if int(illustrous_18[i][0]) == self.get_hand_value(hand) \
                    and int(illustrous_18[i][1]) == self.round.dealer.get_hand_value() \
                    and int(illustrous_18[i][2]) <= self.round.game.true_count and self.round.game.card_counting:
                # checks to see if in the row being looked at, column 1 is the same as the value of the player's hand,
                # column 2 is the value of the dealer's hand, column 3 is smaller than or equal to the true count and
                # that the attribute from Game card counting is True
                if illustrous_18[i][3] == "s":
                    # if all that is true, the value in column 4 is checked. This checks if it is s
                    self.last_move_list.append("stand")
                    # if it is s, stand is appended to the last move list attribute
                elif illustrous_18[i][3] == "d":
                    # this checks if the value in column 4 is d
                    self.hand_list[hand].append(self.round.game.shoe.remove_card())
                    # a card is removed from the shoe via the remove card method, this card is appended to the
                    # hand list at index hand
                    self.last_move_list.append("double")
                    # double is added to the last move list attribute
                return True
                # returns True if one of the rows fulfilled all the requirements. The method can now be exited as all
                # the other rows would not match if this one did so it saves time
        return False
        # returns False to tell the calculate move function to try other moves


class Dealer:
    # creates the class Dealer
    def __init__(self, round: Round):
        # defines the init method which initialises all the attributes when the class is instantiated
        self.round = round
        # creates an attribute called round
        self.hand = [self.round.game.shoe.remove_card()]
        # creates an attribute called hand that initially has the value of a card that was removed from the shoe
        # via the remove card method

    def get_hand_value(self):
        # defines the get hand value method
        return sum([i.get_value() for i in self.hand])
        # creates a for loop through the hand list at index hand, then for each element runs the get value method
        # from the Card class and add them all to a list. The sum of all the elements in this list is returned

    def get_card_value(self, index):
        # defines the get card value method
        return self.hand[index].get_value()
        # returns the value of the get value method

    def get_hand_names(self):
        # defines the get hand names method
        return [i.get_name() for i in self.hand]
        # creates a for loop through the hand list at index hand, then for each element runs the get name method
        # from the Card class and adds them all to a list. This list is then returned


class GUI:
    # creates a GUI class
    def __init__(self, master):
        # defines the init method which initialises all the attributes when the class is instantiated
        self.master = master
        # creates an attribute master which is the root window variable
        master.title("Blackjack Simulator")
        # gives a title to the window
        strategy = ["Basic Strategy", "Card Counting"]
        # defines a list strategy with 2 options, basic strategy or card counting
        five_card_win = ["Yes", "No"]
        # defines a list five card win with 2 options, yes or no
        blackjack_payout = ["3:2", "2:1", "6:5"]
        # defines a list blackjack payout with 3 options, 3:2, 2:1, 6:5. These are the most common blackjack payouts
        # you will find in casinos
        helv18 = font.Font(family="Helvetica", size=18)
        # defined a variable helv18 which is a preset font family and size combination that is used throughout the GUI
        helv20 = font.Font(family="Helvetica", size=20)
        # defined a variable helv20 which is a preset font family and size combination that is used for dropdown menus
        self.rounds_to_play_variable = StringVar()
        # creates an attribute round to play variable which is a StringVar
        self.decks_variable = StringVar()
        # creates an attribute decks variable which is a StringVar
        self.deck_penetration_variable = StringVar()
        # creates an attribute deck penetration variable which is a StringVar

        self.rounds_to_play_label = Label(master, text="Rounds", font=helv18)
        # creates an attribute round to play label which is a label. It is on the master window and has text Rounds
        # with the font helv18
        self.rounds_to_play_option = Entry(master, textvariable=self.rounds_to_play_variable, font=helv18)
        # creates a rounds to play option which is an entry box. It is on the master window and has the text that is
        # entered is set to the rounds to play variable attribute. The font is helv18
        self.rounds_to_play_label.place(x=5, y=0)
        # this places the round to play label at x coordinate 5 and y coordinate 0
        self.rounds_to_play_option.place(x=150, y=0)
        # this places the round to play entry box at x coordinate 150 and y coordinate 0

        self.decks_label = Label(master, text="Decks", font=helv18)
        # creates an attribute decks label which is a label. It is on the master window and has text Decks
        # with the font helv18
        self.decks_option = Entry(master, textvariable=self.decks_variable, font=helv18)
        # creates a decks option which is an entry box. It is on the master window and has the text that is
        # entered is set to the decks variable attribute. The font is helv18
        self.decks_label.place(x=5, y=75)
        # this places the decks label at x coordinate 5 and y coordinate 75
        self.decks_option.place(x=150, y=75)
        # this places the decks entry box at x coordinate 150 and y coordinate 75

        self.deck_penetration_label = Label(master, text="Shoe depth", font=helv18)
        # creates an attribute deck penetration label which is a label. It is on the master window and has text
        # Shoe depth with the font helv18
        self.deck_penetration_option = Entry(master, textvariable=self.deck_penetration_variable,
                                             font=helv18)
        # creates a deck penetration option which is an entry box. It is on the master window and has the text that is
        # entered is set to the deck penetration variable attribute. The font is helv18
        self.deck_penetration_label.place(x=5, y=150)
        # this places the deck penetration label at x coordinate 5 and y coordinate 150
        self.deck_penetration_option.place(x=150, y=150)
        # this places the deck penetration entry box at x coordinate 150 and y coordinate 150

        self.strategy_label = Label(master, text="Strategy", font=helv18)
        # creates an attribute strategy label which is a label. It is on the master window and has text Strategy
        # with the font helv18
        self.card_counting_variable = StringVar(master)
        # creates a card counting variable attribute which is a StringVar
        self.card_counting_variable.set(strategy[0])
        # this sets the default value of card counting variable as the first element in the list strategy
        self.card_counting_option = OptionMenu(master, self.card_counting_variable, *strategy)
        # creates an attribute called card counting option. This is an option menu. It is on the master window,
        # the variable is card counting variable and the options are all the elements in the list strategy
        self.card_counting_option.config(font=helv18)
        # this sets the font of the card counting option text to be helv18
        self.card_counting_menu = root.nametowidget(self.card_counting_option.menuname)
        # this creates an attribute called card counting menu.
        # This gives the code for the dropdown part of the dropdown menu
        self.card_counting_menu.config(font=helv20)
        # this sets the card counting menu attribute to have font helv20
        self.strategy_label.place(x=400, y=0)
        # this places the strategy label at x coordinate 400 and y coordinate 0
        self.card_counting_option.place(x=500, y=0)
        # this places the strategy dropdown menu at x coordinate 500 and y coordinate 0

        self.five_card_win_label = Label(master, text="5 card win", font=helv18)
        # creates an attribute five card win label which is a label. It is on the master window and has text 5 card win
        # with the font helv18
        self.five_card_win_variable = StringVar(master)
        # creates a five card win variable attribute which is a StringVar
        self.five_card_win_variable.set(five_card_win[0])
        # this sets the default value of five card win variable as the first element in the list five card win
        self.five_card_win_option = OptionMenu(master, self.five_card_win_variable, *five_card_win)
        # creates an attribute called five card win option. This is an option menu. It is on the master window,
        # the variable is five card win variable and the options are all the elements in the list five card win
        self.five_card_win_option.config(font=helv18)
        # this sets the font of the five card win option text to be helv18
        self.five_card_win_menu = root.nametowidget(self.five_card_win_option.menuname)
        # this creates an attribute called five card win menu.
        # This gives the code for the dropdown part of the dropdown menu
        self.five_card_win_menu.config(font=helv20)
        # this sets the five card win menu attribute to have font helv20
        self.five_card_win_label.place(x=400, y=75)
        # this places the five card win label at x coordinate 400 and y coordinate 75
        self.five_card_win_option.place(x=600, y=75)
        # this places the five card win dropdown menu at x coordinate 600 and y coordinate 75

        self.blackjack_payout_label = Label(master, text="Blackjack payout", font=helv18)
        # creates an attribute blackjack payout label which is a label. It is on the master window and has text
        # blackjack payout with the font helv18
        self.blackjack_payout_variable = StringVar(master)
        # creates a blackjack payout variable attribute which is a StringVar
        self.blackjack_payout_variable.set(blackjack_payout[0])
        # this sets the default value of blackjack payout variable as the first element in the list blackjack payout
        self.blackjack_payout_option = OptionMenu(master, self.blackjack_payout_variable, *blackjack_payout)
        # creates an attribute called blackjack payout option. This is an option menu. It is on the master window,
        # the variable is blackjack payout variable and the options are all the elements in the list blackjack payout
        self.blackjack_payout_option.config(font=helv18)
        # this sets the font of the blackjack payout option text to be helv18
        self.blackjack_payout_menu = root.nametowidget(self.blackjack_payout_option.menuname)
        # this creates an attribute called blackjack payout menu.
        # This gives the code for the dropdown part of the dropdown menu
        self.blackjack_payout_menu.config(font=helv20)
        # this sets the blackjack payout menu attribute to have font helv20
        self.blackjack_payout_label.place(x=400, y=150)
        # this places the blackjack payout label at x coordinate 400 and y coordinate 150
        self.blackjack_payout_option.place(x=600, y=150)
        # this places the blackjack payout dropdown menu at x coordinate 600 and y coordinate 150

        self.run_button = Button(master, text="Simulate", command=lambda: self.start_simulation(master, helv18)
                                 , font=helv18, height=5, width=12)
        # an attribute called run button is created. It is a button. It is on the master window, has text Simulate,
        # font helv18, height 5 and width 12. When you press it, it calls the method start simulation
        self.run_button.place(x=20, y=800)
        # this places the run button at x coordinate 20 and y coordinate 800

        self.close_button = Button(master, text="Close", command=master.quit, font=helv18, height=5, width=12)
        # an attribute called close button is created. It is a button. It is on the master window, has text Close,
        # font helv18, height 5 and width 12. When you press it, it calls the built-in method .quit which closes the
        # application
        self.close_button.place(x=270, y=800)
        # this places the close button at x coordinate 270 and y coordinate 800

        self.help_button = Button(master, text="Help", command=lambda: self.help(helv18),
                                  font=helv18, height=5, width=12)
        # an attribute called help button is created. It is a button. It is on the master window, has text Help,
        # font helv18, height 5 and width 12. When you press it, it calls the method help
        self.help_button.place(x=520, y=800)
        # this places the help button at x coordinate 520 and y coordinate 800

    def start_simulation(self, master, helv28):
        # defines the method start simulation
        if not (0 < self.deck_penetration_func() <= 1):
            # this is verifying that the deck penetration value is between 0 and 1
            return
            # if it is not, the function will break. This means that the user will need to correct the value for it to
            # run

        blackjack = Game(self.round_number_func(), self.number_of_decks_func(), self.deck_penetration_func(),
                         self.five_card_win_func(), self.blackjack_payout_func(), self.card_counting_func())
        # this creates an instance of the Game class called blackjack. Each parameter is the value of a function which
        # converts the user input into a form for the program to use
        blackjack.simulate()
        # this runs the simulate method in the Game class. From here the whole simulation is automated
        self.profit_graph(blackjack, master)
        # this calls the method profit graph to create and sketch the profit graph
        self.count_graph(blackjack, master)
        # this calls the method count graph to create and sketch the count graph
        self.output_info(blackjack, master, helv28)
        # this calls the method output info which prints on the GUI all relevant information the computer tracked
        # during the simulation

    def round_number_func(self):
        # defines the method round number func
        for i in range(0, len(self.rounds_to_play_variable.get())):
            if self.rounds_to_play_variable.get()[i] not in ["1", "2", "3", "4", "5", "6", "7", "8", "9", "0", ","]:
                # this is one of the many stages of validation. This checks if the rounds to play variable contains any
                # non-number or comma characters
                return 1
                # if there are any non-number or commas characters, it is set to only play 1 round

        for i in range(-1, -len(self.rounds_to_play_variable.get()) - 1, -1):
            # cycles through indexes -1 to -length of the round to play variable value
            if self.rounds_to_play_variable.get()[i] == "," and i % 4 != 0:
                # checks if a character in the rounds to play variable value is a comma and if it is in a valid spot
                # for a comma
                return 1
                # if a comma is in an invalid spot, 1 round is played

        return int(self.rounds_to_play_variable.get().replace(",", ""))
        # if the variable is a number, the rounds to play variable is set as rounding that number down
        # to the nearest integer

    def deck_penetration_func(self):
        # defines the method deck penetration func
        for i in self.deck_penetration_variable.get():
            if i not in ["1", "2", "3", "4", "5", "6", "7", "8", "9", "0", "."]:
                # another example of validation. This checks if the deck penetration variable contains any non-number
                # or dot characters
                return 1
                # if there are any non-number or dot characters, it is set to have a deck penetration of 1
        return float(self.deck_penetration_variable.get())
        # if the variable is a number, the deck penetration variable is set as the float version of
        # whatever number it is. At this stage all numbers are between 0 and 1 because of the validation earlier on

    def number_of_decks_func(self):
        # defines the method number of decks func
        for i in range(0, len(self.decks_variable.get())):
            if self.decks_variable.get()[i] not in ["1", "2", "3", "4", "5", "6", "7", "8", "9", "0", ","]:
                # this is one of the many stages of validation. This checks if the decks variable contains any
                # non-number or comma characters
                return 1
                # if there are any non-number or commas characters, it is set so that the shoe only contains 1 deck

        for i in range(-1, -len(self.decks_variable.get()) - 1, -1):
            # cycles through indexes -1 to -length of the decks variable value
            if self.decks_variable.get()[i] == "," and i % 4 != 0:
                # checks if a character in the decks variable value is a comma and if it is in a valid spot
                # for a comma
                return 1
                # if a comma is in an invalid spot, 1 deck is used in the shoe

        return int(self.decks_variable.get())
        # if the variable is a number, the number of decks variable is set as rounding the number down to the
        # nearset integer

    def card_counting_func(self):
        # defines the method card counting func
        if self.card_counting_variable.get() == "Basic Strategy":
            # checks to see if the value of the card counting variable is basic strategy
            return False
            # returns False if it is
        else:
            return True
            # this return True as it means the player wants to play with the card counting strategy

    def blackjack_payout_func(self):
        # defines the method blackjack payout func
        return int(self.blackjack_payout_variable.get()[0]) / int(self.blackjack_payout_variable.get()[2])
        # this takes the first number in the ratio and divides it by the second, making both integers. This value is
        # then returned

    def five_card_win_func(self):
        # defines the method five card win func
        if self.five_card_win_variable.get() == "Yes":
            # checks if the five card win variable value is yes
            return True
            # returns True if it is yes
        else:
            return False
            # return False otherwise

    def help(self, helv18):
        # defines the method help
        help_window = Toplevel(self.master)
        # creates another window called help window
        help_window.title("Help Window")
        # gives the window a title of Help Window
        help_window.geometry("1000x500")
        # defines the size of the window to be 1000 on the x-axis by 500 on the y-axis

        close_button = Button(help_window, text="Close", command=help_window.destroy)
        # a variable called close button is created. It is a button. It is on the help window, has text Close,
        # height 5 and width 12. When you press it, it calls the built-in method .destroy which closes the
        # window
        close_button.place(x=5, y=5)
        # this places the close button at x coordinate 5 and y coordinate 5

        text_box_input = Message(help_window, text="Input parameters\nRounds: This is the number of rounds to be"
                                                   " played. If it is anything that is not an integer, it is set to 1"
                                                   "\nDecks: This is the number of decks to be used in the shoe. If it "
                                                   "is anything that is not an integer, it is set to 1\nShoe Depth: "
                                                   "This is how far the shoe should be played into before being "
                                                   "remade. The value is 0 to 1, where 1 means the shoe is fully "
                                                   "played. The simulate button will not work if it is a number not "
                                                   "between 0 and 1. If it is not a number, it is set to be 1"
                                                   "\nStrategy: This has the options for the 2 ways of playing, "
                                                   "basic strategy or card counting which uses the high low system\n"
                                                   "5 card win: This is either yes or no and determines whether the "
                                                   "rule of if the player gets 5 cards and still is not bust they win "
                                                   "is being played\nBlackjack payout: This is where you can select one"
                                                   " of the 3 most common blackjack payout ratios in blackjack, "
                                                   "3:2, 6:5 or 2:1")
        # this creates a variable called text box input. It is a message. It is on the help window. The text describes
        # the meanings of all the input parameters that the user can customise
        text_box_input.place(x=50, y=20)
        # this places the text box input at x coordinate 50 and y coordinate 20

        text_box_output = Message(help_window, text="Output data\nHands won: This shows the total number of hands won"
                                                    " by the player\nHands drew: This shows the total number of hands"
                                                    " drew by the player\nHands lose: This shows the total number of"
                                                    " hands lost by the player\nHands blackjack: This shows the total"
                                                    " number of blackjacks achieved by the player\nHands "
                                                    "player>dealer: This shows the total number of times the player "
                                                    "got close to 21 than the dealer\nHands dealer bust: This shows "
                                                    "the total number of times the dealer went over 21\nHands "
                                                    "surrendered: This shows the total number of times the player "
                                                    "surrendered\nHands dealer>player: This shows the total number "
                                                    "of times the dealer was closer to 21 than the player\nHands "
                                                    "bust: This show the total number of times the player went over "
                                                    "21\nFinal profit: This shows the overall profit that the player"
                                                    " achieved throughout all the rounds")
        # this creates a variable called text box output. It is a message. It is on the help window. The text describes
        # the meanings of all the output that the user sees once the simulation is finished
        text_box_output.place(x=500, y=20)
        # this places the text box output at x coordinate 500 and y coordinate 20

        profit_graph_text = Label(help_window, text="Profit graph\nThis graph shows on the x axis the round number"
                                                    " and on the y axis the profit that the player has achieved at "
                                                    "that point in the game")
        # this creates a variable called profit graph text. It is a label. It is on the help window. The text
        # describes how to read the profit graph that is outputted on the screen once the simulation is finished
        profit_graph_text.place(x=160, y=300)
        # this places the profit graph text at x coordinate 160 and y coordinate 300

        count_graph_text = Label(help_window, text="Count graph\nThis graph shows on the x axis the round number"
                                                   " and on the y axis the true count at that point in the game")
        # this creates a variable called count graph text. It is a label. It is on the help window. The text
        # describes how to read the count graph that is outputted on the screen once the simulation is finished
        count_graph_text.place(x=220, y=400)
        # this places the count graph text at x coordinate 220 and y coordinate 400

    def profit_graph(self, blackjack, master):
        # defines a method profit graph
        data = pd.DataFrame({"Round": blackjack.rounds_played_list, "Profit": blackjack.profit_list})
        # using pandas, the data for the profit graph is formatted and given titles
        profit_graph = plt.Figure(figsize=(6.7, 4.7), dpi=100)
        # a variable profit graph is created which is a figure of matplotlib.pyplot
        # The figure size and dpi is specified
        ax1 = profit_graph.add_subplot(111)
        # a variable ax1 is defined
        line1 = FigureCanvasTkAgg(profit_graph, master)
        # line1 is defined using the FigureCanvasTkAgg package
        line1.get_tk_widget().place(x=820, y=10)
        # line1 is placed at x coordinate 820 y coordinate 10
        data = data[["Round", "Profit"]].groupby("Round").sum()
        # the data is grouped and formatted correctly
        data.plot(kind="line", legend=True, ax=ax1, color="r", fontsize=10)
        # the data is plotted, with other parameters like colour being defined
        ax1.set_title("Round vs Profit")
        # the title of Round vs Profit is set

    def count_graph(self, blackjack, master):
        # defines a method count graph
        data = pd.DataFrame({"Round": blackjack.rounds_played_list, "Count": blackjack.count_list})
        # using pandas, the data for the count graph is formatted and given titles
        count_graph = plt.Figure(figsize=(6.7, 4.7), dpi=100)
        # a variable profit graph is created which is a figure of matplotlib.pyplot
        ax1 = count_graph.add_subplot(111)
        # a variable ax1 is defined
        line1 = FigureCanvasTkAgg(count_graph, master)
        # line1 is defined using the FigureCanvasTkAgg package
        line1.get_tk_widget().place(x=820, y=510)
        # line1 is placed at x coordinate 820 y coordinate 510
        data = data[["Round", "Count"]].groupby("Round").sum()
        # the data is grouped and formatted correctly
        data.plot(kind="line", legend=True, ax=ax1, color="b", fontsize=10, linewidth=0.25)
        # the data is plotted, with other parameters like colour being defined
        ax1.set_title("Round vs Count")
        # the title of Round vs Profit is set

    def output_info(self, blackjack, master, helv28):
        # defines a method output info
        final_profit_label = Label(master, text=f"Final profit: {blackjack.profit}", font=helv28)
        # this creates a variable called final profit label. It is a label. It is on the master window.
        # The font is helv28. The text states the final profit of the simulation
        final_profit_label.place(x=270, y=710)
        # final profit label is placed at x coordinate 270 y coordinate 710

        hands_won_label = Label(master, text=f"Hands won: {blackjack.hands_won}", font=helv28)
        # this creates a variable called hands won label. It is a label. It is on the master window.
        # The font is helv28. The text states the number of hands the player won
        hands_won_label.place(x=5, y=275)
        # hands won label is placed at x coordinate 5 y coordinate 275

        hands_drew_label = Label(master, text=f"Hands drew: {blackjack.hands_drew}", font=helv28)
        # this creates a variable called hands drew label. It is a label. It is on the master window.
        # The font is helv28. The text states the number of hands the player drew with the dealer
        hands_drew_label.place(x=250, y=275)
        # hands drew label is placed at x coordinate 250 y coordinate 275

        hands_lost_label = Label(master, text=f"Hands lost: {blackjack.hands_lost}", font=helv28)
        # this creates a variable called hands lost label. It is a label. It is on the master window.
        # The font is helv28. The text states the number of hands the player lost
        hands_lost_label.place(x=500, y=275)
        # hands lost label is placed at x coordinate 500 y coordinate 275

        hands_surrendered_label = Label(master, text=f"Hands surrendered: {blackjack.hands_surrendered}", font=helv28)
        # this creates a variable called hands surrendered label. It is a label. It is on the master window.
        # The font is helv28. The text states the number of hands the player surrendered
        hands_surrendered_label.place(x=5, y=625)
        # hands surrendered label is placed at x coordinate 5 y coordinate 625

        hands_blackjack_label = Label(master, text=f"Hands blackjack: {blackjack.hands_blackjack}", font=helv28)
        # this creates a variable called hands blackjack label. It is a label. It is on the master window.
        # The font is helv28. The text states the number of hands the player got a blackjack
        hands_blackjack_label.place(x=5, y=450)
        # hands blackjack label is placed at x coordinate 5 y coordinate 450

        hands_bust_label = Label(master, text=f"Hands bust: {blackjack.hands_bust}", font=helv28)
        # this creates a variable called hands bust label. It is a label. It is on the master window.
        # The font is helv28. The text states the number of hands the player went bust
        hands_bust_label.place(x=590, y=625)
        # hands bust label is placed at x coordinate 590 y coordinate 625

        hands_player_beat_dealer_label = Label(master, text=f"Hands player>dealer: "
                                                            f"{blackjack.hands_player_beat_dealer}", font=helv28)
        # this creates a variable called hand player beat dealer label. It is a label. It is on the master window.
        # The font is helv28. The text states the number of hands the player got closer to 21 than the dealer
        hands_player_beat_dealer_label.place(x=250, y=450)
        # hands player beat dealer label is placed at x coordinate 250 y coordinate 450

        hands_dealer_beat_player_label = Label(master, text=f"Hands dealer>player: "
                                                            f"{blackjack.hands_dealer_beat_player}", font=helv28)
        # this creates a variable called hand dealer beat player label. It is a label. It is on the master window.
        # The font is helv28. The text states the number of hands the dealer got closer to 21 than the player
        hands_dealer_beat_player_label.place(x=280, y=625)
        # hands dealer beat player label is placed at x coordinate 280 y coordinate 625

        hands_dealer_bust_label = Label(master, text=f"Hands dealer bust: {blackjack.hands_dealer_bust}", font=helv28)
        # this creates a variable called hands dealer bust label. It is a label. It is on the master window.
        # The font is helv28. The text states the number of hands the dealer went bust
        hands_dealer_bust_label.place(x=540, y=450)
        # hands dealer bust label is placed at x coordinate 540 y coordinate 450


root = Tk()
# creates the root window
root.geometry("1500x1000")
# defines the size of the window - 1500 on the x-axis, 1000 on the y-axis
gui = GUI(root)
# creates an instance of the class GUI
root.mainloop()
# creates the mainloop that continuously runs
