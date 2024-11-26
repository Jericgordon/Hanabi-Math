import random #used for shuffling the deck
import copy #used for makeing a copy of a the deck to shuffle
from termcolor import colored #used for printing Hanabi boards in readable output
import bisect #used for inserting into a sorted list
from Card import Hanabi_card

class Hanabi_game():
    def __init__(self,colors:int) -> None:
        #user preferences
        self.print_lost_games = False
        self.debug = False
        self.colors = colors

        #built in options
        self.color_order ={0:"red",1:'yellow',2:'green',3:'blue',4:'white',5:'magenta'}
        self.discards_reference = {x:0 for x in range(1,(self.colors * 5) + 1)}
        self.play_base_reference = [x for x in range(0,(self.colors) * 5,5)]
        self.deck_reference = self._make_deck(colors)

    def print_lost_games(self):
        self.print_lost_games = True

    def _setup_new_game(self):
        self.discards = copy.deepcopy(self.discards_reference)
        self.play_base = copy.deepcopy(self.play_base_reference)
        self.hands = [[] for _ in range(2)]
        self.misfires = 0
        self.game_lost = False # Boolean to check if the game is lost
        self.clue_counter = 8
        #shuffle a new deck
        self.deck = copy.deepcopy(self.deck_reference)
        random.shuffle(self.deck)
        for _ in range(5):
            self.hands[0].append(Hanabi_card(self.deck.pop()))
            self.hands[1].append(Hanabi_card(self.deck.pop()))

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
        
    def play_game(self,strategy) -> bool:
        self._setup_new_game()
        self.players = []
        last_moves = 2
        turn = 0
        player = 0 #this gives us which hand to access when clueing this is the index of the current players hand. player + 1 % 2 is the index of the other
        s1 = strategy() #strategy for player 1
        s2 = strategy() #strategy for player 2
        while last_moves >= 0:
            if len(self.deck) == 0:
                last_moves -= 1 #this gives us exactly 2 turns after the deck depletes, which the rules require
            if self.debug:
                print(f"turn {turn}")
                print("")
                self.print_visual_discard()
                self.print_visual_play_base()
                self.print_visual_other_hand(self.hands[(player + 1) % 2])
                self.print_visual_my_hand(self.hands[player])
    
            if player == 0: #if it's player 
                move = s1.play_next_turn(self.hands[0],self.hands[1],self.discards,self.misfires,self.clue_counter) #player hand,other hand,discards
            if player == 1:
                move = s2.play_next_turn(self.hands[1],self.hands[0],self.discards,self.misfires,self.clue_counter)
            match move[0]:
                case "play":
                    self._play_card(self.hands[player],move[1])
                    break
                case "discard":
                    self._discard_card(self.hands[player],move[1])
                    self.clue_counter += 1 #we don't have logic that forbids discarding with + 8 clue tokens
                    break
                case "clue":
                    self.clue_counter -= 0
                    self._clue_hand(self.hands[player],move[1],move[2])
                case _:
                    raise ValueError("Invalid move given. Valid moves are play, clue, discard")
            
            turn += 1
            player = turn % 2 # This switches between players, as the only fixed relation in this game is between player and turn
        

    def _clue_hand(self,hand,clue_type,clue:int):
        for card in hand:
            card.clue(clue_type,clue)
        
        ...
    def _discard_card(self,hand,index:int):
        self.discards[hand[index].value] +=1 # we do store cards in the discard by their literal value, not by card                                              
        self._resplace_card(hand,index)

    def _is_playable(self,card:Hanabi_card):
        if self.play_base[card.get_color()] == (card - 1):
            return True
        return False
    
    def _resplace_card(self,hand,index:int):
        if index < 0 or index > 4: #check for hand size
            raise AttributeError("Index out of hand size")
        while index > 0: #move other cards down
            hand[index] = hand[index -1]
        if len(self.deck > 0):
            index[0] = self.deck.pop()
        else:
            index[0] = Hanabi_card(0) # we use the zeroeth hanabi card to represent a null space in a hand. This is only for the last move of the game

    def _play_card(self,hand,hand_index:int):
        card = hand[hand_index]
        if self._is_playable(card):
            self.play_base[card.get_color()] += 1
        else:
            self.misfires += 1
            if self.misfires >= 3:
                self.game_lost = True
        self._resplace_card(hand,hand_index)

    def _card_to_color(card:int):
        return (card -1) // 5

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

    def print_visual_other_hand(self,hand):
        print("hand: ",end="")
        for card in hand:
            color = self.color_order[card.color]
            number = card.number
            print(colored(number,color) + " ",end="")
        print("")
    
    def print_visual_my_hand(self,hand):
        print("hand: ",end="")
        for card in hand:
            number = "*" if card.get_number() == -1 else card.get_number()
            color = "light_grey" if card.get_color() == -1 else card.get_color()
            print(colored(number,color) + " ",end="")
        print("")
    
    def print_visual_discard(self):
        print("Discards: ",end="")
        for card in self.discards_reference:
            if self.discards[card] > 0:
                color = self.color_order[Hanabi_game._card_to_color(card)]
                number = card % 5
                if number == 0:
                    number == 5
                print(colored(number,color) + " ",end="")
        print("")



# old code for strategies
# played = False
# could_discard = [] #stores hand position of the card   [0,5]
# index_reference = {} #stores the value of the card indexed by hand position
#                     # {0:15,}
# #go through the hand; play any playable card; keep track of other cards
# for index in range(10):
#     if self._is_playable(self.hand[index]):
#         self._(self.hand[index])
#         #print(f"Played {hand[index]} on {play_base}")
#         self.hand[index] = self.deck.pop() #Draw a new card. This version does not have hand order
#         played = True
#         break #stop going through the hand

#     if not self._is_essential(self.hand[index]):
#         bisect.insort(could_discard,self.hand[index])
#         index_reference[self.hand[index]] = index

# #check to see if we've already played a card
# if played == True:
#     continue 

# elif (played == False) and (len(could_discard) > 0):
#     card = could_discard[-1]
#     hand_index = index_reference[card]
#     self.hand[hand_index] = self.deck.pop()
#     self.discards[card] += 1
#     continue

# else:
#     #debugging printing 
#     if self.print_lost_games:
#         print("Game lost")
#         self.print_visual_hand()
#         self.print_visual_play_base()
#         self.print_visual_discard()
    
#     if self.debug:
#         print(f"hand: {self.hand}")
#         print(f"Play base {self.play_base}")
#         print(f"Discards: {self.discards}")





#  def _is_essential(self,card:int) -> bool:
#         if ((card % 5) == 0): #check if card is a 5
#             return True
        
#         if (self.play_base[Hanabi_game._card_to_color(card)] >= card):
#             return False
        
#         #we don't need to worry about the fact that there are 3 ones in the deck for the following,
#         #because they're alwayas playable or discardable. They'll either be caught by the above expression
#         #or be directly played. This would not be the case if there were 3 ones
#         if (self.discards[card] == 1):
#             return True
#         return False
