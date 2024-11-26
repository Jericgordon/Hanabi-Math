from Hanabi_simulator import Hanabi_game
from Strategy import Strategy

def main():
    s = Hanabi_game(6)
    s.debug = True
    s.play_game(Strategy)


if __name__ == '__main__':
    main()