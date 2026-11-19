from collections.abc import Mapping
from typing import Any
from worlds.AutoWorld import World
from . import Items, Locations, Regions, Rules



class BombermanLand2World(World):
    """
    Bomberman Land 2 touch is epic sauce.
    """

    game = "Bomberman Land Touch! 2"



    location_name_to_id = Locations.LOCATION_NAME_TO_ID
    item_name_to_id = Items.ITEM_NAME_TO_ID

    origin_region_name = "Star Castle A Stage"

    def create_regions(self) -> None:
        Regions.create_and_connect_regions(self)
        Locations.create_all_locations(self)

    def set_rules(self) -> None:
        Rules.set_all_rules(self)

    def create_items(self) -> None:
        Items.create_all_items(self)

    def create_item(self, name: str) -> Items.BombermanLand2Item:
        return Items.create_item_with_correct_classification(self,name)

    def get_filler_item_name(self) -> str:
        return Items.get_random_filler_item_name(self)
"""
    def fill_slot_data(self) -> Mapping[str, Any]:
        return self.options.as_dict(

        )
"""