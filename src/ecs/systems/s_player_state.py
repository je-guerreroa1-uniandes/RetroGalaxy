import esper

from src.ecs.components.c_animation import CAnimation
from src.ecs.components.c_player_state import CPlayerState, PlayerState
from src.ecs.components.c_velocity import CVelocity

def system_player_state(world: esper.World):
    components = world.get_components(CVelocity, CAnimation, CPlayerState)

    for _, (velocity, animation, player_state) in components:
        
        if player_state.state == PlayerState.IDLE:
            _do_idle_state(velocity, animation, player_state)
        elif player_state.state == PlayerState.MOVE:
            _do_move_state(velocity, animation, player_state)

def _do_idle_state(velocity: CVelocity, animation: CAnimation, player_state: CPlayerState):
    _set_animation(animation, 1)
    if velocity.vel.magnitude_squared() > 0:
        player_state.state = PlayerState.MOVE


def _do_move_state(velocity: CVelocity, animation: CAnimation, player_state: CPlayerState):
    _set_animation(animation, 0)
    if velocity.vel.magnitude_squared() <= 0:
        player_state.state = PlayerState.IDLE


def _set_animation(animation: CAnimation, anim: int):
    if animation.curr_anim == anim:
        return
    animation.curr_anim = anim
    animation.curr_anim_time = 0
    animation.curr_frame = animation.animations_list[animation.curr_anim].start