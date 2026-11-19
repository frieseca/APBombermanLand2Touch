from __future__ import annotations

from typing import TYPE_CHECKING

from BaseClasses import ItemClassification, Location

from . import Items

if TYPE_CHECKING:
    from .world import BombermanLand2World


LOCATION_NAME_TO_ID = {
    "Jumping Rope": 1,
    "Bending Spoons": 2,
    "Star Castle A Chest 1": 3,
    "Star Castle A Chest 2": 4,
    "Bought Worn Broom": 5,
    "Star B Shakeable Tree": 6,
    "Acrobat Wheel": 7,
    "Bomber House Star": 8,
    "Fortune Token Star": 9,
    "Buried Aqua Bomb": 10,
    "Star C Buried Chest": 11,
    "Reel 'Em In": 12
}


class BombermanLand2Location(Location):
    game = "Bomberman Land Touch! 2"


def get_location_names_with_ids(location_names: list[str]) -> dict[str, int | None]:
    return {location_name: LOCATION_NAME_TO_ID[location_name] for location_name in location_names}



def create_all_locations(world: BombermanLand2World) -> None:
    create_regular_locations(world)
    create_events(world)

def create_regular_locations(world: BombermanLand2World) -> None:
    star_castle_a_stage = world.get_region("Star Castle A Stage")
    star_aab = world.get_region("Star AAB")
    star_c = world.get_region("Star C")

    star_castle_a_stage_locations = get_location_names_with_ids(["Jumping Rope", "Bending Spoons"])
    star_castle_a_stage.add_locations(star_castle_a_stage_locations, BombermanLand2Location)

    star_aab_locations = get_location_names_with_ids(["Star Castle A Chest 1", "Star Castle A Chest 2", "Bought Worn Broom", "Star B Shakeable Tree", "Acrobat Wheel", "Bomber House Star", "Fortune Token Star"])
    star_aab.add_locations(star_aab_locations,BombermanLand2Location)

    star_c_locations = get_location_names_with_ids(["Buried Aqua Bomb", "Star C Buried Chest", "Reel 'Em In"])
    star_c.add_locations(star_c_locations,BombermanLand2Location)


def create_events(world: BombermanLand2World) -> None:
    star_c = world.get_region("Star C")
    star_c.add_event(
        "Aqua Helped", "Victory", location_type=BombermanLand2Location, item_type=Items.BombermanLand2Item
    )