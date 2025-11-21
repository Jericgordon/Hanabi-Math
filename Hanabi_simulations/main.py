from Hanabi_game import Hanabi_game
from Cheating_strategies import Cheating_play,Cheating_play_discard
import matplotlib.pyplot as plt
import numpy as np



def main():
    iterations = 100000
    score_play_and_discard = [0 for _ in range(26)]
    score_play = [0 for _ in range(26)]
    s = Hanabi_game(5)
    #s.debug = True 
    for _ in range(iterations):
        score_play_and_discard[s.play_game(Cheating_play_discard)] += 1 
        score_play[s.play_game(Cheating_play)] += 1 
        
    x_axis = [x for x in range(0,26)]
    total_points_play_discard = 0
    total_points_play = 0
    for val_index in range(len(score_play_and_discard)):
        total_points_play_discard += (val_index * score_play_and_discard[val_index])
        total_points_play += (val_index * score_play[val_index])

    average_score_play_discard = total_points_play_discard / iterations
    average_score_play = total_points_play /iterations
    print("average score playing and discarding:",average_score_play_discard)
    print("average score playing",average_score_play)

    width = .25
    r = np.arange(26)
    
    plt.bar(r,score_play_and_discard,color = 'b',width=.5)
    plt.bar(r + width,score_play,color = 'g',width=.25)
    plt.xlabel("Score achieved")
    plt.ylabel("Iterations")
    plt.show()


    
if __name__ == '__main__':
    main()
    