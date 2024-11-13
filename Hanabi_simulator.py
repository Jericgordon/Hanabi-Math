import random #used for shuffling the deck
import copy #used for makeing a copy of a the deck to shuffle
from termcolor import colored #used for printing Hanabi boards in readable output
import bisect #used for inserting into a sorted list
import unittest #testing


def main():
    games = 100000
    wins = 0
    h = Hanabi_game(5,False)

    for _ in range(games):
        if h.play_game():
            wins += 1

    print(f"{wins} out of {games} games were won. A win rate of {wins/games}")



class Hanabi_game():
    def __init__(self,colors:int,print_lost_games) -> None:
        #user preferences
        self.print_lost_games = print_lost_games
        self.debug = False
        self.colors = colors

        #built in options
        self.color_order ={0:"red",1:'yellow',2:'green',3:'blue',4:'white',5:'magenta'}
        self.discards_reference = {x:0 for x in range(1,(self.colors * 5) + 1)}
        self.play_base_reference = [x for x in range(0,(self.colors) * 5,5)]
        self.deck_reference = self._make_deck(colors)

        

    def _setup_new_game(self):
        self.discards = copy.deepcopy(self.discards_reference)
        self.play_base = copy.deepcopy(self.play_base_reference)
        self.hand = []
        #shuffle a new deck
        self.deck = copy.deepcopy(self.deck_reference)
        random.shuffle(self.deck)
        for _ in range(10):
            self.hand.append(self.deck.pop())

    #A unique card is card (color_number * 5) + card_number
    #e.g. if blue is 2, the blue one is (2 * 5) + 2 or 12
    def _make_deck(self,colors) -> list:
        deck = []
        for color in range(colors):
            #Add ones
            for _ in range(3):
                deck.append((color * 5) + 1)
            #Add 2-4
            for card_number in range(2,5):
                for _ in range(2):
                    deck.append((color * 5) + card_number)
            #Add 5s
            deck.append((color * 5) + 5)
        return deck
        
    def play_game(self) -> int:
        self._setup_new_game()
        while len(self.deck) > 0:
            played = False
            could_discard = [] #stores hand position of the card   [0,5]
            index_reference = {} #stores the value of the card indexed by hand position
                                # {0:15,}
            #go through the hand; play any playable card; keep track of other cards
            for index in range(10):
                if self._is_playable(self.hand[index]):
                    self._(self.hand[index])
                    #print(f"Played {hand[index]} on {play_base}")
                    self.hand[index] = self.deck.pop() #Draw a new card. This version does not have hand order
                    played = True
                    break #stop going through the hand

                if not self._is_essential(self.hand[index]):
                    bisect.insort(could_discard,self.hand[index])
                    index_reference[self.hand[index]] = index

            #check to see if we've already played a card
            if played == True:
                continue 

            elif (played == False) and (len(could_discard) > 0):
                card = could_discard[-1]
                hand_index = index_reference[card]
                self.hand[hand_index] = self.deck.pop()
                self.discards[card] += 1
                continue
            
            else:
                #debugging printing 
                if self.print_lost_games:
                    print("Game lost")
                    self.print_visual_hand()
                    self.print_visual_play_base()
                    self.print_visual_discard()
                
                if self.debug:
                    print(f"hand: {self.hand}")
                    print(f"Play base {self.play_base}")
                    print(f"Discards: {self.discards}")

                return False
        return True
    
    #helper functions for the game
    def _is_essential(self,card:int) -> bool:
        if ((card % 5) == 0):
            return True
        
        if (self.play_base[(card - 1) // 5] >= card):
            return False
        
        #we don't need to worry about the fact that there are 3 ones in the deck for the following,
        #because they're alwayas playable or discardable. They'll either be caught by the above expression
        #or be directly played. This would not be the case if there were 3 ones
        if (self.discards[card] == 1):
            return True
        return False

    def _is_playable(self,card:int):
        color = (card-1) // 5
        if self.play_base[color] == (card - 1):
            return True
        return False
    
    def _play_card(self,card:int):
        self.play_base[(card - 1)//5] += 1

    def print_visual_play_base(self):
        print("Play Base: ",end="")
        for index in range(self.colors):
            card = self.play_base[index]
            color = self.color_order[index]
            if card == self.play_base_reference[index]:
                number = 0
            else:
                number = ((card -1 ) % 5) + 1
            print(colored(number,color) + " ",end="")
        print("")

    def print_visual_hand(self):
        self.hand.sort()
        print("hand: ",end="")
        for card in self.hand:
            color = self.color_order[(card -1)//5]
            number = card % 5
            if number == 0:
                number = 5
            print(colored(number,color) + " ",end="")
        print("")
    
    def print_visual_discard(self):
        print("Discards: ",end="")
        for card in self.discards_reference:
            if self.discards[card] > 0:
                color = self.color_order[(card -1) // 5]
                number = card % 5
                if number == 0:
                    number == 5
                print(colored(number,color) + " ",end="")
        print("")


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
        h6 = Hanabi_game(6)
        h5.play_base = [0,5,10,15,20]
        h5._(16)
        expected = [0,5,10,16,20]
        self.assertEqual(expected,h5.play_base)
        h5._(21)
        expected = [0,5,10,16,21]
        self.assertEqual(expected,h5.play_base)






if __name__ == "__main__":
    #unittest.main()
    main()  

