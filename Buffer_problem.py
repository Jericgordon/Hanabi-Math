import random



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

#if winnable return 0
#if not winnable return 1

def play_game(players,colors) -> int:

    #setup game variables
    deck = make_deck(colors)
    player_hands = [[] for x in range(players)] # -> [[],[]]
    discard = []
    play_base = [x for x in range(-1,colors * 5,5)] # -> [0,5,10] 

    #deal cards to each player
    for player in range(players):
        #deal a 5 card hand
        for _ in range(5):
            player_hands[player].append(deck.pop())


    while len(deck) > (players - 1):
        for player in range(players):
            could_discard_index = -1
            played = False
            for card_index in range(5):
                if played: #check if played
                    continue

                card = player_hands[player][card_index]
                color = card // 5

                #check if card is playable
                if play_base[color] == (card - 1):
                    #play card
                    #print(f"Played card {card} on board {play_base}")
                    play_base[color] += 1 #play the card
                    player_hands[player][card_index] = deck.pop() # replace the card in the hand
                    played = True #break out of for loop
                
                elif could_discard_index == -1 and (card % 5) != 4 and (play_base[color] >= card or card not in discard):
                    could_discard_index = card_index
                    continue
                
                elif card_index != 4: 
                    continue

                elif could_discard_index != -1:
                    #print(f"discarded {card} on board {play_base}")
                    player_hands[player][could_discard_index] = deck.pop() # replace the card in the hand
                    discard.append(card)
                
                else:
                    return 1

    return 0





    

def main():
    results = {"win":0,"loss":0}
    for _ in range(5000):
        if (play_game(2,6) == 0):
            results["win"] += 1
        else:
            results["loss"] += 1
    print((results["loss"]/5000) * 100)
    
    print(results)

        




main()