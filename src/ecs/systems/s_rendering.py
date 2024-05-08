import esper
import pygame

from src.ecs.components.c_surface import CSurface
from src.ecs.components.c_transform import CTransform

def system_rendering(world:esper.World, screen:pygame.Surface) -> None:
    components = world.get_components(CTransform, CSurface)

    transform:CTransform
    surface:CSurface
    for entity, (transform, surface) in components:
        screen.blit(surface.surf, transform.pos, area=surface.area)


