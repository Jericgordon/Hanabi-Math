from Hanabi_simulator import Hanabi_game
import unittest
from Card import Hanabi_card

class Hanabi_tests(unittest.TestCase):
    def test_is_playble_wrong_color(self):
        h5 = Hanabi_game(5)
        h5._setup_new_game()
        expected = [5,6,10,15,20]
        h5.play_base = [5,6,10,15,20]
        h5._play_card([Hanabi_card(6)],0)
        self.assertTrue(expected,[5,6,10,15,20])
        
    def test_play_card(self):
        h5 = Hanabi_game(5)
        h5._setup_new_game()
        h5.play_base = [0,5,10,15,20]
        h5._play_card([Hanabi_card(16)],0)
        expected = [0,5,10,16,20]
        self.assertEqual(expected,h5.play_base)
        h5._play_card([Hanabi_card(21)],0)
        expected = [0,5,10,16,21]
        self.assertEqual(expected,h5.play_base)