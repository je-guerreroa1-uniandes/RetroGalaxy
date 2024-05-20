import asyncio
import json
import pygame
import esper

from src.create.prefab_creator import cargar_nivel, create_bullet_square, create_player_bullet, create_square, create_player, create_input_player
from src.create.prefab_creator import create_square, create_player, create_input_player, create_game_entity, \
    create_unpause_message, create_pause_message
from src.ecs.components.c_game_state import CGameState, GameState
from src.ecs.components.c_input_command import CInputCommand, CommandPhase
from src.ecs.components.c_surface import CSurface
from src.ecs.components.c_transform import CTransform
from src.ecs.components.c_velocity import CVelocity
from src.ecs.systems.s_alien_state import system_alien_state
from src.ecs.systems.s_animation import system_animation
from src.ecs.systems.s_bullet_screen_stop import system_bullet_screen_stop
from src.ecs.systems.s_bulltet_collision import system_bullet_collision
from src.ecs.systems.s_enemy_screen_bounce import system_enemy_screen_bounce
from src.ecs.systems.s_enemy_shoot import system_enemy_shoot
from src.ecs.systems.s_explosion_life import system_explosion_life
from src.ecs.systems.s_game_state import system_game_state
from src.ecs.systems.s_input_player import system_input_player
from src.ecs.systems.s_movement import system_movement
from src.ecs.systems.s_player_screen_stop import system_player_stop
from src.ecs.systems.s_rendering import system_rendering
from src.ecs.systems.s_star_blink import system_star_blink
from src.ecs.systems.s_star_generator import system_star_generator
from src.ecs.systems.s_star_stop import system_bullet_star_stop
from src.ecs.systems.s_update_posObj import system_update_posObj


class GameEngine:
    def __init__(self) -> None:
        self._load_config_files()

        pygame.init()
        pygame.display.set_caption(self.window_cfg["title"])
        self.screen = pygame.display.set_mode(
            (self.window_cfg["size"]["w"], self.window_cfg["size"]["h"]),
            pygame.SCALED)

        self.clock = pygame.time.Clock()
        self.is_running = False
        self.framerate = self.window_cfg["framerate"]
        self.delta_time = 0
        self.bg_color = pygame.Color(self.window_cfg["bg_color"]["r"],
                                     self.window_cfg["bg_color"]["g"],
                                     self.window_cfg["bg_color"]["b"])
        self.ecs_world = esper.World()

        

        
    def _load_config_files(self):
        with open("assets/cfg/window.json", encoding="utf-8") as window_file:
            self.window_cfg = json.load(window_file)
        with open("assets/cfg/player.json") as player_file:
            self.player_cfg = json.load(player_file)
        with open("assets/cfg/level_01_cfg.json") as level_01_file:
            self.level_01_cfg = json.load(level_01_file)
        with open("assets/cfg/bullet.json") as bullet_file:
            self.bullet_cfg = json.load(bullet_file)
        with open("assets/cfg/enemies.json") as enemies_file:
            self.enemies_cfg = json.load(enemies_file)
        with open("assets/cfg/explosion.json") as explosion_file:
            self.explosion_cfg = json.load(explosion_file)
        with open("assets/cfg/starfield.json") as starfield_file:
            self.starfield_cfg = json.load(starfield_file)
        with open("assets/cfg/pause.json") as pause_file:
            self.pause_cfg = json.load(pause_file)
        

    async def run(self) -> None:
        self._create()
        self.is_running = True
        while self.is_running:
            self._calculate_time()
            self._process_events()
            self._update()
            self._draw()
            await asyncio.sleep(0)
        self._clean()

    def _create(self):
        self.game_entity = create_game_entity(self.ecs_world)
        self.game_st = self.ecs_world.component_for_entity(self.game_entity, CGameState)

        self.player_entity = create_player(self.ecs_world, self.player_cfg, self.level_01_cfg.get("player_spawn"), self.screen)
        self.player_c_vel = self.ecs_world.component_for_entity(self.player_entity, CVelocity)
        self.player_c_t = self.ecs_world.component_for_entity(self.player_entity, CTransform)
        self.player_c_s = self.ecs_world.component_for_entity(self.player_entity, CSurface)
        create_input_player(self.ecs_world)

        cargar_nivel(self.ecs_world, self.level_01_cfg, self.enemies_cfg, self.window_cfg)


    def _calculate_time(self):
        self.clock.tick(self.framerate)
        self.delta_time = self.clock.get_time() / 1000.0

    def _process_events(self):
        for event in pygame.event.get():
            
            system_input_player(self.ecs_world, event, self._do_action)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:  # Assuming 'P' is the pause key
                    if self.game_st.state == GameState.UNPAUSED:
                        self.game_st.state = GameState.PAUSED
                    else:
                        self.game_st.state = GameState.UNPAUSED

            if self.game_st.state == GameState.UNPAUSED:
                system_input_player(self.ecs_world, event, self._do_action)

            if event.type == pygame.QUIT:
                self.is_running = False

    def _update(self):
        if self.game_st.state == GameState.UNPAUSED:

            system_enemy_screen_bounce(self.ecs_world, self.window_cfg)

            system_movement(self.ecs_world, self.delta_time)
            system_update_posObj(self.ecs_world, self.delta_time)

            system_bullet_screen_stop(self.ecs_world, self.screen)
            system_bullet_star_stop(self.ecs_world, self.screen)
            system_player_stop(self.ecs_world, self.screen, self.player_entity)

            #system_enemy_shoot(self.ecs_world, self.enemies_cfg, self.bullet_cfg)

            system_alien_state(self.ecs_world, self.player_entity, self.enemies_cfg, self.window_cfg)

            system_bullet_collision(self.ecs_world, self.explosion_cfg, self.player_entity, self.screen)

            system_explosion_life(self.ecs_world, self.delta_time)

            system_star_generator(self.ecs_world, self.starfield_cfg, self.window_cfg)

        system_game_state(self.ecs_world, self.game_st, self._do_pause_action)
        system_star_blink(self.ecs_world, self.delta_time)
        system_animation(self.ecs_world, self.delta_time)
        self.ecs_world._clear_dead_entities()

    def _draw(self):
        self.screen.fill(self.bg_color)
        system_rendering(self.ecs_world, self.screen)
        pygame.display.flip()

    def _clean(self):
        pygame.quit()

    def _do_action(self, c_input: CInputCommand):
        if c_input.name == "PLAYER_LEFT":
            if c_input.phase == CommandPhase.START:
                self.player_c_vel.vel.x -= self.player_cfg.get("input_velocity")
            elif c_input.phase == CommandPhase.END:
                self.player_c_vel.vel.x += self.player_cfg.get("input_velocity")

        if c_input.name == "PLAYER_RIGHT":
            if c_input.phase == CommandPhase.START:
                self.player_c_vel.vel.x += self.player_cfg.get("input_velocity")
            elif c_input.phase == CommandPhase.END:
                self.player_c_vel.vel.x -= self.player_cfg.get("input_velocity")

        if c_input.name == "PLAYER_FIRE":
            #print("Player fired")
            create_player_bullet(self.ecs_world, self.bullet_cfg, self.player_entity)


    def _do_pause_action(self, is_paused: bool):
        if is_paused:
            create_unpause_message(self.ecs_world, self.screen, self.pause_cfg)

