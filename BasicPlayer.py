from BoardState import BoardState
import random
from typing import Optional


class BasicPlayer:
    def search(self, boardState: BoardState) -> (int, int):
        moves = boardState.allLegalMoves()
        if len(moves) == 0:
            raise RuntimeError("No legal moves in the given board state")

        if len(moves) == 1:
            return moves[0]

        move = self.immediatelyWinningMove(boardState)
        if move is not None:
            return move

        smartMoves = self.smartMoves(boardState)

        if len(smartMoves) == 0:
            return random.choice(moves)
        elif len(smartMoves) == 1:
            return smartMoves[0]
        else:
            return random.choice(smartMoves)


    def immediatelyWinningMove(self, boardState: BoardState) -> (int, int):
        whoami = boardState.player
        for (x, y) in boardState.allLegalMoves():
            child = boardState.clone()
            child.set(x, y)
            if child.isTerminal() and child.gameWon == whoami:
                return x, y
        return None


    def smartMoves(self, boardState: BoardState) -> [(int, int)]:
        result = []

        for (x, y) in boardState.allLegalMoves():
            child = boardState.clone()
            child.set(x, y)
            move = self.immediatelyWinningMove(child)
            if move is None:
                result.append((x, y))

        return result