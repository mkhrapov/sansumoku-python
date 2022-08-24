from BoardState import BoardState
from BoardState import DONE
import random


class MonteCarloPlayer:
    def __init__(self, iter_count: int):
        self.iter_count = iter_count


    def search(self, boardState: BoardState) -> (int, int):
        moves = boardState.allLegalMoves()
        whoami = boardState.player
        scores = []

        if len(moves) == 0:
            raise RuntimeError("No legal moves in the given board state")

        if len(moves) == 1:
            return moves[0]

        for _ in moves:
            scores.append(0.0)

        for _ in range(self.iter_count):
            for i in range(len(moves)):
                x, y = moves[i]
                child = boardState.clone()
                child.set(x, y)
                winner = self.playout(child)
                if winner == whoami:
                    scores[i] += 1.0
                if winner == DONE:
                    scores[i] += 0.05

        bestMove = moves[0]
        highestScore = scores[0]

        for i in range(1, len(moves)):
            if scores[i] > highestScore:
                highestScore = scores[i]
                bestMove = moves[i]

        return bestMove


    def playout(self, boardState: BoardState) -> int:
        while not boardState.isTerminal():
            moves = boardState.allLegalMoves()
            x, y = random.choice(moves)
            boardState.set(x, y)
        return boardState.gameWon