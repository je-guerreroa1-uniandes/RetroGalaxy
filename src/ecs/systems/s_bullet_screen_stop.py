import esper
import pygame

from src.ecs.components.c_transform import CTransform
from src.ecs.components.c_surface import CSurface
from src.ecs.components.tags.c_tag_bullet import CTagBullet


def system_bullet_screen_stop(world:esper.World,  screen:pygame.Surface) -> None:
    components = world.get_components(CTransform, CSurface, CTagBullet)
    screen_rect = screen.get_rect()

    transform:CTransform
    surface:CSurface
    for entity, (transform, surface, _) in components:

        cuad_rect = CSurface.get_area_relative(surface.area, transform.pos)

        if cuad_rect.left < 0 or cuad_rect.right > screen_rect.right:
            world.delete_entity(entity)
            continue

        if cuad_rect.top < 0 or cuad_rect.bottom > screen_rect.bottom:
            world.delete_entity(entity)
            continue