import random
import esper
import pygame

from src.create.prefab_creator import create_enemy_bullet
from src.ecs.components.c_velocity import CVelocity
from src.ecs.components.c_transform import CTransform
from src.ecs.components.c_surface import CSurface
from src.ecs.components.tags.c_tag_enemy import CTagEnemy

def system_enemy_shoot(world: esper.World, enemyData: dict, bulletData: dict):
    components = world.get_components(CTransform, CVelocity, CSurface, CTagEnemy)

    transform:CTransform
    velocity:CVelocity
    surface:CSurface
    for entity, (transform, velocity, surface, enemy) in components:

        random_number = random.randint(0, enemyData["probability"])

        if random_number == 0:
            create_enemy_bullet(world, bulletData, entity)