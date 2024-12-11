import random #used for shuffling the deck
import copy #used for makeing a copy of a the deck to shuffle
from termcolor import colored #used for printing Hanabi boards in readable output
from Card import Hanabi_card

class Hanabi_game():
    def __init__(self,colors:int) -> None:
        #user preferences
        self.print_lost_games = False
        self.debug = False
        self.colors = colors
        self.clues_per_play = 0 #this is a testing parameter for auto-deducting a clue per_play. 
                            #has no use in the real game

        #built in options
        self.color_order ={0:"red",1:'yellow',2:'green',3:'blue',4:'white',5:'magenta'}
        self.discards_reference = {x:0 for x in range(1,(self.colors * 5) + 1)}
        self.discards_reference[500] = 0
        self.play_base_reference = [x for x in range(0,(self.colors) * 5,5)]
        self.deck_reference = self._make_deck(colors)

    def print_lost_games(self):
        self.print_lost_games = True

    def _setup_new_game(self):
        self.discards = copy.deepcopy(self.discards_reference)
        self.play_base = copy.deepcopy(self.play_base_reference)
        self.hands = [[] for _ in range(2)]
        self.misfires = 0
        self._game_lost = False # Boolean to check if the game is lost
        self.clue_counter = 8
        self.score = 0
        self.turn = 0
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
        last_moves = 2
        player = 0 #this gives us which hand to access when clueing this is the index of the current players hand. player + 1 % 2 is the index of the other
        opponant = 1
        s1 = strategy() #strategy for player 1
        s2 = strategy() #strategy for player 2
        if self.clues_per_play != 0: #sets clue cost in strategy if enabled
            s1.play_cost = self.clues_per_play # 
            s2.play_cost = self.clues_per_play #
        while last_moves >= 0 and self.score != (self.colors * 5):
            if len(self.deck) == 0:
                last_moves -= 1 #this gives us exactly 2 turns after the deck depletes, which the rules require
            self._print_all()
            if player == 0: #if it's player 
                move = s1.play_next_turn(self.hands[0],self.hands[1],self.discards,self.play_base,self.misfires,self.clue_counter) #player hand,other hand,discards
            if player == 1:
                move = s2.play_next_turn(self.hands[1],self.hands[0],self.discards,self.play_base,self.misfires,self.clue_counter)
            match move[0]:
                case "play":
                    self._play_card(self.hands[player],move[1])
                case "discard":
                    self._discard_card(self.hands[player],move[1])
                case "clue":
                    self._clue_hand(self.hands[opponant],move[1],move[2])
                case _:
                    raise ValueError("Invalid move given. Valid moves are play, clue, discard")
            
            self.turn += 1
            player = self.turn % 2 # This switches between players, as the only fixed relation in this game is between player and turn
            opponant = (player + 1) % 2
            if self._game_lost:
                break
        self._print_all()
        return self.score

    def _clue_hand(self,hand,clue_type,clue:int):
        self.clue_counter -= 1
        for card in hand:
            card.clue(clue_type,clue)
        
    def _print_all(self):                                                                  
        if self.debug:
            print(f"turn {self.turn}")
            print("")
            print(f"Clue tokens: {self.clue_counter}")
            self.print_visual_discard()
            self.print_visual_play_base()
            self.print_visual_other_hand(self.hands[(self.turn +1) % 2])
            self.print_visual_other_hand(self.hands[(self.turn) % 2])
            self.print_visual_my_hand(self.hands[(self.turn +1) % 2])
            self.print_visual_my_hand(self.hands[(self.turn) % 2])
    
    def _discard_card(self,hand,index:int):
        self.discards[hand[index].value] +=1 # we do store cards in the discard by their literal value, not by card                                              
        self._resplace_card(hand,index)
        self._add_clue_token()

    def _is_playable(self,card:Hanabi_card):
        if self.play_base[card.color] == (card.value - 1):
            return True
        return False
    
    def _resplace_card(self,hand,index:int): #we could get faster with a circular queue; I'm not sure how much faster it would be
        if index < 0 or index > 4: #check for hand size
            raise AttributeError("Index out of hand size")
        while index > 0: #move other cards down
            hand[index] = hand[index -1]
            index -= 1
        if len(self.deck) > 0:
            hand[0] = Hanabi_card(self.deck.pop())
        else:
            hand[0] = Hanabi_card(500) # we use the zeroeth hanabi card to represent a null space in a hand. This is only for the last move of the game

    def _play_card(self,hand,hand_index:int) -> None:
        card = hand[hand_index]
        self.clue_counter -= self.clues_per_play
        if self.clue_counter < 0 and self.clues_per_play != 0:
            raise RuntimeError("Cannot have less than 0 clue tokens")
        if not self._is_playable(card): #if the selected card is not playable
            self.misfires += 1
            if self.misfires >= 3:
                self._game_lost = True
            self._resplace_card(hand,hand_index)
            return
        
         # if it is playable
        if hand[hand_index].number == 5:
            self._add_clue_token()
        self.score += 1
        self.play_base[card.color] += 1
        self._resplace_card(hand,hand_index)

    def _card_to_color(card:int):
        return (card -1) // 5

    def _add_clue_token(self) -> None:
        self.clue_counter += 1
        if self.clue_counter > 8:
            self.clue_counter = 8 
            

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
            print(card.get_entire_card(),end="")
        print("")
    
    def print_visual_my_hand(self,hand):
        print("hand: ",end="")
        for card in hand:
            print(card,end="")
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