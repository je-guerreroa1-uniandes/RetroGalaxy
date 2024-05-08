import esper
from src.ecs.components.c_animation import CAnimation
from src.ecs.components.c_surface import CSurface


def system_animation(ecs_world:esper.World, delta_time:float):
    components = ecs_world.get_components(CAnimation, CSurface)

    for _, (animation, surface) in components:

        animation.curr_anim_time -= delta_time

        if animation.curr_anim_time <= 0:

            animation.curr_anim_time = animation.animations_list[animation.curr_anim].framerate

            animation.curr_frame += 1

            if animation.curr_frame > animation.animations_list[animation.curr_anim].end:
                animation.curr_frame = animation.animations_list[animation.curr_anim].start

            rect_surf = surface.surf.get_rect()
            surface.area.w = rect_surf.w / animation.number_frames
            surface.area.x = surface.area.w * animation.curr_frame
