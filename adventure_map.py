import json
import os
from dataclasses import dataclass

import numpy as np

TERRAIN_MAP = {
    'Grass': 0,
    'Highlands': 1,
    'Dirt': 2,
    'Lava': 3,
    'Subterranean': 4,
    'Rock': 5,
    'Rough': 6,
    'Wasteland': 7,
    'Sand': 8,
    'Snow': 9,
    'Swamp': 10,
    'Water': 11,
}


pandoras = {
    '5ke': 6000,
    '10ke': 12000,
    '15ke': 18000,
    '20ke': 24000,
    '5kg': 5000,
    '10kg': 10000,
    '15kg': 15000,
    '20kg': 20000,
    '1lvl': 5000,
    '2lvl': 7500,
    '3lvl': 10000,
    '4lvl': 12500,
    '5lvl': 15000,
    'all_air': 15000,
    'all_fire': 15000,
    'all_water': 15000,
    'all_earth': 15000,
    'all_magic': 30000
}


# TODO maybe separate to all instances?
#  arena = AdventureMapObject(title='Creature dwelling')
# TODO separate
#  arena = AdventureMapObject(title='Town')
#  arena = AdventureMapObject(title='Artifact')
@dataclass
class AdventureMapObject:
    """"""

    title: str  # object name
    index: int  # index (to track)
    can_be_basis: bool  # object can be a basis tile
    visiting_scheme: list
    rmg_value: int


@dataclass
class MapTile:
    """The basic movement unit for heroes"""

    x: int  # horizontal coordinate
    y: int  # vertical coordinate (starts from up and growth down)
    size: int = 64  # width and height (in pixels)
    terrain: int = None     # what kind of terrain this tile placed on?
    map_object: AdventureMapObject = None   # adventure map object (or some part of it) or creature
    can_be_visited: bool = True     # can a hero stand on this tile?


class AdventureMap:
    """If an object is None, then it's terra incognita

    self.width: number of tiles horizontally
    self.height: number of tiles vertically
    self.array: matrix representing adventure map
    self.basis_tile:
    """

    # all possible adventure map objects with neutral creatures
    OBJECTS = {
        title: AdventureMapObject(
            title=title,
            index=map_object['index'],
            can_be_basis=map_object.get('can_be_basis', False),
            visiting_scheme=map_object.get('visiting_scheme', []),
            rmg_value=map_object.get('rmg_value', 0)
        )
        for title, map_object in json.loads(
            open(os.path.dirname(os.path.abspath(__file__)) + '/data/adventure_map_objects_hota.json', 'r').read()
        ).items()
    }

    def __init__(self, width, height, basis_tile: MapTile = None, objects: list = None):
        """Constructs an adventure map by width and height.
        By default the whole map is covered by terra incognita

        Args:
            width: number of tiles (or size in pixels) horizontally
            height: number of tiles (or size in pixels) vertically
            basis_tile: basis tile that serves as an anchor during map constructing
            objects: list of 2-tuples consisting an of object name and its position e.g. ('Gold Mine', (0, 0, 128, 64)
        """

        if objects and not basis_tile:
            self.basis_tile = self.define_basis_tile(objects)
        elif basis_tile:
            self.basis_tile = basis_tile
        else:
            self.basis_tile = MapTile(x=0, y=0, size=64)

        if width <= 144 or height <= 144:
            self.width = width
            self.height = height
        else:
            width = width / self.basis_tile.size
            height = height / self.basis_tile.size
            self.width = int(width) if width.is_integer() else int(width) + 1
            self.height = int(height) if height.is_integer() else int(height) + 1

        self.array = [
            [None for _ in range(self.width)]
            for _ in range(self.height)
        ]
        self.objects = {}   # dict of all objects presented on this map

        if objects:
            self._build(objects)

    # TODO refactor this
    def __array__(self):
        return np.array([
            [cell.index if cell else -1 for cell in row]
            for row in self.array
        ])

    @classmethod
    def define_basis_tile(cls, objects: list) -> MapTile:
        """By given picture find x, y coordinates and size of basis tile

        Args:
            objects: list of 2-tuples consisting an of object name and its position e.g. ('Gold Mine', (0, 0, 128, 64)

        Returns:
            MapTile:
        """

        # TODO what if there is non of "can_be_basis" tile

        for map_object, (x0, y0, x1, y1) in objects:
            if cls.OBJECTS[map_object].can_be_basis:
                return MapTile(x=x0, y=y0, size=x1 - x0)

    def _build(self, objects: list) -> None:
        """Place objects on a matrix

        Args:
            objects: list of 2-tuples consisting an of object name and its position e.g. ('Gold Mine', (0, 0, 128, 64)

        Returns:

        """

        shift_x = self.basis_tile.x % self.basis_tile.size
        shift_y = self.basis_tile.y % self.basis_tile.size

        for map_object, (x0, y0, _, _) in objects:
            map_object = self.OBJECTS[map_object]
            x = int((shift_x + x0) / self.basis_tile.size)
            y = int((shift_y + y0) / self.basis_tile.size)

            for idx_y, vertical in enumerate(map_object.visiting_scheme):
                for idx_x, horizontal in enumerate(vertical):
                    # "-1" - means tile belongs to rectangle in which the object is inscribed, but not belongs to
                    # the object
                    if horizontal != -1:
                        # TODO why is y first?
                        self.array[y + idx_y][x + idx_x] = MapTile(
                            x=x + idx_x,
                            y=y + idx_y,
                            size=self.basis_tile.size,
                            map_object=map_object,
                            can_be_visited=horizontal == 1
                        )

            self.objects.setdefault(map_object, []).append((x, y))

    def find_objects(self, name: str) -> list:
        # TODO not implement
        pass
