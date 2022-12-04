from dataclasses import dataclass
from enum import IntEnum


class Move(IntEnum):
    rock = 1
    paper = 2
    scissors = 3


@dataclass(frozen=True)
class Round:
    their_move: Move
    my_move: Move


def score_round(round: Round) -> int:
    outcome_points: int
    their_move = round.their_move
    my_move = round.my_move

    if their_move == my_move:
        # Draw
        outcome_points = 3
    elif their_move % len(Move) + 1 == my_move:
        # Win
        outcome_points = 6
    else:
        # Loss
        outcome_points = 0

    return outcome_points + my_move
