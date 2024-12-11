from rating import Rating

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


"""
This class is an extension of the idea that we do have perfect knowledge, but now 
it might cost clues to play a card. This emulates the idea of a strategy, putting
some of the limitations of the boom - bust cycle naturally occuring in Hanbi back
into the game, but without the limitation of defining the clue strategy that would
give the average clue value defined in the class.

That is to say, we can define here that a card costs .25 clues to play, without being
burdened with creating and proving that there exists a strategy that could give
that average, and prove that it would come out to that.

Ideally, this gives us a good benchmark for how efficent a clue strategy must be to 
attain certain scores in Hanabi - an imporant step in defining a successful strategy
for the game.

category definitions for this class
4 - essential
3 - playable
2 - discardable, but useful
1 - useless

"""
class Cheating_clue_cost():
    def __init__(self):
        self.play_cost = 0
    def play_next_turn(self,my_hand,other_hand,discard,play_base,misfires,clue_tokens):
        #stop = input()
        self._new_turn(play_base,discard)
        my_hand_rating = Rating(0,4,5) # initally set our hand to the most essential card
        for card_index in range(len(my_hand)):
            r = self.rate_next_card(card_index,my_hand[card_index])
            if r.category == 3 and self._can_play(clue_tokens):
                return ("play",r.index)
            if r < my_hand_rating:
                my_hand_rating = r

        if clue_tokens < 1 + self.play_cost: #if we can't clue, we should discard
            return ("discard",r.index)

        for card_index in range(len(other_hand)):
            other_rating = self.rate_next_card(card_index,other_hand[card_index])
            if other_rating.category < my_hand_rating.category or other_rating.category == 3: 
                return ("clue","color",3) #if the other player has a categoricaly better card, we clue
        
        #otherwise we discard our best card
        return("discard",my_hand_rating.index)
 
    def _is_playable(self,card) -> bool:
        if card.value == 500:
            return False
        if self.play_base[card.color] == (card.value - 1):
            return True
        return False
    
    def _new_turn(self,play_base,discard):
        self.play_base = play_base
        self.discard = discard

    def _can_play(self,clues):
        if clues - self.play_cost < 0:
            return False
        return True
    
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


        diff = card.value - self.play_base[card.color] #difference between what's played, and what the card is
        return Rating(index,2,diff)