import json
import os
from dataclasses import dataclass


UNKNOWN = 0
FEW = 1
SEVERAL = 2
PACK = 3
LOTS = 4
HORDE = 5
THRONG = 6
SWARM = 7
ZOUNDS = 8
LEGION = 9


ARMY_NUMBER = {
    FEW: (1, 4),
    SEVERAL: (5, 9),
    PACK: (10, 19),
    LOTS: (20, 49),
    HORDE: (50, 99),
    THRONG: (100, 249),
    SWARM: (250, 499),
    ZOUNDS: (500, 999),
    LEGION: (1000, 9999)
}


ARMY_NUMBER_CHOICES = [
    (FEW, 'Few (1-4)'),
    (SEVERAL, 'Several (5-9)'),
    (PACK, 'Pack (10-19)'),
    (LOTS, 'Lots (20-49)'),
    (HORDE, 'Horde (50-99)'),
    (THRONG, 'Throng (100-249)'),
    (SWARM, 'Swarm (250-499)'),
    (ZOUNDS, 'Zounds (500-999)'),
    (LEGION, 'Legion (1000-9999)')
]


def get_army_key(number):
    for key, (min_value, max_value) in ARMY_NUMBER.items():
        if min_value <= number <= max_value:
            return key
    return 0


@dataclass
class Creature:
    name: str
    town: int   #
    level: str
    portrait: str
    view: str
    attack: int
    defense: int
    damage_min: int
    damage_max: int
    health: int
    speed: int
    growth: int
    value: int
    cost: dict
    shots: int = None


class ArmyStack:
    """Creatures in the hero army (with advantages from hero skills and stats)"""

    def __init__(self, creature: Creature, number: int):
        self.creature = creature
        self.number = number


# all the available creatures
CREATURES = {}

with open(os.path.dirname(os.path.abspath(__file__)) + '/data/spells_hota.json', 'r') as file:
    for name, attributes in json.loads(file.read()).items():
        CREATURES[name] = Creature(
            name=name,
            **{
                field: attributes[field]
                for field in [
                    'town', 'level', 'portrait', 'view', 'attack', 'defense', 'damage_min', 'damage_max', 'health',
                    'speed', 'growth', 'value', 'cost', 'shots'
                ]
            }
        )
