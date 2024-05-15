import random
import pygame
import esper
from src.create.prefab_creator import create_star
from src.ecs.components.c_star import CStar
from src.ecs.components.c_transform import CTransform


def system_star_generator(world:esper.World, star_data:dict, screen_data:dict):
    
    random_number = random.randint(0, star_data["probability"])

    if random_number != 0:
        return None
    
    stars = world.get_components(CStar, CTransform)
    count = 0
    for entity, (star, transform) in stars:
        count += 1

    if count >= star_data["number_of_stars"]:
        return None
    
    create_star(world, star_data, screen_data)