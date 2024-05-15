

import pygame
import esper
from src.ecs.components.c_star import CStar
from src.ecs.components.c_surface import CSurface


def system_star_blink(world: esper.World, delta_time: float) -> None:
    components = world.get_components(CStar, CSurface)

    star:CStar
    surface:CSurface
    for entity, (star, surface) in components:
        star.timeAlive += delta_time
        if star.timeAlive >= star.time:
            star.timeAlive = 0
            if star.state == 1:
                surface.surf.fill(pygame.Color(0, 0, 0))
                star.state = 0
            else:
                surface.surf.fill(star.color)
                star.state = 1
            world.add_component(entity, surface)
            world.add_component(entity, star)