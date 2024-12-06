#from abc import ABC,ABCMeta
class Strategy():
    def play_next_turn(self,my_hand,other_hand,discard,play_base,misfires,clue_tokens): #this returns a tuple of the following format (move,relevant_index) or (clue,clue_type,clue). Move has 3 valid states 
        move = 0
        while move not in range(1,4):
            print("1 - Play card")
            print("2 - Discard card")
            print("3 - clue")
            move = int(input("Which would you like to do?"))
        
        match move:
            case 1:
                index = 0
                while index not in range(1,6):
                    index = int(input("which card would you like to play"))
                index -= 1
                return ("play",index)
            case 2:
                index = 0
                while index not in range(1,6):
                    index = int(input("which card would you like to discard"))
                    test = type(index)
                index -= 1
                return("discard",index)
            case 3:
                type_choice  = 0
                while type_choice not in range(1,3):
                    print("1 - color clue")
                    print("2 - number clue")
                    type_choice = int(input())
                type_choice -= 1
                if type_choice == 0:
                    color = 0
                    color_list = ["red",'yellow','green','blue','white','magenta']
                    while color not in range(1,7):
                        for color_index in range(len(color_list)):
                            print(color_index + 1,end="")
                            print(" - ",end="")
                            print(color_list[color_index],end="")
                            print(",",end="")
                        color = int(input("What color would you like to clue?"))
                    color -= 1
                    return ("clue","color",color)
                else:
                    number = 0
                    while number not in range(1,6):
                        number = int(input("Pick a number to clue"))
                    return ("clue","number",number)
                
                        
            

