class Cheating_play_discard():
    # Statuses of playing
        # 1.clue 
        # 2.discard
        # 3.play
    def play_next_turn(self,my_hand,other_hand,discard,play_base,misfires,clue_tokens):
        #infinte clues, perfect knowledge
        stop = input()
        seen = {x:0 for x in range(1,(6 * 5) + 1)}
        seen[500] = 0
        my_hand_evaluation = [-1,5,0] #index, category, other_value # see comment above discard_usefullness
        for card_index in range(len(my_hand)):
            if self._is_playable(my_hand[card_index],play_base):
                return ("play",card_index)
            my_hand_evaluation = self.discard_usefullness(my_hand,card_index,play_base,discard,my_hand_evaluation)
            if seen[my_hand[card_index].value] == 0: #deals with duplicates in hand
                seen[my_hand[card_index].value] += 1
            else:
                my_hand_evaluation = [card_index,1,0]

        other_hand_evaluation = [-1,5,0]
        for card_index in range(len(other_hand)):
            other_hand_evaluation = self.discard_usefullness(other_hand,card_index,play_base,discard,other_hand_evaluation)
            if seen[my_hand[card_index].value] == 0: #deals with duplicates across hands
                seen[my_hand[card_index].value] += 1
            else:
                my_hand_evaluation = [card_index,1,0]
            # if the other hand has a better card to discard, or a card to play, we should let them either play or discard
            if self._is_playable(other_hand[card_index],play_base):
                return("clue","color",3) #clue the blue card
            if (other_hand_evaluation[1] < my_hand_evaluation[1]):
                return("clue","color",3) #clue the blue card
        
        if (other_hand_evaluation[1] == 2 and my_hand_evaluation[1] == 2): #in the case that both hands are filled with essential cards
            if other_hand[other_hand_evaluation[0]].number > my_hand[my_hand_evaluation[0]].number:
                return("clue","color",3) #clue the blue card
            else:
                return("discard",my_hand_evaluation[0])
            
        else:
            return ("discard",my_hand_evaluation[0])
                

    def _is_playable(self,card,play_base) -> bool:
        if card.value == 500:
            return False
        if play_base[card.color] == (card.value - 1):
            return True
        return False
    
    # Categories of usefullness: 
        # 1. Useless: If we've already played it, we don't care
        # 2. Other; how we recon this is the difference between strategies
            # 1. We can discard the highest card,
            # 2. We can discard the highest chain card
        # 3. Essential: It's a 5, or we've discarded it before
    def discard_usefullness(self,hand,index,play_base,discard,hand_evaluation):
        if hand[index].value == 500:
            return hand_evaluation
        if play_base[hand[index].color] >= hand[index].value:
            return [index,1,0] # return that it's useless
        
        if hand[index].number == 5 or discard[hand[index].value] == 1: #if the card is essential
            other_value = 5 - hand[index].number
            if 3 < hand_evaluation[1]:
                return [index,3,other_value]
            if hand_evaluation[1] == 3 and other_value < hand_evaluation[2]:
                return [index,3,other_value]
            return hand_evaluation

        else:
            other_value = hand[index].value - play_base[hand[index].color]
            if 2 < hand_evaluation[1]: #if this is a better card to discard
                return [index,2,other_value]
            if hand_evaluation[1] == 2 and other_value > hand_evaluation[2]:
                return [index,2,other_value]
            return hand_evaluation
        

class Cheating_play():
    # Statuses of playing
        # 1.clue 
        # 2.discard
        # 3.play
    def play_next_turn(self,my_hand,other_hand,discard,play_base,misfires,clue_tokens):
        #infinte clues, perfect knowledge
        stop = input()
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
                other_hand_could_discard.append(could_discard)
        
        if len(could_discard >= 1):
            return("discard",could_discard[0])
        elif len(other_hand_could_discard) >= 1:
            return("clue","color",3)
        else:
            return ("discard",my_hand[0])

    def _is_playable(self,card,play_base) -> bool:
        if card.value == 500:
            return False
        if play_base[card.color] == (card.value - 1):
            return True
        return False

    def _is_essential(self,card,play_base,discard):
        if card.number == 5:
            return True
        if play_base[card.color] >= card.value:
            return False
        if discard[card.value] >= 1:
            return True
        return False
