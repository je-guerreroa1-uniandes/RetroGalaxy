import esper
from src.ecs.components.c_explosion import CExplosion

def system_explosion_life(world:esper.World, deltatime: float):
    components = world.get_component(CExplosion)

    explotion:CExplosion
    for entity, (explotion) in components:
        explotion.timeAlive += deltatime
        if explotion.source == "player" and explotion.timeAlive >= 0.6:
            world.delete_entity(entity)
        elif explotion.source == "enemy" and explotion.timeAlive >= 0.3:
            world.delete_entity(entity)