from Hanabi_simulator import Hanabi_game
import unittest
from Card import Hanabi_card

class Hanabi_tests(unittest.TestCase):
    def test_is_playbable_empty_board(self):
        #test the normal case of playable cards on an empty board
        h5 = Hanabi_game(5)
        h5.play_base = [0,5,10,15,20]
        valid_plays = [1,6,11,16,21]
        invalid_plays = []
        for number in range(1,26):
            if number not in valid_plays:
                invalid_plays.append(number)
        for play in valid_plays:
            self.assertTrue(h5._is_playable(play))

        for play in invalid_plays:
            self.assertFalse(h5._is_playable(play))

    def test_is_playble_wrong_color(self):
        h5 = Hanabi_game(5)
        h5.play_base = [5,6,10,15,20]
        self.assertFalse(h5._is_playable(6))
        
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