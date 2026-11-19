from __future__ import annotations

from typing import TYPE_CHECKING

from BaseClasses import Entrance, Region
if TYPE_CHECKING:
    from .world import BombermanLand2World

def create_and_connect_regions(world: BombermanLand2World) -> None:
    create_all_regions(world)
    connect_regions(world)

def create_all_regions(world: BombermanLand2World) -> None:
    star_castle_a_stage = Region("Star Castle A Stage", world.player, world.multiworld)
    star_aab = Region("Star AAB", world.player, world.multiworld)
    star_c = Region("Star C", world.player, world.multiworld)

    regions = [star_castle_a_stage,star_aab,star_c]

    world.multiworld.regions += regions


def connect_regions(world: BombermanLand2World) -> None:
    star_castle_a_stage = world.get_region("Star Castle A Stage")
    star_aab = world.get_region("Star AAB")
    star_c = world.get_region("Star C")

    star_castle_a_stage.connect(star_aab, "Star Castle A Gate")
    star_aab.connect(star_c, "Star B to C")
