import esper
import pygame

from src.ecs.components.c_velocity import CVelocity
from src.ecs.components.c_transform import CTransform
from src.ecs.components.c_alien import AlienState, CAlien

def system_update_posObj(world:esper.World, deltatime: float) -> None:
    components = world.get_components(CTransform, CVelocity, CAlien)

    transform:CTransform
    velocity:CVelocity
    alien:CAlien
    for entity, (transform, velocity, alien) in components:
        
        alien.posObj.x += alien.velActual_x * deltatime
