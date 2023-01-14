import csv
import random
import math
from tkinter import font, Tk, Canvas, Button, Label, OptionMenu, Entry, StringVar
#from tkinter import *
import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

totals_csv = open('Hard totals.csv', 'r')
reader = csv.reader(totals_csv)
totals = []
for row in reader:
    totals.append(row)
totals_csv.close()

illustrous_18_csv = open('illustrous_18.csv', 'r')
reader = csv.reader(illustrous_18_csv)
illustrous_18 = []
for row in reader:
    illustrous_18.append(row)
illustrous_18_csv.close()

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
    def __init__(self, num_of_decks, game):
        self.num_of_decks = num_of_decks
        self.game = game
        names = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "jack", "queen", "king", "ace"]
        self.count_value = {"2": 1, "3": 1, "4": 1, "5": 1, "6": 1, "7": 0, "8": 0, "9": 0,
                       "10": -1, "jack": -1, "queen": -1, "king": -1, "ace": -1}
        self.deck = []
        for k in range(0, self.num_of_decks):
            for i in range(0, 4):
                for j in names:
                    self.deck.append(Card(j))
        random.shuffle(self.deck)
        self.game.running_count = 0
        self.game.true_count = 0

    def remove_card(self):
        card = self.deck.pop()
        self.game.running_count += self.count_value[card.get_name()]
        self.game.true_count = self.game.running_count / (math.ceil(self.get_length_of_shoe() / 52))
        return card

    def get_length_of_shoe(self):
        return len(self.deck)


class Game:
    def __init__(self, rounds_to_play, num_of_decks, deck_penetration, five_card_win, blackjack_payout, card_counting):
        self.profit = 0
        self.profit_list = []
        self.count_list = []
        self.rounds_to_play = rounds_to_play
        self.rounds_played = 0
        self.rounds_played_list = []
        self.shoe = Shoe(num_of_decks, self)
        self.num_of_decks = num_of_decks
        self.deck_penetration = deck_penetration
        self.five_card_win = five_card_win
        self.blackjack_payout = blackjack_payout
        self.card_counting = card_counting
        self.running_count = 0
        self.true_count = self.running_count//(math.ceil(self.shoe.get_length_of_shoe()/52))
        self.hands_won = 0
        self.hands_drew = 0
        self.hands_lost = 0
        self.hands_surrendered = 0
        self.hands_blackjack = 0
        self.hands_21 = 0
        self.hands_bust = 0
        self.hands_player_beat_dealer = 0
        self.hands_dealer_beat_player = 0
        self.hands_dealer_bust = 0

    def simulate(self):
        while self.rounds_played < self.rounds_to_play:
            self.shoe = Shoe(self.num_of_decks, self)
            while self.rounds_played < self.rounds_to_play and self.shoe.get_length_of_shoe() > self.num_of_decks * 52 \
                    * (1 - self.deck_penetration):
                if self.shoe.get_length_of_shoe() < 15:
                    self.shoe = Shoe(self.num_of_decks, self)
                one_round = Round(self)
                self.profit += one_round.determine_profit()
                self.profit_list.append(self.profit)
                self.count_list.append(self.true_count)
                self.rounds_played += 1
                self.rounds_played_list.append(self.rounds_played)
                self.hands_won += one_round.player.hand_status.count("w") + one_round.player.hand_status.count("b")
                self.hands_lost += one_round.player.hand_status.count("l") + one_round.player.hand_status.count("s")
                self.hands_drew += one_round.player.hand_status.count("d")
                self.hands_surrendered += one_round.player.hand_status.count("s")
                self.hands_blackjack += one_round.player.hand_status.count("b")
                self.hands_21 += one_round.player.hand_status.count("21")
                self.hands_bust += one_round.player.hand_status.count("bust")
                self.hands_player_beat_dealer += one_round.player.hand_status.count("player>dealer")
                self.hands_dealer_beat_player += one_round.player.hand_status.count("dealer>player")
                self.hands_dealer_bust += one_round.player.hand_status.count("dealer_bust")

class Round:
    def __init__(self, game: Game):
        self.game = game
        self.finished = False
        self.hands_played = 0
        self.bet_calc = self.calculate_bet()
        self.player = Player(self, self.bet_calc)
        self.dealer = Dealer(self)
        self.dealer_hand_value = self.dealer.get_hand_value()
        self.player.deal_hand()

        while not self.finished:
            self.player.bet = self.bet_calc
            self.player.calculate_move(self.hands_played)
            self.hands_played += 1
            if self.hands_played == len(self.player.hand_list):
                self.finished = True

        if "stand" in self.player.last_move_list or "double" in self.player.last_move_list:
            self.deal_dealer_cards()

        self.determine_winner()

        #for i in range(0, len(self.player.hand_list)):
            #print(f"Player hand: {self.player.get_hand_names(i)}")
        #print(f"Dealer hand:{self.dealer.get_hand_names()}")
        #print(f"Profit list: {self.player.profit_list_of_hands}\n")

    def calculate_bet(self):
        if not self.game.card_counting or self.game.true_count <= 0:
            return 1
        return int(self.game.true_count)


    def determine_profit(self):
        return sum(self.player.profit_list_of_hands)

    def deal_dealer_cards(self):
        if self.dealer.get_card_value(-1) == 11:
            aces = 1
        else:
            aces = 0
        while self.dealer_hand_value < 17:
            self.dealer.hand.append(self.game.shoe.remove_card())
            if self.dealer.get_card_value(-1) == 11:
                aces += 1
            if aces > 1:
                self.dealer_hand_value = self.dealer.get_hand_value() - 10 * (aces -1)
            else:
                self.dealer_hand_value = self.dealer.get_hand_value()

            if self.dealer.get_hand_value() > 21 and aces > 0:
                self.dealer_hand_value = self.dealer.get_hand_value() - 10 * aces
        #print(self.dealer_hand_value)





    def determine_winner(self):
        for hand_num in range(0,len(self.player.hand_list)):
            if self.player.last_move_list[hand_num] == "blackjack":
                self.player.blackjack_win()
            elif self.player.last_move_list[hand_num] == "bust":
                self.player.lose(False)
                self.player.hand_status.append("bust")
            elif self.player.last_move_list[hand_num] == "21":
                self.player.win(False)
                self.player.hand_status.append("21")
            elif self.player.last_move_list[hand_num] == "surrender":
                self.player.surrender()
            elif self.player.last_move_list[hand_num] == "double":
                self.compare_to_dealer(hand_num, True)
            else:
                self.compare_to_dealer(hand_num, False)
    def compare_to_dealer(self, hand_num, double):
        if self.player.get_hand_value(hand_num) == 21:
            self.player.win(double)
            self.player.hand_status.append("21")
        elif self.dealer.get_hand_value() > 21:
            self.player.win(double)
            self.player.hand_status.append("dealer_bust")
        elif self.dealer.get_hand_value() < self.player.get_hand_value(hand_num):
            self.player.win(double)
            self.player.hand_status.append("player>dealer")
        elif self.dealer.get_hand_value() > self.player.get_hand_value(hand_num):
            self.player.lose(double)
            self.player.hand_status.append("dealer>player")
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
        self.hand_status = []

    def deal_hand(self):
        self.hand_list.append([self.round.game.shoe.remove_card(), self.round.game.shoe.remove_card()])

    def deal_hand_split(self, hand):
        self.hand_list.append([self.hand_list[hand][0], self.round.game.shoe.remove_card()])
        self.hand_list[hand] = [self.hand_list[hand][0], self.round.game.shoe.remove_card()]

    def win(self, double):
        if double:
            self.profit_list_of_hands.append(self.bet * 2)
        else:
            self.profit_list_of_hands.append(self.bet)
        self.hand_status.append("w")


    def lose(self, double):
        if double:
            self.profit_list_of_hands.append(-self.bet * 2)
        else:
            self.profit_list_of_hands.append(-self.bet)
        self.hand_status.append("l")


    def draw(self):
        self.profit_list_of_hands.append(0)
        self.hand_status.append("d")

    def blackjack_win(self):
        self.profit_list_of_hands.append(self.bet * self.round.game.blackjack_payout)
        self.hand_status.append("b")


    def surrender(self):
        self.profit_list_of_hands.append(-self.bet * 0.5)
        self.hand_status.append("s")


    def split(self, hand):
        self.deal_hand_split(hand)

    def hit(self, hand):
        self.hand_list[hand].append(self.round.game.shoe.remove_card())

    def calculate_move(self, hand):
        self.first_move = True
        while True:
            if self.check_card_counting_moves(hand):
                return

            elif self.get_hand_value(hand) == 21 and self.first_move:
                #print("blackjack", self.get_hand_names(hand), self.round.dealer.get_hand_names())
                self.last_move_list.append("blackjack")
                return

            elif self.get_hand_value(hand) > 21:
                #print("lose", self.get_hand_names(hand), self.round.dealer.get_hand_names())
                self.last_move_list.append("bust")
                return

            elif (self.get_hand_value(hand) == 21) or \
                    (self.get_hand_length(hand) > 4 and self.round.game.five_card_win):
                #print("win", self.get_hand_names(hand), self.round.dealer.get_hand_names())
                self.last_move_list.append("21")
                return

            elif self.get_hand_value(hand) > 16:
                #print("stand", self.get_hand_names(hand), self.round.dealer.get_hand_names())
                self.last_move_list.append("stand")
                return

            elif ((self.get_hand_value(hand) == 16 and self.round.dealer.get_hand_value() > 8) or
                  (self.get_hand_value(hand) == 15 and self.round.dealer.get_hand_value() == 10)) and self.first_move:
                #print("surrender", self.get_hand_names(hand), self.round.dealer.get_hand_names())
                self.last_move_list.append("surrender")
                return

            elif self.splittable(hand) and totals[self.hand_list[hand][0].get_value() + 16]\
                [self.round.dealer.get_hand_value() -1] == "y":
                #print("split", self.get_hand_names(hand), self.round.dealer.get_hand_names())
                self.split(hand)


            elif totals[self.get_hand_value(hand) - 7][self.round.dealer.get_hand_value() - 1] == "d"\
                    and self.first_move:
                #print("double", self.get_hand_names(hand), self.round.dealer.get_hand_names())
                self.hand_list[hand].append(self.round.game.shoe.remove_card())
                self.last_move_list.append("double")
                return

            elif self.get_hand_value(hand) > 16 or \
                    totals[self.get_hand_value(hand) - 7][self.round.dealer.get_hand_value() - 1] == "s":
                #print("stand", self.get_hand_names(hand), self.round.dealer.get_hand_names())
                self.last_move_list.append("stand")
                return

            else:
                self.first_move = False
                #print("hit", self.get_hand_names(hand), self.round.dealer.get_hand_names())
                self.hit(hand)


    def get_hand_names(self, hand):
        return [i.get_name() for i in self.hand_list[hand]]

    def get_hand_value(self, hand):
        return sum([i.get_value() for i in self.hand_list[hand]])

    def get_hand_length(self, hand):
        return len(self.hand_list[hand])

    def splittable(self, hand):
        return self.hand_list[hand][0].same_name(self.hand_list[hand][1])

    def check_card_counting_moves(self, hand):
        for i in range(0, 15):
            if int(illustrous_18[i][0]) == self.get_hand_value(hand)\
                and int(illustrous_18[i][1]) == self.round.dealer.get_hand_value() \
                and int(illustrous_18[i][2]) <= self.round.game.true_count and self.round.game.card_counting:
                if illustrous_18[i][3] == "s":
                    #print("stand", self.get_hand_names(hand), self.round.dealer.get_hand_names())
                    self.last_move_list.append("stand")
                elif illustrous_18[i][3] == "d":
                    #print("double", self.get_hand_names(hand), self.round.dealer.get_hand_names())
                    self.hand_list[hand].append(self.round.game.shoe.remove_card())
                    self.last_move_list.append("double")
                #print(self.get_hand_names(hand), self.round.dealer.get_hand_names(), self.round.game.running_count, self.round.game.true_count, self.round.game.shoe.get_length_of_shoe()/52)
                return True
        return False




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


class GUI:

    def __init__(self, master):
        self.master = master
        master.title("Blackjack Simulator")
        strategy = ["Basic Strategy", "Card Counting"]
        five_card_win = ["Yes", "No"]
        blackjack_payout = ["3:2", "2:1", "6:5"]
        helv18 = font.Font(family = "Helvetica", size = 18)
        helv20 = font.Font(family = "Helvetica", size = 20)
        self.rounds_to_play_variable = StringVar()
        self.decks_variable = StringVar()
        self.deck_penetration_variable = StringVar()
        """self.canvas = Canvas(self.master)

        self.canvas.create_line(750, 0, 750, 1000)
        self.canvas.place()"""

        self.rounds_to_play_label = Label(master, text = "Rounds", font = helv18)
        self.rounds_to_play_option = Entry(master, textvariable= self.rounds_to_play_variable, font = helv18)
        self.rounds_to_play_label.place(x = 5, y = 0)
        self.rounds_to_play_option.place(x = 150, y = 0)

        self.decks_label = Label(master, text = "Decks", font = helv18)
        self.decks_option = Entry(master, textvariable = self.decks_variable, font = helv18)
        self.decks_label.place(x = 5, y = 75)
        self.decks_option.place(x = 150, y = 75)

        self.deck_penetration_label = Label(master, text = "Shoe depth", font = helv18)
        self.deck_penetration_option = Entry(master, textvariable = self.deck_penetration_variable,
                                             font = helv18)
        self.deck_penetration_label.place(x = 5, y = 150)
        self.deck_penetration_option.place(x = 150, y = 150)

        self.strategy_label = Label(master, text = "Strategy", font = helv18)
        self.card_counting_variable = StringVar(master)
        self.card_counting_variable.set(strategy[0])
        self.card_counting_option = OptionMenu(master, self.card_counting_variable, *strategy)
        self.card_counting_option.config(font = helv18)
        self.card_counting_menu = root.nametowidget(self.card_counting_option.menuname)
        self.card_counting_menu.config(font = helv20)
        self.strategy_label.place(x = 400, y = 0)
        self.card_counting_option.place(x = 500, y = 0)

        self.five_card_win_label = Label(master, text = "5 card win", font = helv18)
        self.five_card_win_variable = StringVar(master)
        self.five_card_win_variable.set(five_card_win[0])
        self.five_card_win_option = OptionMenu(master, self.five_card_win_variable, *five_card_win)
        self.five_card_win_option.config(font = helv18)
        self.five_card_win_menu = root.nametowidget(self.five_card_win_option.menuname)
        self.five_card_win_menu.config(font=helv20)
        self.five_card_win_label.place(x = 400, y = 75)
        self.five_card_win_option.place(x = 600, y = 75)

        self.blackjack_payout_label = Label(master, text = "Blackjack payout", font = helv18)
        self.blackjack_payout_variable = StringVar(master)
        self.blackjack_payout_variable.set(blackjack_payout[0])
        self.blackjack_payout_option = OptionMenu(master, self.blackjack_payout_variable, *blackjack_payout)
        self.blackjack_payout_option.config(font=helv18)
        self.blackjack_payout_menu = root.nametowidget(self.blackjack_payout_option.menuname)
        self.blackjack_payout_menu.config(font=helv20)
        self.blackjack_payout_label.place(x = 400, y = 150)
        self.blackjack_payout_option.place(x = 600, y = 150)

        self.run_button = Button(master, text = "Simulate", command = lambda: self.start_simulation(master, helv18)
                                 , font = helv18, height = 5, width = 12)
        self.run_button.place(x = 20, y = 800)

        self.close_button = Button(master, text = "Close", command = master.quit, font = helv18, height = 5, width = 12)
        self.close_button.place(x = 270, y = 800)

        self.help_button = Button(master, text = "Help", command = lambda: self.help(),
                                  font=helv18, height = 5, width = 12)
        self.help_button.place(x = 520, y = 800)


    def start_simulation(self, master, helv28):
        blackjack = Game(self.round_number_func(), self.number_of_decks_func(), self.deck_penetration_func(),
                         self.five_card_win_func(), self.blackjack_payout_func(), self.card_counting_func())
        #print(card_counting_variable, blackjack_payout_variable, five_card_win_variable)
        blackjack.simulate()
        self.profit_graph(blackjack, master)
        self.count_graph(blackjack, master)
        self.output_info(blackjack, master, helv28)

    def round_number_func(self):
        return int(self.rounds_to_play_variable.get())

    def deck_penetration_func(self):
        return float(self.deck_penetration_variable.get())

    def number_of_decks_func(self):
        return int(self.decks_variable.get())
    def card_counting_func(self):
        if self.card_counting_variable.get() == "Basic Strategy":
            return False
        else:
            return True

    def blackjack_payout_func(self):
        return int(self.blackjack_payout_variable.get()[0]) / int(self.blackjack_payout_variable.get()[2])

    def five_card_win_func(self):
        if self.five_card_win_variable.get() == "Yes":
            return True
        else:
            return False

    def help(self):
        pass
    def profit_graph(self, blackjack, master):
        data = pd.DataFrame({"Round": blackjack.rounds_played_list, "Profit": blackjack.profit_list})
        profit_graph = plt.Figure(figsize = (6.7, 4.7), dpi = 100)
        ax1 = profit_graph.add_subplot(111)
        line1 = FigureCanvasTkAgg(profit_graph, master)
        line1.get_tk_widget().place(x = 820, y = 10)
        data = data[["Round", "Profit"]].groupby("Round").sum()
        data.plot(kind = "line", legend = True, ax = ax1, color = "r", fontsize = 10)
        ax1.set_title("Round vs Profit")
    def count_graph(self, blackjack, master):
        data = pd.DataFrame({"Round": blackjack.rounds_played_list, "Count": blackjack.count_list})
        count_graph = plt.Figure(figsize= (6.7, 4.7), dpi=100)
        ax1 = count_graph.add_subplot(111)
        line1 = FigureCanvasTkAgg(count_graph, master)
        line1.get_tk_widget().place(x = 820, y = 510)
        data = data[["Round", "Count"]].groupby("Round").sum()
        data.plot(kind = "line", legend = True, ax = ax1, color = "b", fontsize = 10, linewidth = 0.25)
        ax1.set_title("Round vs Count")

    def output_info(self, blackjack, master, helv28):
        final_profit_label = Label(master, text = f"Final profit: {blackjack.profit}", font = helv28)
        final_profit_label.place(x = 270, y = 710)
        hands_won_label = Label(master, text = f"Hands won: {blackjack.hands_won}", font = helv28)
        hands_won_label.place(x = 5, y = 275)
        hands_drew_label = Label(master, text=f"Hands drew: {blackjack.hands_drew}", font=helv28)
        hands_drew_label.place(x = 250, y = 275)
        hands_lost_label = Label(master, text=f"Hands lost: {blackjack.hands_lost}", font=helv28)
        hands_lost_label.place(x = 500, y = 275)
        hands_surrendered_label = Label(master, text=f"Hands surrendered: {blackjack.hands_surrendered}", font=helv28)
        hands_surrendered_label.place(x = 5, y = 625)
        hands_blackjack_label = Label(master, text=f"Hands blackjack: {blackjack.hands_blackjack}", font=helv28)
        hands_blackjack_label.place(x = 5, y = 450)
        hands_21_label = Label(master, text=f"Hands reached 21: {blackjack.hands_21}", font=helv28)
        hands_21_label.place()
        hands_bust_label = Label(master, text=f"Hands bust: {blackjack.hands_bust}", font=helv28)
        hands_bust_label.place(x = 590, y = 625)
        hands_player_beat_dealer_label = Label(master, text=f"Hands player>dealer: "
                                                             f"{blackjack.hands_player_beat_dealer}", font=helv28)
        hands_player_beat_dealer_label.place(x = 250, y = 450)
        hands_dealer_beat_player_label = Label(master, text=f"Hands dealer>player: "
                                                            f"{blackjack.hands_dealer_beat_player}", font=helv28)
        hands_dealer_beat_player_label.place(x = 280, y = 625)
        hands_dealer_bust_label = Label(master, text=f"Hands dealer bust: {blackjack.hands_dealer_bust}", font=helv28)
        hands_dealer_bust_label.place(x = 540, y = 450)


root = Tk()
root.geometry("1500x1000")
canvas = Canvas(root)
canvas.create_line(750, 0, 750, 1000)
canvas.place()
gui = GUI(root)
root.mainloop()

