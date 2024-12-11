from rating import Rating

class Clue_color():
    # Statuses of playing
        # 1.clue
        # 2.discard
        # 3.play
    def play_next_turn(self,my_hand,other_hand,discard,play_base,misfires,clue_tokens):
        #infinte clues, perfect knowledge
        my_hand_rating = Rating(0,3,5) #index, category, other_value # see comment above discard_usefullness
        s = play_discard_rater(discard,play_base)
        for card_index in range(len(my_hand)):
            if self._is_playable(my_hand[card_index],play_base) and :
                return ("play",card_index)
            r = s.rate_next_card(card_index,my_hand[card_index])
            if r < my_hand_rating:
                my_hand_rating = r
            
        for card_index in range(len(other_hand)):
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
    
    # def _is_clueable(self, card,play_base) -> bool:
    #     if self._is_playable(card,play_base):
            

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
    

        

class play_discard_rater():
    def __init__(self,discard, play_base):
        self.discard = discard
        self.play_base = play_base
        self.seen = {}

    # Categories of usefullness: 
    # 1. Useless: If we've already played it, we don't care
    # 2. Other; how we recon this is the difference between strategies
        # 1. We can discard the highest card,
        # 2. We can discard the highest chain card
    # 3. Essential: It's a 5, or we've discarded it before

    def rate_next_card(self,index,card) -> Rating:
        if card.value == 500:
            return Rating(index,3,5) # return max rating. We never want to discard the filler card
        
        #store the card in the seen list
        self.seen[card.value] = 1

        if self.play_base[card.color] >= card.value: #if the card is useless
            return Rating(index,1,0) 
        
        if card.number == 5 or self.discard[card.value] == 1: #if the card is essential
            diff = 5 - card.number
            return Rating(index,3,diff)

        #if we have a copy of it in either of the hands
        if card.value in self.seen.keys():
            return Rating(index,1,0)

        else:
            diff = card.value - self.play_base[card.color] #difference between what's played, and what the card is
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



