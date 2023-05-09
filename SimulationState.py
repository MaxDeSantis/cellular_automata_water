
from Parameters import Parameters

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
        
    
    def add_solid(self, pos:Position):
        
        # Ensure we have a valid cell
        if pos.x < 0 or pos.x > self.params.WIDTH - 1:
            return
        if pos.y < 0 or pos.y > self.params.HEIGHT - 1:
            return
        
        self.solids[pos.y*self.params.WIDTH + pos.x] = True
    
    def update_state(self):
        pass