from Cheating_strategies import Cheating_play_discard
from Hanabi_game import Hanabi_game
import matplotlib.pyplot as plt


def main():
     """This setup is for 5 cards, with a cheating strategy that has infinite clues,
     but not complete knowledge of the deck. In the situation where it has to discard
     a card, it chooses the one that is non-essential furthest from being played.

     Imagine the following board

     Board r1 g2 ....
     Discard - [cards that make all other cards essential]

     Hand: r4, g4 ... [all esential cards]
     Hand2: [all esential cards]

     The algority with discard the r4 because it's 3 away from being played, 
     and the g4 is 2 away from being played
     """

     game = Hanabi_game(5) # 
     number_of_games = 10 ** 5

     #final results variables
     games_exactly_at_25 = 0
     games_less_than_25 = 0

     for _ in range(number_of_games):
          if (game.play_game(Cheating_play_discard) == 25):
               games_exactly_at_25 += 1
          else:
               games_less_than_25 += 1

     graph_won_lost([games_exactly_at_25,games_less_than_25])



def graph_won_lost(games):
     
     total_games = 0

     #get total games
     for number in games:
          total_games += number
     
     print("games won",games[0]/total_games)\

     plt.bar(["games won","games lost"],games)
     plt.show()
          




if (__name__ == '__main__'):
     main()