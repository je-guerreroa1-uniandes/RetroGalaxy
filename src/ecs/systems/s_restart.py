import esper
import pygame

from src.ecs.components.c_transform import CTransform
from src.ecs.components.c_surface import CSurface
from src.ecs.components.c_star import CStar
from src.ecs.components.tags.c_tag_enemy import CTagEnemy


def system_reset(world:esper.World) -> None:
    components = world.get_components(CSurface, CTagEnemy)

    for entity, ( surface, ene) in components:

        world.delete_entity(entity)