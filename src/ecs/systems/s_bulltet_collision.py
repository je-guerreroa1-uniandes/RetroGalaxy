import pygame
import esper
from src.create.prefab_creator import create_explosion
from src.ecs.components.c_surface import CSurface
from src.ecs.components.c_transform import CTransform
from src.ecs.components.tags.c_tag_enemy import CTagEnemy
from src.ecs.components.tags.c_tag_bullet import CTagBullet
from src.ecs.components.c_game_state import  GameState
from src.engine.service_locator import ServiceLocator

def system_bullet_collision(world: esper.World, explosion_data: dict, player_entity: int, screen: pygame.Surface):
    enemies = world.get_components(CSurface, CTransform, CTagEnemy)
    bullets = world.get_components(CSurface, CTransform, CTagBullet)

    pl_t = world.component_for_entity(player_entity, CTransform)
    pl_s = world.component_for_entity(player_entity, CSurface)

    pl_rect = CSurface.get_area_relative(pl_s.area, pl_t.pos)

    ret = False

    if len(enemies) == 0:
        return GameState.CHANGE_LEVEL

    for bullet_entity, (bullet_surface, bullet_transform, bullet_tag) in bullets:

        if bullet_tag.type == "player":
            

            bullet_rect = bullet_surface.area.copy()
            bullet_rect.topleft = bullet_transform.pos

            for enemy_entity, (enemy_surface, enemy_transform, enemy_tag) in enemies:

                enemy_rect = CSurface.get_area_relative(enemy_surface.area, enemy_transform.pos)

                if bullet_rect.colliderect(enemy_rect):
                    create_explosion(world, enemy_transform.pos, explosion_data["enemy"], "enemy")
                    world.delete_entity(bullet_entity)
                    world.delete_entity(enemy_entity)
                    ServiceLocator.data_service.add_points(100)
                    
        
        elif bullet_tag.type == "enemy":
            bullet_rect = bullet_surface.area.copy()
            bullet_rect.topleft = bullet_transform.pos

            player_surface, player_transform = world.component_for_entity(player_entity, CSurface), world.component_for_entity(player_entity, CTransform)
            player_rect = CSurface.get_area_relative(player_surface.area, player_transform.pos)

            if bullet_rect.colliderect(player_rect):
                pos_copy = player_transform.pos.copy()
                pos_copy.x -= player_surface.area.width / 2
                pos_copy.y -= player_surface.area.height / 2
                create_explosion(world, pos_copy, explosion_data["player"], "player")
                world.delete_entity(bullet_entity)
                player_transform.pos.x = (screen.get_width() / 2) - (player_surface.area.width / 2)
                ret = True

    for enemy_entity, (enemy_surface, enemy_transform, enemy_tag) in enemies:

        enemy_rect = CSurface.get_area_relative(enemy_surface.area, enemy_transform.pos)
        
        player_surface, player_transform = world.component_for_entity(player_entity, CSurface), world.component_for_entity(player_entity, CTransform)
        player_rect = CSurface.get_area_relative(player_surface.area, player_transform.pos)

        if enemy_rect.colliderect(player_rect):
            pos_copy = player_transform.pos.copy()
            pos_copy.x -= player_surface.area.width / 2
            pos_copy.y -= player_surface.area.height / 2
            create_explosion(world, pos_copy, explosion_data["player"], "player")
            player_transform.pos.x = (screen.get_width() / 2) - (player_surface.area.width / 2)
            world.delete_entity(enemy_entity)
            ret = True

    if ret:
        return GameState.DIED
    else:
        return GameState.UNPAUSED
        

                
