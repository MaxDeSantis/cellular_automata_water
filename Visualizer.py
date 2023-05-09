import pygame

from Parameters import Parameters
from SimulationState import SimulationState, Position

class Visualizer:
    def __init__(self, params:Parameters):
        self.params = params
        
        
        pygame.init()
        self.size = self.params.WIDTH * self.params.GRID_SIZE, self.params.HEIGHT * self.params.GRID_SIZE
        self.screen = pygame.display.set_mode(self.size)
        
        pygame.display.set_caption('Cellular Automata Water')
        
        self.COLOR_AIR = (255, 255, 255)
        self.COLOR_SOLID = (127, 75, 0)
        self.COLOR_WATER = (0, 0, 255)
        
        
        self.solid_dragging = False
        self.water_dragging = False
        self.background = pygame.Surface(self.screen.get_size())
        
        self.font = pygame.font.SysFont("monospace", 30)
    
    def update_screen(self, sim_state:SimulationState) -> bool:
        ev = pygame.event.get()
        
        for event in ev:
            if event.type == pygame.QUIT:
                pygame.quit()
                return False
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == pygame.BUTTON_LEFT:
                    self.solid_dragging = True
                if event.button == pygame.BUTTON_RIGHT:
                    self.water_dragging = True
                    
            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == pygame.BUTTON_LEFT:
                    self.solid_dragging = False
                if event.button == pygame.BUTTON_RIGHT:
                    self.water_dragging = False
        
        
        if self.solid_dragging:
            pos = pygame.mouse.get_pos()
            
            x = pos[0] // self.params.GRID_SIZE
            y = pos[1] // self.params.GRID_SIZE
            
            new_pos = Position(x, y)
            sim_state.add_solid(new_pos)
        
        elif self.water_dragging:
            pos = pygame.mouse.get_pos()
            
            x = pos[0] // self.params.GRID_SIZE
            y = pos[1] // self.params.GRID_SIZE
            
            new_pos = Position(x, y)
            sim_state.add_water(new_pos)

        pygame.draw.rect(self.background, self.COLOR_AIR, (0, 0, self.size[0], self.size[1]))
        
        for i, solid in enumerate(sim_state.solids):
            y = i // self.params.WIDTH
            x = i - y * self.params.WIDTH
            
            water = sim_state.water[y*self.params.WIDTH + x]
            if solid:
                rect = pygame.Rect(x*self.params.GRID_SIZE, y*self.params.GRID_SIZE, self.params.GRID_SIZE, self.params.GRID_SIZE)
                pygame.draw.rect(self.background, self.COLOR_SOLID, rect, self.params.GRID_SIZE)
            elif water > 0:
                water_weighted_color = (0, 0, water)
                rect = pygame.Rect(x*self.params.GRID_SIZE, y*self.params.GRID_SIZE, self.params.GRID_SIZE, self.params.GRID_SIZE)
                pygame.draw.rect(self.background, water_weighted_color, rect, self.params.GRID_SIZE)
        
        self.screen.blit(self.background, (0,0))
        pygame.display.flip()

        return True