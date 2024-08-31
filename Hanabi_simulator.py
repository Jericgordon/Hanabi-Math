import random
from termcolor import colored


def main():
    games = 1000000
    wins = 0
    for _ in range(games):
        if play_game(5):
            wins += 1

    print(f"{wins} out of {games} games were won. A win rate of {wins/games}")
    # print_visual_cards([3, 7, 12, 5, 17, 8, 20, 11, 1, 2, 18, 5])
    # print_play_base([-1, 4, 9, 15, 22])

def is_essential(discards:list, play_base:list, card:int) -> bool:
    if ((card % 5) == 4):
        return True
    
    if (play_base[card // 5] >= card):
        return False
    
    if card in discards:
        return True
    
    return False

def is_playable(card:int, play_base):
    
    color = card // 5
    if play_base[color] == (card - 1):
        return True
    return False

def play_game(colors) -> int:
    #print("---New Game----")
    deck = make_deck(colors)
    hand = [] #create a list of cards to add into the hand representing both hands
    discard = [] #list of cards discarded
    play_base = [x for x in range(-1,(colors-1) * 5,5)] # -> [0,5,10] 
    #print(f"Play Base: {play_base}")

    #deal hand
    for _ in range(10):
        hand.append(deck.pop())

    while len(deck) > 0:
        played = False
        for index in range(10):
            if is_playable(hand[index],play_base):
                play_base[(hand[index] // 5)] += 1
                #print(f"Played {hand[index]} on {play_base}")
                hand[index] = deck.pop()
                played = True
                
                break
        
        #check to see if we've already played a card
        if played == True:
            continue

        #see if there's a card that we could get
        for index in range(10):
            if not is_essential(discard,play_base,hand[index]):
                discard.append(hand[index])
                hand[index] = deck.pop()
                played = True
                break
        
        if played == False:
            # print("Game lost")
            # print(f"could not play any of {hand} on {play_base}")
            # print("hand: ",end="")
            # print_visual_cards(hand)
            # print("Play Base: ",end="")
            # print_play_base(play_base)
            # print(f"The discard was: ",end="")
            # print_visual_cards(discard)
            return False
    
    #print("Game won")
    return True



def print_play_base(to_print):
    color_order = {0:"red",1:'yellow',2:'green',3:'blue',4:'white'}
    for index in range(len(to_print)):
        card = to_print[index] + 1
        color = color_order[(card) // 5]
        number = (card) % 5
        print(colored(number,color) + " ",end="")
    print("")

def print_visual_cards(to_print:list):
    color_order = {0:"red",1:'yellow',2:'green',3:'blue',4:'white'}
    to_print.sort()
    for card in to_print:
        color = color_order[card//5]
        number = card % 5
        print(colored(number + 1,color) + " ",end="")
    print("")






#A unique card is card (color_number * 5) + card_number
#e.g. if blue is 2, the blue one is (2 * 5) + 2 or 12
def make_deck(colors) -> list:
    deck = []
    for color in range(colors):
        #Add ones
        for _ in range(3):
            deck.append((color * 5) + 0)
        #Add 2-4
        for card_number in range(2,5):
            for _ in range(2):
                deck.append((color * 5) + card_number - 1)
        #Add 5s
        deck.append((color * 5) + 4)
    random.shuffle(deck)
    return deck









if __name__ == "__main__":
    main()  
