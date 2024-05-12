import random
import pygame
import esper
from src.ecs.components.c_animation import CAnimation
from src.ecs.components.c_explosion import CExplosion
from src.ecs.components.c_input_command import CInputCommand
from src.ecs.components.c_player_state import CPlayerState
from src.ecs.components.c_surface import CSurface
from src.ecs.components.c_transform import CTransform
from src.ecs.components.c_velocity import CVelocity
from src.ecs.components.tags.c_tag_bullet import CTagBullet
from src.ecs.components.tags.c_tag_enemy import CTagEnemy
from src.ecs.components.tags.c_tag_player import CTagPlayer
from src.engine.service_locator import ServiceLocator


#NA
def create_square(ecs_world:esper.World, size:pygame.Vector2,
                    pos:pygame.Vector2, vel:pygame.Vector2, col:pygame.Color):
    cuad_entity = ecs_world.create_entity()
    ecs_world.add_component(cuad_entity,
                CSurface(size, col))
    ecs_world.add_component(cuad_entity,
                CTransform(pos))
    ecs_world.add_component(cuad_entity,
                CVelocity(vel))
def crear_cuadrado(ecs_world:esper.World, size:pygame.Vector2, pos:pygame.Vector2, 
                   vel:pygame.Vector2, col:pygame.Color) -> int:
    
    cuad_entity = ecs_world.create_entity()

    ecs_world.add_component(cuad_entity, 
                CSurface(size, col))
       
    ecs_world.add_component(cuad_entity,
                CTransform(pos))
        
    ecs_world.add_component(cuad_entity,
                CVelocity(vel))
    
    return cuad_entity

def crear_texto(ecs_world:esper.World, text:str, pos:pygame.Vector2, color: pygame.Color, size: int) -> int:

    entity = ecs_world.create_entity()
    font = ServiceLocator.fonts_service.get("assets/fnt/PressStart2P.ttf", size)

    ecs_world.add_component(entity, CTransform(pos))
    ecs_world.add_component(entity, CSurface.from_text(text, font, color))

    return entity

def create_sprite(ecs_world:esper.World, pos:pygame.Vector2, vel:pygame.Vector2,
                  surface:pygame.Surface) -> int:
    
    sprite_entity = ecs_world.create_entity()
    
    ecs_world.add_component(sprite_entity, CTransform(pos))
    ecs_world.add_component(sprite_entity, CVelocity(vel))

    ecs_world.add_component(sprite_entity, CSurface.from_surface(surface))

    return sprite_entity

# crear espesificos


def create_explosion(ecs_world:esper.World, pos:pygame.Vector2, explotion_data:dict) -> int:

    explotion_surface = ServiceLocator.images_service.get(explotion_data["image"])

    explotion_entity = create_sprite(ecs_world, pos, pygame.Vector2(0,0), explotion_surface)

    ecs_world.add_component(explotion_entity, CAnimation(explotion_data["animations"]))
    ecs_world.add_component(explotion_entity, CExplosion())

    ServiceLocator.sounds_service.play(explotion_data["sound"])

    return explotion_entity

def create_player(world: esper.World, player_info: dict, player_lvl_info: dict, screen:pygame.Surface) -> int:
    player_sprite = ServiceLocator.images_service.get(player_info["image"])
    size = player_sprite.get_size()
    size = (size[0] / player_info["animations"]["number_frames"], size[1])
    if player_lvl_info.get("use_default", False):
        pos = pygame.Vector2(
            (screen.get_width() / 2) - (size[0] / 2),
            screen.get_height() - size[1] - 10
        )
    else:
        pos = pygame.Vector2(
            player_lvl_info["position"]["x"] - (size[0] / 2),
            player_lvl_info["position"]["y"] - (size[1] / 2)
        )

    vel = pygame.Vector2(0, 0)

    player_entity = create_sprite(world,
                                  pos,
                                  vel,
                                  player_sprite
                                  )

    world.add_component(player_entity, CTagPlayer())
    # world.add_component(player_entity, CAnimation(player_info["animations"]))
    world.add_component(player_entity, CPlayerState())
    return player_entity

def create_input_player(world: esper.World):
    input_left = world.create_entity()
    input_right = world.create_entity()
    input_up = world.create_entity()
    input_down = world.create_entity()
    input_fire = world.create_entity()
    input_pause = world.create_entity()
    world.add_component(input_left, CInputCommand("PLAYER_LEFT", pygame.K_LEFT))
    world.add_component(input_right, CInputCommand("PLAYER_RIGHT", pygame.K_RIGHT))
    world.add_component(input_up, CInputCommand("PLAYER_UP", pygame.K_UP))
    world.add_component(input_down, CInputCommand("PLAYER_DOWN", pygame.K_DOWN))
    world.add_component(input_fire, CInputCommand("PLAYER_FIRE", pygame.K_SPACE))
    world.add_component(input_pause, CInputCommand("PAUSE", pygame.K_p))


def create_bullet_square(ecs_world:esper.World, bullet_data:dict, player_entity:int, level_data:dict) -> int:

        bullets = ecs_world.get_component(CTagBullet)
        cont = 0
        for _, (tag) in bullets:
            if tag.type == 1:
                cont += 1

        if cont >= level_data["player_spawn"]["max_bullets"]:
            return None

        bullet_surface = ServiceLocator.images_service.get(bullet_data["image"])
        bullet_size = bullet_surface.get_rect().size

        player_c_t = ecs_world.component_for_entity(player_entity, CTransform)
        player_c_s = ecs_world.component_for_entity(player_entity, CSurface)

        player_area = player_c_s.area.size

        
        pos = pygame.Vector2(player_c_t.pos.x + player_area[0]/2 - bullet_size[0]/2,
                            player_c_t.pos.y + player_area[1]/2 - bullet_size[1]/2)

        vel = pygame.mouse.get_pos()
        vel = vel - pos

        player_pos_center = pygame.Vector2(player_c_t.pos.x + (player_area[0]/2), 
                                   player_c_t.pos.y + (player_area[1]/2))
        vel = pygame.mouse.get_pos()
        vel = vel - player_pos_center

        vel = vel.normalize() * bullet_data["velocity"]
    
        bullet_entity = create_sprite(ecs_world, pos, vel, bullet_surface)
    
        ecs_world.add_component(bullet_entity, CTagBullet(1))

        ServiceLocator.sounds_service.play(bullet_data["sound"])

        return bullet_entity