import pytest
import main as m


class TestCard:
    def test_get_value(self):
        names = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "jack", "queen", "king", "ace"]
        values = {"2": 2, "3": 3, "4": 4, "5": 5, "6": 6, "7": 7, "8": 8, "9": 9,
                  "10": 10, "jack": 10, "queen": 10, "king": 10, "ace": 11}
        for i in range(0, len(names)):
            card = m.Card(names[i])
            assert card.get_value() == list(values.values())[i]

    def test_same_value(self):
        names = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "jack", "queen", "king", "ace"]
        for i in range(0, len(names)):
            card = m.Card(names[i])
            other = m.Card(names[i])
            assert card.same_value(other) is True

    def test_get_name(self):
        names = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "jack", "queen", "king", "ace"]
        values = {"2": 2, "3": 3, "4": 4, "5": 5, "6": 6, "7": 7, "8": 8, "9": 9,
                  "10": 10, "jack": 10, "queen": 10, "king": 10, "ace": 11}
        for i in range(0, len(names)):
            card = m.Card(names[i])
            assert card.get_name() == list(values)[i]


class TestShoe:
    def test_remove_card(self):
        for i in range(1, 11):
            shoe = m.Shoe(i)
            values_dict = {"2": 2, "3": 3, "4": 4, "5": 5, "6": 6, "7": 7, "8": 8, "9": 9,
                           "10": 10, "jack": 11, "queen": 12, "king": 13, "ace": 14}
            values = [["2", 2], ["3", 3], ["4", 4], ["5", 5], ["6", 6], ["7", 7], ["8", 8], ["9", 9], ["10", 10],
                      ["jack", 11], ["queen", 12], ["king", 13], ["ace", 14]]
            sum_of_shoe = sum([values[values_dict[j.get_name()] - 2][1] for j in shoe.deck])
            removed_card = shoe.remove_card()
            new_sum_of_shoe = sum([values[values_dict[j.get_name()] - 2][1] for j in shoe.deck])
            assert removed_card.get_name() == values[(sum_of_shoe - new_sum_of_shoe - 2)][0]

    def test_get_length_of_shoe(self):
        for i in range(0, 11):
            shoe = m.Shoe(i)
            assert shoe.get_length_of_shoe() == 52 * i
