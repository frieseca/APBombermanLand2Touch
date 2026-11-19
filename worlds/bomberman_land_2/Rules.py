from __future__ import annotations

from typing import TYPE_CHECKING

from rule_builder.options import OptionFilter
from rule_builder.rules import Has, HasAll, Rule

##from .options import HardMode

if TYPE_CHECKING:
    from .world import BombermanLand2World

HAS_KEY = Has("Key")




def set_all_rules(world: BombermanLand2World) -> None:
    set_all_entrance_rules(world)
    set_all_location_rules(world)
    set_completion_condition(world)


def set_all_entrance_rules(world: BombermanLand2World) -> None:
    star_castle_a_gate = world.get_entrance("Star Castle A Gate")
    star_b_to_c = world.get_entrance("Star B to C")

    star1 = Has("Star Piece")
    world.set_rule(star_castle_a_gate,star1)
    has_bomb = Has("Regular Bomb")
    world.set_rule(star_b_to_c,has_bomb)


def set_all_location_rules(world: BombermanLand2World) -> None:
    star_fortune_gate = world.get_location("Fortune Token Star")
    star3 = Has("Star Piece", count=3)
    world.set_rule(star_fortune_gate,star3)

    has_broom = Has("Progressive Broom")
    buried_chest = world.get_location("Star C Buried Chest")
    buried_bomb = world.get_location("Buried Aqua Bomb")
    world.set_rule(buried_chest,has_broom)
    world.set_rule(buried_bomb,has_broom)
    has_aqua_bomb = Has("Aqua Bomb")
    help_aqua = world.get_location("Aqua Helped")
    world.set_rule(help_aqua, has_aqua_bomb)

def set_completion_condition(world: BombermanLand2World) -> None:
    world.set_completion_rule(Has("Victory"))