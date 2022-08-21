from __future__ import annotations
from array import array

OPEN = 0
BLUE = 1
ORAN = 2
DONE = 3

SUDOKU_GROUPS = [
    {0, 1, 2, 3, 4, 5, 6, 7, 8},
    {9, 10, 11, 12, 13, 14, 15, 16, 17},
    {18, 19, 20, 21, 22, 23, 24, 25, 26},
    {27, 28, 29, 30, 31, 32, 33, 34, 35},
    {36, 37, 38, 39, 40, 41, 42, 43, 44},
    {45, 46, 47, 48, 49, 50, 51, 52, 53},
    {54, 55, 56, 57, 58, 59, 60, 61, 62},
    {63, 64, 65, 66, 67, 68, 69, 70, 71},
    {72, 73, 74, 75, 76, 77, 78, 79, 80},

    {0, 9, 18, 27, 36, 45, 54, 63, 72},
    {1, 10, 19, 28, 37, 46, 55, 64, 73},
    {2, 11, 20, 29, 38, 47, 56, 65, 74},
    {3, 12, 21, 30, 39, 48, 57, 66, 75},
    {4, 13, 22, 31, 40, 49, 58, 67, 76},
    {5, 14, 23, 32, 41, 50, 59, 68, 77},
    {6, 15, 24, 33, 42, 51, 60, 69, 78},
    {7, 16, 25, 34, 43, 52, 61, 70, 79},
    {8, 17, 26, 35, 44, 53, 62, 71, 80}
]

ones = [
    1, 1, 1,   1, 1, 1,   1, 1, 1,
    1, 1, 1,   1, 1, 1,   1, 1, 1,
    1, 1, 1,   1, 1, 1,   1, 1, 1,

    1, 1, 1,   1, 1, 1,   1, 1, 1,
    1, 1, 1,   1, 1, 1,   1, 1, 1,
    1, 1, 1,   1, 1, 1,   1, 1, 1,

    1, 1, 1,   1, 1, 1,   1, 1, 1,
    1, 1, 1,   1, 1, 1,   1, 1, 1,
    1, 1, 1,   1, 1, 1,   1, 1, 1
]

zeroes = [
    0, 0, 0,   0, 0, 0,   0, 0, 0,
    0, 0, 0,   0, 0, 0,   0, 0, 0,
    0, 0, 0,   0, 0, 0,   0, 0, 0,

    0, 0, 0,   0, 0, 0,   0, 0, 0,
    0, 0, 0,   0, 0, 0,   0, 0, 0,
    0, 0, 0,   0, 0, 0,   0, 0, 0,

    0, 0, 0,   0, 0, 0,   0, 0, 0,
    0, 0, 0,   0, 0, 0,   0, 0, 0,
    0, 0, 0,   0, 0, 0,   0, 0, 0
]

array_ones = array("B", ones)
array_zeroes = array("B", zeroes)

class BoardState:
    def __init__(self):
        # OPEN, BLUE, ORAN
        self.cellOccupied = array_zeroes

        # 0 - 9: zero if cell empty, 1 - 9 if cell played
        self.cellValue = array_zeroes

        # is cell allowed - 1 - true, 0 - false
        self.cellAllowed = array_ones

        # OPEN, BLUE, ORAN, DONE: done means full, but not won
        self.sectionWon = [OPEN, OPEN, OPEN,    OPEN, OPEN, OPEN,    OPEN, OPEN, OPEN]

        # which section is allowed on next move
        self.sectionAllowed = [True, True, True,    True, True, True,    True, True, True]

        self.sectionNextValue = [ 1, 1, 1,   1, 1, 1,   1, 1, 1]

        self.sectionWonByConstraint = [False, False, False,   False, False, False,    False, False, False]

        self.player = BLUE
        self.gameWon = OPEN # OPEN if not won yet, DONE if a draw
        self.finalStrikeStart = -1
        self.finalStrikeEnd = -1
        self.mostRecent = 100


    def isInitialState(self) -> bool:
        for i in self.cellOccupied:
            if i != OPEN:
                return False
        return True


    def isTerminal(self) -> bool:
        return self.gameWon != OPEN


    def allLegalMoves(self) -> [(int, int)]:
        res = []

        for x in range(9):
            for y in range(9):
                if self.legalPlay(x, y):
                    res.append((x, y))
        return res


    def clone(self) -> BoardState:
        child = BoardState()

        child.cellOccupied = array("B", self.cellOccupied)
        child.cellValue = array("B", self.cellValue)
        child.cellAllowed = array("B", self.cellAllowed)

        child.sectionWon = self.sectionWon.copy()
        child.sectionAllowed = self.sectionAllowed.copy()
        child.sectionNextValue = self.sectionNextValue.copy()
        child.sectionWonByConstraint = self.sectionWonByConstraint.copy()

        child.player = self.player
        child.gameWon = self.gameWon
        child.finalStrikeStart = self.finalStrikeStart
        child.finalStrikeEnd = self.finalStrikeEnd
        child.mostRecent = self.mostRecent

        return child


    def legalPlay(self, x: int, y: int) -> bool:
        if self.gameWon != OPEN:
            return False

        if x < 0 or x > 8 or y < 0 or y > 8:
            return False

        cell = y * 9 + x
        return self.cellAllowed[cell] == 1


    # this function is very complicated. It contains basically all the game logic.
    def set(self, x, y):
        if not self.legalPlay(x, y):
            raise RuntimeError("An illegal move has been made")

        cell = y*9 + x
        section = self.ownSection2(x, y)
        self.mostRecent = cell

        # set position
        self.cellOccupied[cell] = self.player
        self.cellValue[cell] = self.sectionNextValue[section]
        self.sectionNextValue[section] += 1

        if self.won(self.player, section):
            self.sectionWon[section] = self.player
            if self.entireGameWonBy(self.player):
                self.gameWon = self.player
            elif self.entireBoardIsFull():
                self.gameWon = DONE
        elif self.full(section):
            self.sectionWon[section] = DONE
            if self.entireBoardIsFull():
                self.gameWon = DONE

        # zero out allowed cells and sections
        for i in range(9):
            self.sectionAllowed[i] = False

        for i in range(81):
            self.cellAllowed[i] = 0

        # Figure out allowed sections
        nextSection = self.targetSection(x, y)
        if self.sectionWon[nextSection] == OPEN:
            self.sectionAllowed[nextSection] = True
        else:
            for i in range(9):
                if self.sectionWon[i] == OPEN:
                    self.sectionAllowed[i] = True

        # Figure out allowed cells
        for s in range(9):
            if self.sectionAllowed[s]:
                cells = self.sectionLocations(s)
                for i in cells:
                    if self.cellOccupied[i] == OPEN and not self.sudokuConstrained(i):
                        self.cellAllowed[i] = 1

        self.recursiveConstraintProcessing()

        # finishing touches
        if self.player == BLUE:
            self.player = ORAN
        else:
            self.player = BLUE


    def recursiveConstraintProcessing(self):
        if self.isTerminal():
            return

        if not self.noAllowedCells():
            return

        # opponent can not make a play, all cells in allowed sections are either
        # occupied or prohibited by sudoku constraints. We break this dead end
        # by scoring the allowed sections for the player, and allowing opponent
        # to play in any non-won, non-full sections.

        for i in range(9):
            if self.sectionAllowed[i] == 1:
                self.sectionWon[i] = self.player
                self.sectionWonByConstraint[i] = True

        if self.entireGameWonBy(self.player):
            self.gameWon = self.player
        elif self.entireBoardIsFull():
            self.gameWon = DONE
        else:
            for i in range(9):
                self.sectionAllowed = False

            for i in range(9):
                if self.sectionWon[i] == OPEN:
                    self.sectionAllowed = True

            # figured out allowed cells
            for section in range(9):
                if self.sectionAllowed[section]:
                    cells = self.sectionLocations(section)
                    for cell in cells:
                        if self.cellOccupied[cell] == OPEN and not self.sudokuConstrained(cell):
                            self.cellAllowed[cell] = 1

        self.recursiveConstraintProcessing()


    def ownSection2(self, x: int, y: int) -> int:
        return 3*(y//3) + (x//3)


    def ownSection(self, i: int) -> int:
        y = i // 9
        x = i % 9
        return self.ownSection2(x, y)


    def targetSection(self, x: int, y: int) -> int:
        return 3*(y%3) + (x%3)


    def won(self, player: int, section: int) -> bool:
        locations = self.sectionLocations(section)
        listOfIndexes = [
            [0, 1, 2],
            [3, 4, 5],
            [6, 7, 8],
            [0, 3, 6],
            [1, 4, 7],
            [2, 5, 8],
            [0, 4, 8],
            [2, 4, 6]
        ]

        for indexes in listOfIndexes:
            if self.cellOccupied[locations[indexes[0]]] == player and self.cellOccupied[locations[indexes[1]]] == player and self.cellOccupied[locations[indexes[2]]] == player:
                return True
        return False


    def sectionLocations(self, section: int) -> [int]:
        locations = [0, 1, 2, 9, 10, 11, 18, 19, 20]

        if section < 3:
            for i in range(9):
                locations[i] += section*3
        elif section < 6:
            for i in range(9):
                locations[i] += 27 + (section-3)*3
        else:
            for i in range(9):
                locations[i] += 54 + (section-6)*3

        return locations


    def full(self, section: int) -> bool:
        locations = self.sectionLocations(section)

        for i in locations:
            if self.cellOccupied[i] == OPEN:
                return False
        return True


    def entireBoardIsFull(self) -> bool:
        for section in range(9):
            if self.sectionWon[section] == OPEN:
                return False
        return True


    def entireGameWonBy(self, player: int) -> bool:
        listOfIndexes = [
            [0, 1, 2],
            [3, 4, 5],
            [6, 7, 8],
            [0, 3, 6],
            [1, 4, 7],
            [2, 5, 8],
            [0, 4, 8],
            [2, 4, 6]
        ]

        for indexes in listOfIndexes:
            if self.sectionWon[indexes[0]] == player and self.sectionWon[indexes[1]] == player and self.sectionWon[indexes[2]] == player:
                self.finalStrikeStart = indexes[0]
                self.finalStrikeEnd = indexes[2]
                return True
        return False


    def sudokuConstrained(self, cell: int) -> bool:
        section = self.ownSection(cell)
        digit = self.sectionNextValue[section]

        for otherCell in self.peers(cell):
            if self.cellValue[otherCell] == digit:
                return True
        return False


    def peers(self, cell: int) -> {int}:
        p = set()

        for g in SUDOKU_GROUPS:
            if cell in g:
                p.union(g)

        p.remove(cell)

        for otherCell in p:
            if self.constraintRemoved(otherCell):
                p.remove(otherCell)

        return p


    def constraintRemoved(self, cell: int) -> bool:
        section = self.ownSection(cell)
        if self.sectionWon[section] == BLUE or self.sectionWon[section] == ORAN:
            return True
        return False


    def noAllowedCells(self) -> bool:
        for allowed in self.cellAllowed:
            if allowed == 1:
                return False
        return True
