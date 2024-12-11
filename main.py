from Hanabi_simulator import Hanabi_game
from Cheating_strategies import Cheating_play,Cheating_play_discard,Cheating_clue_cost
import matplotlib.pyplot as plt
import numpy as np



def main():
    iterations = 100000
    #build the list of things considered
    play_cost_considered = [] 
    min_val = 0
    max_val = 2.1
    step_val = .25
    while min_val < max_val:
        play_cost_considered.append(min_val)
        min_val += step_val

    results = [[0 for _ in range(26)] for _ in range(len(play_cost_considered))] 
    s = Hanabi_game(5)
    #s.debug = True 
    for times in range(iterations):
        if times % 10000 == 0:
            print(times," iterations complete")
        for cost_index in range(len(play_cost_considered)):
            s.clues_per_play = play_cost_considered[cost_index]
            results[cost_index][s.play_game(Cheating_clue_cost)] += 1
        #score_play[s.play_game(Cheating_play)] += 1 
    
    cost_averages = {}
    for score_index in range(len(play_cost_considered)):
        sum_score = 0
        for val_index in range(len(results[0])):
            sum_score += (val_index * results[score_index][val_index])
        cost_averages[play_cost_considered[score_index]] = (sum_score / iterations)
    
 



    
    r = np.arange(26)
    for scores_index in range(len(play_cost_considered)):
        width = .1 * scores_index
        plt.bar(r + width,results[scores_index],label=play_cost_considered[scores_index],width=.1)
    
    plt.xlabel("Game Score")
    plt.ylabel("Number of games")
    plt.legend()
    plt.show()

    y_val = []
    for key,value in cost_averages.items():
        print(f"Average Score of play cost {key}:{value}")

        y_val.append(value)

    plt.xlabel("Clue cost of playing a card")
    plt.ylabel("Average score")
    plt.plot(play_cost_considered,y_val)
    plt.show()

    
if __name__ == '__main__':
    main()
    