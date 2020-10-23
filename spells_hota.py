import json
import os
from dataclasses import dataclass

AIR_SCHOOL = 1
EARTH_SCHOOL = 2
FIRE_SCHOOL = 3
WATER_SCHOOL = 4
ALL_SCHOOLS = 5

COMBAT_TYPE = 1
ADVENTURE_TYPE = 2


SCHOOLS_CHOICES = [
    (AIR_SCHOOL, 'School of air magic'),
    (EARTH_SCHOOL, 'School of earth magic'),
    (FIRE_SCHOOL, 'School of fire magic'),
    (WATER_SCHOOL, 'School of water magic'),
    (ALL_SCHOOLS, 'Available in all magic schools'),
]

# all the available spells
SPELLS = {}


@dataclass
class Spell:
    """Magic that can be used in combat or on the adventure map"""

    title: str
    mana: int
    image: str
    level: int
    school: int     # what magic school does the spell belong to?
    duration: int = 1   # how long (or combat rounds) does the spell work?
    type: bool = True   # True - during combat, False - on the adventure map


with open(os.path.dirname(os.path.abspath(__file__)) + '/data/spells_hota.json', 'r') as file:
    for title, spell in json.loads(file.read()).items():
        SPELLS[title] = Spell(
            title=title,
            **{
                field: spell[field]
                for field in ['mana', 'image', 'level', 'school']
            }
        )
