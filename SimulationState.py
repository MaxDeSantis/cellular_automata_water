
from Parameters import Parameters

import copy

class Position:
    def __init__(self, x, y):
        self.x = x
        self.y = y
    
    def get_string(self):
        return f'Position({self.x}, {self.y})'

    def __str__(self) -> str:
        return self.get_string()
    
    def __repr__(self) -> str:
        return self.get_string()

class SimulationState:
    def __init__(self, params:Parameters):
        self.params = params
        
        # Solids are placed by the user. Water is spawned by user and spreads. Air is everything that isn't solid or water.
        # - Solid is binary. Water if a byte from 0 to 255 depending on how full.
        self.solids = [False] * self.params.HEIGHT * self.params.WIDTH
        self.water = [0] * self.params.HEIGHT * self.params.WIDTH
        self.new_water = [0] * self.params.HEIGHT * self.params.WIDTH
        
        
    
    def add_solid(self, pos:Position):
        
        # Ensure we have a valid cell
        if pos.x < 0 or pos.x > self.params.WIDTH - 1:
            return
        if pos.y < 0 or pos.y > self.params.HEIGHT - 1:
            return
        
        self.solids[pos.y*self.params.WIDTH + pos.x] = True
        
    def add_water(self, pos:Position):
        # Ensure we have a valid cell
        if pos.x < 0 or pos.x > self.params.WIDTH - 1:
            return
        if pos.y < 0 or pos.y > self.params.HEIGHT - 1:
            return
        
        new_water = min(self.water[pos.y*self.params.WIDTH + pos.x] + 20, 255)
        self.water[pos.y*self.params.WIDTH + pos.x] = new_water
        
    def get_stable_water_below(self, total_mass):
        if total_mass <= 1:
            return 1
        
        elif total_mass < 2 * self.params.MAX_WATER + self.params.MAX_COMPRESS:
            return int((self.params.MAX_WATER**2 + total_mass*self.params.MAX_COMPRESS) / (self.params.MAX_WATER + self.params.MAX_COMPRESS))
        else:
            return int((total_mass + self.params.MAX_COMPRESS) // 2)
    
    def update_state(self):
        for y in range(0, self.params.HEIGHT):
            for x in range(0, self.params.WIDTH):
                
                # Don't calculate for solids
                if self.solids[y*self.params.WIDTH + x]:
                    continue
                
                flow = 0
                remaining_mass = self.water[y*self.params.WIDTH + x]
                
                # Check below block for solid
                if y < self.params.HEIGHT - 1 and not self.solids[(y+1)*self.params.WIDTH + x]:
                    # There is no solid underneath. Move downards.
                    flow = self.get_stable_water_below(remaining_mass + self.water[(y+1)*self.params.WIDTH + x])
                    if flow > self.params.MIN_FLOW:
                        flow *= 0.5
                        
                    flow = max(0, min(flow, min(self.params.MAX_FLOW, remaining_mass)))
                    self.new_water[y*self.params.WIDTH + x] -= flow
                    self.new_water[(y+1)*self.params.WIDTH + x] += flow
                    remaining_mass -= flow
                    
                if remaining_mass <0:
                    continue
        
        self.water = copy.deepcopy(self.new_water)
        self.new_water = [0]*self.params.HEIGHT*self.params.WIDTH