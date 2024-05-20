import random
import pygame
import esper

from src.ecs.components.c_animation import CAnimation
from src.ecs.components.c_alien import CAlien, AlienState
from src.ecs.components.c_surface import CSurface
from src.ecs.components.c_transform import CTransform
from src.ecs.components.c_velocity import CVelocity
from src.engine.service_locator import ServiceLocator

def system_alien_state(world:esper.World, player_entity: int, enemy_data:dict, window_data:dict) -> None:
    components = world.get_components(CAlien, CTransform, CVelocity)

    pl_transfotm = world.component_for_entity(player_entity, CTransform)

    for _, (alien, transform, velocity) in components:
        
        if alien.state == AlienState.MOV:
            _do_mov_state(alien, transform, velocity, enemy_data["probability_jump"], enemy_data["jump_distance"])
        elif alien.state == AlienState.CHASE:
            _do_chase_state(alien, transform, velocity, pl_transfotm, enemy_data["chase_velocity"], window_data["size"]["h"])
        elif alien.state == AlienState.RETURN:
            _do_return_state(alien, transform, velocity, enemy_data["chase_velocity"])



def _do_mov_state(alien: CAlien, transform: CTransform, velocity: CVelocity, probability: int, jump_distance: int) -> None:

    random_number = random.randint(0, probability)

    if random_number == 0:
        alien.state = AlienState.CHASE
        velocity.vel.y = velocity.vel.y + jump_distance
        alien.posObj = transform.pos.copy()


def _do_chase_state(alien: CAlien, transform: CTransform, velocity: CVelocity, pl_transform: CTransform, chase_velocity:int, window_h: int) -> None:

    # rotar si necesario para estar al revez

    # change vel a jugador

    velNew = pl_transform.pos - transform.pos
    velNew = velNew.normalize() * chase_velocity
    velNew.y = chase_velocity 

    velocity.vel = velNew

    # if tocar fondo -> saltar arriba

    if transform.pos.y > window_h:
        alien.state = AlienState.RETURN
        transform.pos.y = 1


def _do_return_state(alien: CAlien, transform: CTransform, velocity: CVelocity, chase_velocity:int) -> None:

    # rotar si necesario para estar al derecho

    # change vel a origen

    velNew = alien.posObj - transform.pos
    velNew = velNew.normalize() * chase_velocity

    velocity.vel = velNew

    # if tocar origen -> cambiar a mov

    #pitagoras
    if transform.pos.distance_squared_to(alien.posObj) < 2:
        alien.state = AlienState.MOV
        velocity.vel.x = alien.velActual_x * 2
        velocity.vel.y = 0
        transform.pos.y = alien.posObj.y
        transform.pos.x = alien.posObj.x
