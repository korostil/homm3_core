from dataclasses import dataclass

from homm3_core import creatures_hota


@dataclass
class BattleTile:
    """The basic movement unit for creatures"""

    x: int  # horizontal coordinate
    y: int  # vertical coordinate (starts from up and growth down)
    creature: creatures_hota.Creature = None
    can_be_visited: bool = True  # can a creature stand on this tile?
