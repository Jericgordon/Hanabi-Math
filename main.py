from Hanabi_simulator import Hanabi_game
from Strategy import Strategy
from Cheating_strategy import Cheating_strategy
from Cheat_strat_clue import Cheat_strat_clue
import matplotlib.pyplot as plt

def main():
    # iterations = 1000000
    # score = [0 for _ in range(26)] 
    # s = Hanabi_game(5)
    # for _ in range(iterations):
    #     score[s.play_game(Cheating_strategy)] += 1   
    # x_axis = [x for x in range(0,26)]
    # average_score = 0
    # for val_index in range(len(score)):37
    #     average_score += (val_index * score[val_index])
    # average_score = average_score / iterations
    # print(average_score)
    # plt.bar(x_axis,score)
    # plt.show()
    s = Hanabi_game(5)
    s.debug = True
    #s.play_game(Strategy)
    s.play_game(Cheat_strat_clue)
    #s.play_game(Cheating_strategy)
    
    
if __name__ == '__main__':
    main()
    