import esper
import pygame

from src.ecs.components.c_velocity import CVelocity
from src.ecs.components.c_transform import CTransform

def system_movement(world:esper.World, deltatime: float) -> None:
    components = world.get_components(CTransform, CVelocity)

    transform:CTransform
    velocity:CVelocity
    for entity, (transform, velocity) in components:
        transform.pos += velocity.vel * deltatime
