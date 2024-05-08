import esper
import pygame

from src.ecs.components.c_transform import CTransform
from src.ecs.components.c_surface import CSurface


def system_player_stop(world:esper.World,  screen:pygame.Surface, player_entity:int) -> None:
    screen_rect = screen.get_rect()
    
    player_transform = world.component_for_entity(player_entity, CTransform)
    player_surface = world.component_for_entity(player_entity, CSurface)

    player_rect = CSurface.get_area_relative(player_surface.area, player_transform.pos)

    if player_rect.left < 0 or player_rect.right > screen_rect.right:
        player_rect.clamp_ip(screen_rect)
        player_transform.pos.x = player_rect.x
    
    if player_rect.top < 0 or player_rect.bottom > screen_rect.bottom:
        player_rect.clamp_ip(screen_rect)
        player_transform.pos.y = player_rect.y