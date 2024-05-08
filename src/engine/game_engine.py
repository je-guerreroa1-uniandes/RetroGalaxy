import asyncio
import json
import pygame
import esper


#from src.create.prefab_creator import crear_cuadrado

from src.create.prefab_creator import crear_texto, create_input_player
from src.ecs.components.c_input_command import CInputCommand, CommandPhase
from src.ecs.components.c_surface import CSurface
from src.ecs.components.c_transform import CTransform
from src.ecs.components.c_velocity import CVelocity


from src.ecs.systems.s_input_player import system_input_player
from src.ecs.systems.s_rendering import system_rendering

class GameEngine:
    def __init__(self) -> None:
        self.is_running = False
        pygame.init()

        self.load_data()

        self.screen = pygame.display.set_mode((self.window_data["size"]["w"], self.window_data["size"]["h"]), 0)
        pygame.display.set_caption(self.window_data["title"])

        self.clock = pygame.time.Clock()
        self.framerate = self.window_data["framerate"]
        self.delta_time = 0

        self.ecs_world = esper.World()

        

        
    def load_data(self):
        f1 = open("assets/cfg/window.json")
        self.window_data = json.load(f1)
        f1.close()

        # cargar demas elementos

        

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

        # crear jugador, datos ...
        create_input_player(self.ecs_world)
        
        # crear textos de pantalla

        self.is_paused = False
        self.paused_text = None


        

    def _calculate_time(self):
        self.clock.tick(self.framerate)
        self.delta_time = self.clock.get_time() / 1000.0


    def _process_events(self):
        for event in pygame.event.get():
            system_input_player(self.ecs_world, event, self._do_action)
            if event.type == pygame.QUIT:
                self.is_running = False


    def _update(self):



        if not self.is_paused:

            #systems

            pass

        self.ecs_world._clear_dead_entities()


    def _draw(self):

        self.screen.fill((self.window_data["bg_color"]["r"], self.window_data["bg_color"]["g"], self.window_data["bg_color"]["b"]))

        system_rendering(self.ecs_world, self.screen)

        pygame.display.flip()


    def _clean(self):
        self.ecs_world.clear_database()
        pygame.quit()


    def _do_action(self, c_input: CInputCommand):

        # inputs del jugador

        if c_input.name == "PAUSE":
            if c_input.phase == CommandPhase.START:
                if self.is_paused:
                    self.is_paused = False
                    self.ecs_world.delete_entity(self.paused_text)
                else:
                    self.is_paused = True
                    self.paused_text = crear_texto(self.ecs_world, "PAUSED", 
                                                   pygame.Vector2(self.level_data["player_spawn"]["position"]["x"] , self.level_data["player_spawn"]["position"]["y"]), 
                            pygame.Color(255,255,255), 20)
            
        