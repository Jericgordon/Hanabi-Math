from Hanabi_simulator import Hanabi_game
from Strategy import Strategy
from Cheating_strategy import Cheating_strategy


def main():
    s = Hanabi_game(6)
    # s.debug = True
    s.play_game(Cheating_strategy)


if __name__ == '__main__':
    main()