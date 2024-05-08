import esper
from src.ecs.components.c_explosion import CExplosion

def system_explosion_life(world:esper.World, deltatime: float):
    components = world.get_component(CExplosion)

    explotion:CExplosion
    for entity, (explotion) in components:
        explotion.timeAlive += deltatime
        if explotion.timeAlive >= 0.5:
            world.delete_entity(entity)