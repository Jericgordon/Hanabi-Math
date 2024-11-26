import unittest

# we use a class to represent a hanabi card, and group related functions.
# importantly, we use by convention the card 0 to indicate a null value

class Hanabi_card():    
    card_id = 0
    def __init__(self,card:int):
        if card < 0: #check for valid value
            raise AttributeError("Cannot assign a negative or zero value to a card.")
        
        if (card - 1) // 5 < 0:
            raise AttributeError("Cannot assign a negative color")
        
        self.value = card

        self.number = (card - 1) % 5 + 1 # 1 -> 1 5 -> 5, 6->1,9 ->4,10 -> 5 
        
        self.color = card // 5
        self._color_known = False
        self._number_known = False

        self.card_id = Hanabi_card.card_id % 1024 
            #how to tell cards across rounds

    def get_color(self): #returns -1 if color not yet identified
        if self._color_known:
            return self.color
        else: 
            return -1 
        
    def get_number(self):
        if self._number_known:
            return self.number
        else:
            return -1
    
    def clue(self,clue_type,clue): # clue_type should be an enum
        if clue_type == "number" and self.number == clue:
            self._number_known = True
        
        if clue_type == "color" and self.color == clue:
            self._color_known = True


        




