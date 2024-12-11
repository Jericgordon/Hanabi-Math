from rating import Rating

class Clue_eff():
    # Statuses of playing
        # 1.clue
        # 2.discard
        # 3.play
    def play_next_turn(self,my_hand,other_hand,discard,play_base,misfires,clue_tokens):
        #limited clues, must clue before playing, perfect knowledge
        # stop = input()
        my_hand_rating = Rating(0,4,0) #index, category, other_value # see comment above discard_usefullness
        s = card_rater(play_base,discard)
        for card_index in range(len(my_hand)):
            if self._is_playable(my_hand[card_index],play_base) and self._is_clued(my_hand[card_index]):
                return ("play",card_index)
            r = s.rate_next_card(card_index,my_hand[card_index])
            if r < my_hand_rating:
                my_hand_rating = r
        
        if clue_tokens <= 0:
            return("discard",r.index)
        
        opt_clue = self._opt_clue(other_hand,play_base)
        if opt_clue != None:
            return opt_clue

        for card_index in range(len(other_hand)):
            other_rating = s.rate_next_card(card_index,my_hand[card_index])
            if other_rating < my_hand_rating or self._is_playable(other_hand[card_index],play_base): # if it's playable or better to discard
                return("clue","number",5) #clue the blue card

        return("discard",my_hand_rating.index)


    def _is_clued(self, card):
        if card.get_color() == -1 and card.get_number() == -1:
            return False
        return True
 

    def _is_playable(self,card,play_base) -> bool:
        if card.value == 500:
            return False
        if play_base[card.color] == (card.value - 1):
            return True
        return False
    
    def _opt_clue(self, hand,play_base):
        color_clues = {0:[0,False],
                        1:[0,False],
                        2:[0,False],
                        3:[0,False],
                        4:[0,False],
                        19:[0,False]}
        
        number_clues = {1:[0,False],
                        2:[0,False],
                        3:[0,False],
                        4:[0,False],
                        5:[0,False],
                        99:[0,False]}
        
        max = 0
        clue = None
        for card_index in range(len(hand)):
            if hand[card_index].value == 500:
                continue
            if self._is_playable(hand[card_index], play_base):
                color_clues[hand[card_index].color][1] = True
                number_clues[hand[card_index].number][1] = True
            color_clues[hand[card_index].color][0] += 1 #update color
            if color_clues[hand[card_index].color][0] > max and color_clues[hand[card_index].color][1]:
                max = color_clues[hand[card_index].color][0]
                clue = ("clue","color",hand[card_index].color)
            number_clues[hand[card_index].number][0] += 1
            if number_clues[hand[card_index].number][0] > max and number_clues[hand[card_index].number][1]:
                max = number_clues[hand[card_index].number][0]
                clue = ("clue","number",hand[card_index].number)
        return clue




            

class Clue_color():
    # Statuses of playing
        # 1.clue
        # 2.discard
        # 3.play
    def play_next_turn(self,my_hand,other_hand,discard,play_base,misfires,clue_tokens):
        #limited clues, must clue before playing, perfect knowledge
        #stop = input()
        my_hand_rating = Rating(0,3,5) #index, category, other_value # see comment above discard_usefullness
        s = play_discard_rater(discard,play_base)
        for card_index in range(len(my_hand)):
            if self._is_playable(my_hand[card_index],play_base) and my_hand[card_index].get_color() != -1:
                return ("play",card_index)
            r = s.rate_next_card(card_index,my_hand[card_index])
            if r < my_hand_rating:
                my_hand_rating = r
        
        if clue_tokens <= 0:
            return("discard",r.index)

        for card_index in range(len(other_hand)):
            if self._is_playable(other_hand[card_index],play_base):
                return("clue","color",other_hand[card_index].color)
            other_rating = s.rate_next_card(card_index,my_hand[card_index])
            if other_rating < my_hand_rating or self._is_playable(other_hand[card_index],play_base): # if it's playable or better to discard
                return("clue","number",5) #clue the blue card

        return("discard",my_hand_rating.index)
 

    def _is_playable(self,card,play_base) -> bool:
        if card.value == 500:
            return False
        if play_base[card.color] == (card.value - 1):
            return True
        return False
    
class Clue_num():
    # Statuses of playing
        # 1.clue
        # 2.discard
        # 3.play
    def play_next_turn(self,my_hand,other_hand,discard,play_base,misfires,clue_tokens):
        #limited clues, must clue before playing, perfect knowledge
        #stop = input()
        my_hand_rating = Rating(0,3,5) #index, category, other_value # see comment above discard_usefullness
        s = play_discard_rater(discard,play_base)
        for card_index in range(len(my_hand)):
            if self._is_playable(my_hand[card_index],play_base) and my_hand[card_index].get_number() != -1:
                return ("play",card_index)
            r = s.rate_next_card(card_index,my_hand[card_index])
            if r < my_hand_rating:
                my_hand_rating = r
            
        if clue_tokens <= 0:
            return("discard",r.index)
        
        for card_index in range(len(other_hand)):
            if self._is_playable(other_hand[card_index],play_base):
                return("clue","number",other_hand[card_index].number)
            other_rating = s.rate_next_card(card_index,my_hand[card_index])
            if other_rating < my_hand_rating or self._is_playable(other_hand[card_index],play_base): # if it's playable or better to discard
                return("clue","number",5) #clue the blue card

        return("discard",my_hand_rating.index)
 

    def _is_playable(self,card,play_base) -> bool:
        if card.value == 500:
            return False
        if play_base[card.color] == (card.value - 1):
            return True
        return False

class Cheating_play_discard():
    # Statuses of playing
        # 1.clue 
        # 2.discard
        # 3.play
    def play_next_turn(self,my_hand,other_hand,discard,play_base,misfires,clue_tokens):
        #infinte clues, perfect knowledge
        my_hand_rating = Rating(0,3,5) #index, category, other_value # see comment above discard_usefullness
        s = play_discard_rater(discard,play_base)
        for card_index in range(len(my_hand)):
            if self._is_playable(my_hand[card_index],play_base):
                return ("play",card_index)
            r = s.rate_next_card(card_index,my_hand[card_index])
            if r < my_hand_rating:
                my_hand_rating = r
            
        for card_index in range(len(other_hand)):
            other_rating = s.rate_next_card(card_index,my_hand[card_index])
            if other_rating < my_hand_rating or self._is_playable(other_hand[card_index],play_base): # if it's playable or better to discard
                return("clue","color",3) #clue the blue card

        return("discard",my_hand_rating.index)
 

    def _is_playable(self,card,play_base) -> bool:
        if card.value == 500:
            return False
        if play_base[card.color] == (card.value - 1):
            return True
        return False
    

class card_rater():
    def __init__(self,play_base,discard):
        self.play_base = play_base
        self.discard = discard

    def _is_playable(self,card) -> bool:
        if card.value == 500:
            return False
        if self.play_base[card.color] == (card.value - 1):
            return True
        return False
    
    def rate_next_card(self,index,card) -> Rating:
        if card.value == 500:
            return Rating(index,4,5) # return max rating. We never want to discard the filler card
    
        if self._is_playable(card): #returns a rating of 4 if playable
            other_value = 5 - card.number
            return Rating(index,3,other_value)
        #store the card in the seen list
        

        if self.play_base[card.color] >= card.value: #if the card is useless
            return Rating(index,1,0) 
        
        if card.number == 5 or (self.discard[card.value] == 1 and card.number != 1) or \
            (card.number == 1 and self.discard[card.value] == 2): #if the card is essential
            diff = 5 - card.number
            return Rating(index,4,diff)


        diff = abs(self.play_base[card.color] - card.value) #difference between what's played, and what the card is
        return Rating(index,2,diff)



class Cheating_play():
    # Statuses of playing
        # 1.clue 
        # 2.discard
        # 3.play
    def play_next_turn(self,my_hand,other_hand,discard,play_base,misfires,clue_tokens):
        #infinte clues, perfect knowledge
        #stop = input()
        seen = {x:0 for x in range(1,(6 * 5) + 1)}
        seen[500] = 0
        could_discard = []
        other_hand_could_discard = []
        for card_index in range(len(my_hand)):
            if self._is_playable(my_hand[card_index],play_base):
                return ("play",card_index)
            if not self._is_essential(my_hand[card_index],play_base,discard):
                could_discard.append(card_index)
            
        for card_index in range(len(other_hand)):
            # if the other hand has a card to play, we should let them either play or discard
            if self._is_playable(other_hand[card_index],play_base):
                return("clue","color",3) #clue the blue card
            if not self._is_essential(other_hand[card_index],play_base,discard):
                other_hand_could_discard.append(card_index)
        
        if len(could_discard) >= 1:
            return("discard",could_discard[0])
        elif len(other_hand_could_discard) >= 1:
            return("clue","color",3)
        else:
            return ("discard",4)

    def _is_playable(self,card,play_base) -> bool:
        if card.value == 500:
            return False
        if play_base[card.color] == (card.value - 1):
            return True
        return False

    def _is_essential(self,card,play_base,discard):
        if card.value == 500:
            return True
        if card.number == 5:
            return True
        if play_base[card.color] >= card.value:
            return False
        if discard[card.value] >= 1:
            return True
        return False



