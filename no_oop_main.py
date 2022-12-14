import random
import csv
import time
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('TkAgg')

start = time.time()
totals_csv = open('Hard totals.csv', 'r')
reader = csv.reader(totals_csv)
totals = []
for row in reader:
    totals.append(row)
totals_csv.close()


def create_shoe(num_of_decks):
    shoe = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "jack", "queen", "king", "ace"] * 4 * num_of_decks
    random.shuffle(shoe)
    return shoe


def return_value_of_card(card):
    values = {"2": 2, "3": 3, "4": 4, "5": 5, "6": 6, "7": 7, "8": 8, "9": 9,
              "10": 10, "jack": 10, "queen": 10, "king": 10, "ace": 11}
    return values[card]


def return_value_of_hand(hand):
    values = {"2": 2, "3": 3, "4": 4, "5": 5, "6": 6, "7": 7, "8": 8, "9": 9,
              "10": 10, "jack": 10, "queen": 10, "king": 10, "ace": 11}
    return sum([values[card] for card in hand])


def same_card(card1, card2):
    return card1 == card2


def deal_player_cards(shoe):
    player_hand = [shoe.pop(0), shoe.pop(0)]
    return player_hand


def deal_dealer_cards(shoe):
    dealer_hand = [shoe.pop(0)]
    return dealer_hand


def create_bet():
    bet = 1
    return bet


def do_moves(player_hand, dealer_hand, shoe, totals, bet, five_card_win, first_move):
    while True:
        if return_value_of_hand(player_hand) == 21 and first_move:
            blackjack_win(bet)
            print(player_hand, dealer_hand)
            return bet * 1.5

        elif return_value_of_hand(player_hand) > 21:
            lose(bet)
            print(player_hand, dealer_hand)
            return -bet

        elif return_value_of_hand(player_hand) == 21:
            win(bet)
            print(player_hand, dealer_hand)
            return bet

        elif len(player_hand) > 4 and five_card_win:
            win(bet)
            print(player_hand, dealer_hand)
            return bet

        elif ((return_value_of_hand(player_hand) == 16 and return_value_of_hand(
                dealer_hand) > 8) or (
                      return_value_of_hand(player_hand) == 15 and return_value_of_hand(dealer_hand) == 10)) \
                and first_move:
            surrender(bet)
            print(player_hand, dealer_hand)
            return bet * -0.5

        elif same_card(player_hand[0], player_hand[1]) and totals[return_value_of_card(player_hand[0]) + 16][
            return_value_of_card(dealer_hand[0]) - 1] == "y" and first_move:
            first_move = False
            split(bet, player_hand, dealer_hand, shoe, five_card_win, totals)

        elif return_value_of_hand(player_hand) > 16:
            return stand(player_hand, dealer_hand, shoe, bet)

        elif return_value_of_hand(player_hand) < 9:
            first_move = False
            player_hand.append(shoe.pop(0))
        else:
            move = totals[return_value_of_hand(player_hand) - 7][return_value_of_card(dealer_hand[0]) - 1]
            if move == "d" and first_move:
                return double(player_hand, dealer_hand, shoe, bet)
            elif move == "s":
                return stand(player_hand, dealer_hand, shoe, bet)
            else:
                first_move = False
                player_hand.append(shoe.pop(0))


def blackjack_win(bet):
    print("blackjack")


def win(bet):
    print("win")
    # return bet


def lose(bet):
    print("lose")
    # return -bet


def draw(bet):
    print("draw")


def surrender(bet):
    print("surrender")


def split(bet, player_hand, dealer_hand, shoe, five_card_win, totals):
    print("split")
    player_hand_2 = [player_hand.pop(0), shoe.pop(0)]
    player_hand.append(shoe.pop(0))
    do_moves(player_hand_2, dealer_hand, shoe, totals, bet, five_card_win, first_move=False)


def stand(player_hand, dealer_hand, shoe, bet):
    while return_value_of_hand(dealer_hand) < 17:
        dealer_hand.append(shoe.pop(0))

    if return_value_of_hand(dealer_hand) > 21:
        win(bet)
        print(player_hand, dealer_hand)
        return bet

    elif return_value_of_hand(dealer_hand) > return_value_of_hand(player_hand):
        lose(bet)
        print(player_hand, dealer_hand)
        return -bet

    elif return_value_of_hand(dealer_hand) < return_value_of_hand(player_hand):
        win(bet)
        print(player_hand, dealer_hand)
        return bet

    else:
        draw(bet)
        print(player_hand, dealer_hand)
        return 0


def double(player_hand, dealer_hand, shoe, bet):
    bet *= 2
    player_hand.append(shoe.pop(0))
    return stand(player_hand, dealer_hand, shoe, bet)


def blackjack(shoe, totals, five_card_win):
    bet = 1
    player_hand = deal_player_cards(shoe)

    dealer_hand = deal_dealer_cards(shoe)

    return do_moves(player_hand, dealer_hand, shoe, totals, bet, five_card_win, first_move=True)


def main(num_of_decks, deck_penetration, rounds_to_play, five_card_win):
    rounds_played = 0
    rounds = []
    net_profit = 0
    profits = []
    while rounds_played < rounds_to_play:
        shoe = create_shoe(num_of_decks)
        while len(shoe) / (num_of_decks * 52) > deck_penetration:
            net_profit += blackjack(shoe, totals, five_card_win)
            profits.append(net_profit)
            rounds_played += 1
            rounds.append(rounds_played)
    print(rounds_played, net_profit)
    print(len(rounds), len(profits))
    print(profits)
    print(rounds)
    x = rounds
    y = profits
    plt.plot(x, y)
    plt.title("Profit graph")
    plt.show()


main(8, 0.5, 100000, True)
print(time.time() - start)
