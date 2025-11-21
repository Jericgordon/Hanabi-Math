
from termcolor import colored #used for printing Hanabi boards in readable output

class Hanabi_card():
    """Hanabi Card is a class created to represent a card in a hand of Hanabi"""    
    card_id = 0
    def __init__(self,card:int):
        if card < 0: #check for valid value
            raise AttributeError("Cannot assign a negative or zero value to a card.")
        
        if ((card - 1) // 5 ) < 0:
            raise AttributeError("Cannot assign a negative color")
        
       

        self.value = card #value is the literal number of the card in the encoding system

        self.number = (card - 1) % 5 + 1 # 1 -> 1 5 -> 5, 6->1,9 ->4,10 -> 5 
        self.color = (card - 1) // 5 

        self._color_order ={0:"red",1:'yellow',2:'green',3:'blue',4:'white',5:'magenta',99:'cyan'} #reference function for game
        self._color_text = self._color_order[self.color]
        self._color_known = False
        self._number_known = False

        self.card_id = Hanabi_card.card_id % 1024 
            #how to tell cards across rounds
    
    def __str__(self):
        """Allows a print(card) statement to correctly print in color"""
        number = self.number if self._number_known else "*"
        color = self._color_text if self._color_known else "dark_grey"
        return colored(number,color) + " "

    def get_entire_card(self) -> str:
        """Allows getting the entire card, ignoring whether it's been clued or not"""
        number = self.number
        color = self._color_text
        return colored(number,color) + " "


    def get_color(self): #returns -1 if color not yet identified
        """Returns the color of the card if known, or -1 if not identified"""
        if self._color_known:
            return self.color
        else: 
            return -1 
        
    def get_number(self): #returns -1 if color not yet identified
        """Returns the number of the card if known, or -1 if not identified"""
        if self._number_known:
            return self.number
        else:
            return -1
    
    def clue(self,clue_type,clue): # clue_type should be an enum
        """Allows a 'clue' to be given to a number card. This markes the color or number as "known"
        if applicable, and future calls to get_number/get_color will respond correctly
            Parmeters:
                clue_tyle: takes a string "number" or "color" to represent the sort of clue given
                clue: takes a number (1-5) if a number clue, or a color (1-5,6) if a color clue
        """
        if clue_type == "number" and self.number == clue:
            self._number_known = True
        
        if clue_type == "color" and self.color == clue:
            self._color_known = True


        




