import random
import csv
import time

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


def do_moves(player_hand, dealer_hand, shoe, totals, bet, first_move):
    print(player_hand, dealer_hand)
    if return_value_of_hand(player_hand) == 21 and first_move:
        blackjack_win()

    elif return_value_of_hand(player_hand) > 21:
        lose()

    elif len(player_hand) > 4:
        win()

    elif return_value_of_hand(player_hand) == 16 and return_value_of_hand(
            dealer_hand) > 8 or return_value_of_hand(player_hand) == 15 and return_value_of_hand(dealer_hand) == 15 and \
            first_move:
        surrender()

    elif same_card(player_hand[0], player_hand[1]) and totals[return_value_of_card(player_hand[0]) + 16][
        return_value_of_card(dealer_hand[0]) - 1] == "y" and first_move:
        first_move = False
        split(player_hand, dealer_hand)

    elif return_value_of_hand(player_hand) > 16:
        stand(player_hand, dealer_hand, shoe, bet)

    elif return_value_of_hand(player_hand) < 9:
        first_move = False
        hit(player_hand, dealer_hand, shoe, totals, bet, first_move)

    else:
        move = totals[return_value_of_hand(player_hand) - 7][return_value_of_card(dealer_hand[0]) - 1]
        if move == "d" and first_move:
            first_move = False
            double(player_hand, dealer_hand, shoe, bet)
        elif move == "s":
            stand(player_hand, dealer_hand, shoe, bet)
        else:
            first_move = False
            hit(player_hand, dealer_hand, shoe, totals, bet, first_move)


def blackjack_win():
    print("blackjack")


def win():
    print("win")


def lose():
    print("lose")


def draw():
    print("draw")


def surrender():
    print("surrender")


def split(player_hand, dealer_hand):
    player_hand_2 = [player_hand.pop(0)]
    return player_hand_2, player_hand


def stand(player_hand, dealer_hand, shoe, bet):
    while return_value_of_hand(dealer_hand) < 17:
        dealer_hand.append(shoe.pop(0))

    if return_value_of_hand(dealer_hand) > 21:
        win()

    elif return_value_of_hand(dealer_hand) > return_value_of_hand(player_hand):
        lose()

    elif return_value_of_hand(dealer_hand) < return_value_of_hand(player_hand):
        win()

    else:
        draw()


def double(player_hand, dealer_hand, shoe, bet):
    bet *= 2
    player_hand.append(shoe.pop(0))
    stand(player_hand, dealer_hand, shoe, bet)


def hit(player_hand, dealer_hand, shoe, totals, bet, first_move):
    player_hand.append(shoe.pop(0))
    do_moves(player_hand, dealer_hand, shoe, totals, bet, first_move)


def blackjack(shoe, totals):
    bet = create_bet()
    player_hand = deal_player_cards(shoe)

    dealer_hand = deal_dealer_cards(shoe)

    do_moves(player_hand, dealer_hand, shoe, totals, bet, first_move=True)


def main(num_of_decks, deck_penetration, rounds_to_play):
    rounds_played = 0
    while rounds_played < rounds_to_play:
        shoe = create_shoe(num_of_decks)
        while len(shoe) / (num_of_decks * 52) > deck_penetration:
            blackjack(shoe, totals)
            rounds_played += 1


main(8, 0.5, 500000)
print(time.time() - start)
