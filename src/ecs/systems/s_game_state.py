from typing import Callable

import esper
from src.ecs.components.c_game_state import CGameState, GameState
from src.ecs.components.tags.c_tag_message_pause import CTagMessagePause


def system_game_state(world: esper.World, game_state: GameState, do_action: Callable[[bool], None]):
    components = world.get_components(CTagMessagePause)
    for message_id, (_) in components:
        world.delete_entity(message_id)
    do_action(game_state.state == GameState.PAUSED)
