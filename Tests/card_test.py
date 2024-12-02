from Card import Hanabi_card
import unittest

class Hanabi_card_tests(unittest.TestCase):

    def test_get_number(self):
        card_number = 1
        for base_card_number in range(1,30):
            h = Hanabi_card(base_card_number)
            h._number_known = True
            self.assertEqual(card_number,h.get_number())
            if card_number == 5: #
                card_number = 1
            else:
                card_number += 1
    
    def test_get_color(self):
        color = 0
        h = Hanabi_card(5)
        h._color_known = True
        self.assertEqual(0,h.get_color())

    def test_clue(self):
        h = Hanabi_card(5)
        h.clue("number",5)
        self.assertEqual(5,h.get_number())
        h.clue("color",0)
        self.assertEqual(0,h.get_color())

        h = Hanabi_card(19)
        h.clue("number",4)
        h.clue("color",3)
        self.assertEqual(4,h.get_number())
        self.assertEqual(3,h.get_color())

