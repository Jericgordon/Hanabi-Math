from Hanabi_simulator import Hanabi_game
from Cheating_strategies import Cheating_play,Cheating_play_discard,Clue_color, Clue_num, Clue_eff
import matplotlib.pyplot as plt
import numpy as np



def main():
    iterations = 10000
    score_clue_color = [0 for _ in range(26)]
    score_clue_num = [0 for _ in range(26)]
    s = Hanabi_game(5)
    s.debug = True
    s.play_game(Clue_eff)
    # for _ in range(iterations):
    #     score_clue_color[s.play_game(Clue_color)] += 1
    #     score_clue_num[s.play_game(Clue_num)] += 1 
        
    # x_axis = [x for x in range(0,26)]
    # total_points_clue_color = 0
    # total_points_clue_num = 0
    # for val_index in range(len(score_clue_color)):
    #     total_points_clue_color += (val_index * score_clue_color[val_index])
    #     total_points_clue_num += (val_index * score_clue_num[val_index])

    # average_score_clue_color = total_points_clue_color /iterations
    # average_score_clue_num = total_points_clue_num /iterations
    # print("average score clue_color",average_score_clue_color)
    # print("average score clue_num",average_score_clue_num)

    # width = .25
    # r = np.arange(26)
    # print("done with other things")
    # plt.bar(r,score_clue_color,color = 'g',width=.25,label= "clue_by_color")
    # plt.bar(r + width,score_clue_num,color = 'b',width=.25,label = "clue by number")
    # plt.legend()
    # plt.show()


    
if __name__ == '__main__':
    main()
    