import esper
import pygame

from src.ecs.components.c_velocity import CVelocity
from src.ecs.components.c_transform import CTransform
from src.ecs.components.c_surface import CSurface
from src.ecs.components.tags.c_tag_enemy import CTagEnemy
from src.ecs.components.c_alien import AlienState, CAlien

def system_enemy_screen_bounce(world: esper.World, window_data: dict) -> None:
    components = world.get_components(CTransform, CVelocity, CSurface, CTagEnemy, CAlien)

    max_x = window_data["size"]["w"] - window_data["enemy_padding_x"]
    min_x = window_data["enemy_padding_x"]

    enemy_max_x = 0
    enemy_min_x = 10000

    transform:CTransform
    velocity:CVelocity
    surface:CSurface
    enemy:CAlien
    for entity, (transform, velocity, surface, enemy, alien) in components:

        if alien.state == AlienState.MOV:

            enemy_rect = CSurface.get_area_relative(surface.area, transform.pos)

            enemy_max_x = max(enemy_max_x, transform.pos.x + enemy_rect.width)
            enemy_min_x = min(enemy_min_x, transform.pos.x)

    
    if enemy_max_x > max_x or enemy_min_x < min_x:

        for entity, (transform, velocity, surface, enemy, alien) in components:

            if alien.state == AlienState.MOV:
                
                velocity.vel.x *= -1
        
            alien.velActual_x *= -1
            
            