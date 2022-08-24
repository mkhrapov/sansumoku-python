import random


def initialMove() -> (int, int):
    return random.choice([
        (3, 3), (3, 5), (5, 3), (5, 5), (4, 4)
    ])