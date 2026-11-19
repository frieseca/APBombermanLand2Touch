from __future__ import annotations

from typing import TYPE_CHECKING

from BaseClasses import Item, ItemClassification

if TYPE_CHECKING:
    from .world import BombermanLand2World


ITEM_NAME_TO_ID = {
    "Star Piece": 1,
    #"Moon Piece": 2,
    #"Sun Piece": 3,
    "Earth Piece": 4,
    #"Heart Piece": 5,
    #"Rainbow Piece": 6,
    #"Lightning Piece": 7,
    "Token": 8,
    "Triple Token": 9,

    #"Basketball Bomb": 10,
    #"Pot Bomb": 11,
    #"Fossil Bomb": 12,
    #"Magnet Bomb": 13,
    "Aqua Bomb": 14,
    #"Ruby Bomb": 15,
    #"Minecart Ticket": 16,
    #"Boat Ticket": 17,
    #"Fishing Rod": 18,
    #"Inner Tube": 19,
    "Progressive Broom": 20,
    #"Throwing Star": 21,
    #progressive broom again
    #progressive broom again
    "Regular Bomb": 24,
    #"Soccer Bomb": 25,
    #"Star Hat": 26,
    #"Evil Hat": 27,
    #"Flute Hat": 28,
    #"Pumpkin Helm": 29,
    #gap for circus queen hat
    #"Sage Hat": 31,
    #"Star Cape": 32,
    #"Evil Cape": 33,




}



DEFAULT_ITEM_CLASSIFICATIONS = {
    "Star Piece": ItemClassification.progression,
    "Regular Bomb": ItemClassification.progression,
    "Token": ItemClassification.filler,
    "Aqua Bomb": ItemClassification.progression,
    "Progressive Broom": ItemClassification.progression,
    "Earth Piece": ItemClassification.filler,
    "Triple Token": ItemClassification.filler,
}


class BombermanLand2Item(Item):
    game = "Bomberman Land Touch! 2"



def get_random_filler_item_name(world: BombermanLand2World) -> str:
    return "Token"


def create_item_with_correct_classification(world: BombermanLand2World, name: str) -> BombermanLand2Item:
    classification = DEFAULT_ITEM_CLASSIFICATIONS[name]
    return BombermanLand2Item(name,classification,ITEM_NAME_TO_ID[name],world.player)

def create_all_items(world: BombermanLand2World) -> None:
    itempool: list[Item] = [
        world.create_item("Star Piece"),
        world.create_item("Star Piece"),
        world.create_item("Star Piece"),
        world.create_item("Star Piece"),
        world.create_item("Regular Bomb"),
        world.create_item("Token"),
        world.create_item("Token"),
        world.create_item("Aqua Bomb"),
        world.create_item("Progressive Broom"),
        world.create_item("Earth Piece"),
        world.create_item("Earth Piece"),
        world.create_item("Triple Token")
    ]

    number_of_items = len(itempool)
    number_of_unfilled_locations = len(world.multiworld.get_unfilled_locations(world.player))
    needed_number_of_filler_items = number_of_unfilled_locations - number_of_items
    itempool += [world.create_filler() for _ in range(needed_number_of_filler_items)]


    world.multiworld.itempool += itempool