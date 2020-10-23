import pytest

from homm3_core.adventure_map import AdventureMap, MapTile


@pytest.mark.parametrize(
    'width,height,basis,expected_width,expected_height',
    [
        (144, 144, None, 144, 144),     # by number of tiles
        (1234, 345, MapTile(x=456, y=169, size=35), 36, 10)     # by pixels and basis tile
    ]
)
def test_adventure_map_creation(width, height, basis, expected_width, expected_height):
    adventure_map = AdventureMap(width, height, basis)

    assert adventure_map.width == expected_width
    assert adventure_map.height == expected_height


@pytest.mark.parametrize(
    'objects,expected_map_tile',
    [
        ([('Gold Mine', (0, 0, 128, 64)), ('Crystal', (128, 128, 192, 192))], MapTile(x=128, y=128, size=64)),
        ([('Gold Mine', (0, 0, 128, 64))], None),
        ([], None),
    ]
)
def test_basis_tile_definition(objects, expected_map_tile):
    basis = AdventureMap.define_basis_tile(objects)

    if expected_map_tile:
        assert basis.x == expected_map_tile.x
        assert basis.y == expected_map_tile.y
        assert basis.size == expected_map_tile.size
    else:
        assert basis is None


def test_adventure_map_build():
    adventure_map = AdventureMap(
        width=360,
        height=190,
        basis_tile=MapTile(x=115, y=150, size=35),
        objects=[
            ('Library of Enlightenment', (185, 45, 325, 115)),
            ('Naga Bank', (80, 115, 150, 150)),
            ("Pandora's Box", (115, 150, 140, 185)),
            ('Rally Flag', (45, 45, 115, 80))
        ]
    )

    rally_flag = AdventureMap.OBJECTS['Rally Flag']
    pandora = AdventureMap.OBJECTS["Pandora's Box"]
    naga_bank = AdventureMap.OBJECTS['Naga Bank']
    library = AdventureMap.OBJECTS['Library of Enlightenment']

    assert adventure_map.array == [
        [None for _ in range(11)],
        [
            None, MapTile(x=1, y=1, map_object=rally_flag, size=35, can_be_visited=False),
            MapTile(x=2, y=1, map_object=rally_flag, size=35), None, None, None, None,
            MapTile(x=7, y=1, size=35, map_object=library, can_be_visited=False),
            MapTile(x=8, y=1, size=35, map_object=library, can_be_visited=False), None, None
        ],
        [None for _ in range(5)] + [
            MapTile(x=5, y=2, size=35, map_object=library, can_be_visited=False),
            MapTile(x=6, y=2, size=35, map_object=library, can_be_visited=False),
            MapTile(x=7, y=2, size=35, map_object=library, can_be_visited=True),
            MapTile(x=8, y=2, size=35, map_object=library, can_be_visited=False), None, None
        ],
        [
            None, None, MapTile(x=2, y=3, size=35, map_object=naga_bank, can_be_visited=True),
            MapTile(x=3, y=3, size=35, map_object=naga_bank, can_be_visited=False)] + [None for _ in range(7)],
        [
            None, None, None, MapTile(x=3, y=4, size=35, map_object=pandora, can_be_visited=True)
        ] + [None for _ in range(7)],
        [None for _ in range(11)]
    ]
