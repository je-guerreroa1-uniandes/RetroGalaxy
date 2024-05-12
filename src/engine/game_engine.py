import asyncio
import json
import pygame
import esper

from src.create.prefab_creator import create_square, create_player, create_input_player, create_game_entity, \
    create_unpause_message, create_pause_message
from src.ecs.components.c_game_state import CGameState, GameState
from src.ecs.components.c_input_command import CInputCommand, CommandPhase
from src.ecs.components.c_surface import CSurface
from src.ecs.components.c_transform import CTransform
from src.ecs.components.c_velocity import CVelocity
from src.ecs.systems.s_animation import system_animation
from src.ecs.systems.s_game_state import system_game_state
from src.ecs.systems.s_input_player import system_input_player
from src.ecs.systems.s_movement import system_movement
from src.ecs.systems.s_rendering import system_rendering


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
        # create_square(self.ecs_world,
        #               pygame.Vector2(50, 50),
        #               pygame.Vector2(150, 100),
        #               pygame.Vector2(-100, 200),
        #               pygame.Color(255, 255, 100))
        self.player_entity = create_player(self.ecs_world, self.player_cfg, self.level_01_cfg.get("player_spawn"), self.screen)
        self.player_c_vel = self.ecs_world.component_for_entity(self.player_entity, CVelocity)
        self.player_c_t = self.ecs_world.component_for_entity(self.player_entity, CTransform)
        self.player_c_s = self.ecs_world.component_for_entity(self.player_entity, CSurface)
        create_input_player(self.ecs_world)


    def _calculate_time(self):
        self.clock.tick(self.framerate)
        self.delta_time = self.clock.get_time() / 1000.0

    def _process_events(self):
        for event in pygame.event.get():
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
            system_movement(self.ecs_world, self.delta_time)
        system_game_state(self.ecs_world, self.game_st, self._do_pause_action)
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

        if c_input.name == "PLAYER_UP":
            if c_input.phase == CommandPhase.START:
                self.player_c_vel.vel.y -= self.player_cfg.get("input_velocity")
            elif c_input.phase == CommandPhase.END:
                self.player_c_vel.vel.y += self.player_cfg.get("input_velocity")

        if c_input.name == "PLAYER_DOWN":
            if c_input.phase == CommandPhase.START:
                self.player_c_vel.vel.y += self.player_cfg.get("input_velocity")
            elif c_input.phase == CommandPhase.END:
                self.player_c_vel.vel.y -= self.player_cfg.get("input_velocity")

        if c_input.name == "PLAYER_FIRE":
            print("Player fired")


    def _do_pause_action(self, is_paused: bool):
        if is_paused:
            create_unpause_message(self.ecs_world, self.screen, self.pause_cfg)

