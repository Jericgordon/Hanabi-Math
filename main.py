from Hanabi_simulator import Hanabi_game
from Cheating_strategies import Cheating_play,Cheating_play_discard,Clue_color, Clue_num, Clue_eff
import matplotlib.pyplot as plt
import numpy as np



def main():
    iterations = 10000
    score_clue_eff = [0 for _ in range(26)]
    s = Hanabi_game(5)
    # s.debug = True
    # s.play_game(Clue_eff)
    for _ in range(iterations):
        score_clue_eff[s.play_game(Clue_eff)] += 1
        
    x_axis = [x for x in range(0,26)]
    total_points_clue_eff = 0
    for val_index in range(len(score_clue_eff)):
        total_points_clue_eff += (val_index * score_clue_eff[val_index])

    average_score_clue_eff = total_points_clue_eff /iterations
    print("average score clue_eff",average_score_clue_eff)

    width = .25
    r = np.arange(26)
    plt.bar(r + width,score_clue_eff,color = 'b',width=.25,label = "clue efficiency")
    plt.legend()
    plt.show()


    
if __name__ == '__main__':
    main()
    