

class Cheating_strategy():
    # Statuses of playing
        # 1.clue 
        # 2.discard
        # 3.play
    def play_next_turn(self,my_hand,other_hand,discard, play_base,misfires,clue_tokens):
        current_evaluation = [-1,0,0] #index, category, other_value # see comment above discard_usefullness
        can_play = []
        for card_index in len(my_hand):
            if self._is_playable(my_hand[card_index],play_base):
                can_play.append(card_index)
                continue # We don't want to consider discarding this card if we can play it, as
                         # we'll always choose to play a card if possible
            current_evaluation = self.discard_usefullness(my_hand[card_index],play_base,discard,current_evaluation)
        if len(can_play == 1):
            return ("play",can_play[0])
        if len(can_play) > 1:
            for card_index in can_play():
                for card in other_hand:
                    if my_hand[card_index].color == card.color < 


    def _is_playable(self,card,play_base) -> bool:
        ...
    
    # Categories of usefullness: 
        # 1. Essential: It's a 5, or we've discarded it before
        # 2. Useless: If we've already played it, we don't care
        # 3. Other; how we recon this is the difference between strategies
            # 1. We can discard the highest card,
            # 2. We can discard the highest chain card
         
    def discard_usefullness(self,card,play_base,discard,current_evaluation) -> int:
        index = -1
        category = 0
        other_value = 0
        ...

