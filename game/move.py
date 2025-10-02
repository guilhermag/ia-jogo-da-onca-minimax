from dataclasses import dataclass
from typing import Tuple

@dataclass(frozen=True)
class Move:
    player_type: str
    move_type: str
    number_of_jumps: int
    origin: Tuple[str, str]
    destination: Tuple[str, ...]


    @classmethod
    def from_string(cls, move_str: str) -> "Move":
        result = move_str.split()
        player_type = result[0]
        move_type = result[1]
        number_of_jumps = 0
        if move_type == 's':
            number_of_jumps = int(result[2])
            origin = (result[3], result[4])
            destination = tuple(result[5:])
        else:
            origin = (result[2], result[3])
            destination = tuple(result[4:])

        return cls(
            player_type=player_type,
            move_type=move_type,
            number_of_jumps=number_of_jumps,
            origin=origin,
            destination=destination
        )
