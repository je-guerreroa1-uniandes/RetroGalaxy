from typing import Callable

import esper
from src.ecs.components.c_game_state import CGameState, GameState
from src.ecs.components.tags.c_tag_message_pause import CTagMessagePause
from src.ecs.components.c_message import CMessage


def system_clear_text(world: esper.World, game_state: GameState):
    components = world.get_components(CMessage)

    for message_id, (_) in components:
        world.delete_entity(message_id)
    
