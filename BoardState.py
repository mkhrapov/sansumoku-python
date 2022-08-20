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
        self.sectionWon: [OPEN, OPEN, OPEN,    OPEN, OPEN, OPEN,    OPEN, OPEN, OPEN]

        # which section is allowed on next move
        self.sectionAllowed: [True, True, True,    True, True, True,    True, True, True]

        self.sectionNextValue: [ 1, 1, 1,   1, 1, 1,   1, 1, 1]

        self.sectionWonByConstraint: [False, False, False,   False, False, False,    False, False, False]

        self.player = BLUE
        self.gameWon = OPEN # OPEN if not won yet, DONE if a draw
        self.finalStrikeStart = -1
        self.finalStrikeEnd = -1
        self.mostRecent = 100

