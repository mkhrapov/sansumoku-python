from BoardState import BoardState, BLUE
from BasicPlayer import BasicPlayer
from MonteCarloPlayer import MonteCarloPlayer
from InitialMove import initialMove
import datetime


def main():
    game = BoardState()
    blue = BasicPlayer()
    orange = MonteCarloPlayer(1000)

    print(datetime.datetime.now())
    print("NEW GAME")
    counter = 1

    x, y = initialMove()
    print(f"BLUE {x} {y}")
    game.set(x, y)

    counter += 1

    while not game.isTerminal():
        if game.player == BLUE:
            x, y = blue.search(game)
            print(f"BLUE {x} {y}")
            game.set(x, y)
        else:
            x, y = orange.search(game)
            print(f"ORAN {x} {y}")
            game.set(x, y)

        counter += 1

    print(f"WINNER {game.gameWon}")
    print(datetime.datetime.now())


if __name__ == "__main__":
    main()
